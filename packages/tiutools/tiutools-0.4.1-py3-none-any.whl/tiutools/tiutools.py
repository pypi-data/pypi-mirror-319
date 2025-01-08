#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ncdegroot'

from typing import Optional, Union
from typing_extensions import Final
import socket
from contextlib import contextmanager
# from gluon.storage import Storage
# import datetime
import dateutil.parser  # type: ignore
import sys
import json
from configparser import ConfigParser
import os
from pathlib import Path, PurePath
import time
import getpass
# import base64
import datetime as dt
from dataclasses import dataclass

import csv
import ldap3  # type: ignore
# from ldap3.core.exceptions import LDAPSocketOpenError, LDAPException
# from pydantic import BaseModel, validator
from attrs import define, field
from rich.prompt import Prompt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # imports
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import requests
import logging
import keyring

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s",
                    level=logging.ERROR)
mod_logger = logging.getLogger(__name__)

URI: Final = "ldap://ldap.uvt.nl:389"
IP: Final = "137.56.247.196"
TIMEOUT: Final = 10.0

db = None  # Note: has to be set from model or controller
noprint = False


def download_transactions(appid: str,
                          logger=mod_logger,
                          date=None,
                          user=None, use_test=False) -> str:
    def rename_download_file(newname: str, folder_of_download: str, time_to_wait: int = 60) -> str:
        """ watch a download folder for time_to_wait seconds
            and rename the latest download to 'newname'
        """
        new_path_filename = os.path.join(folder_of_download, newname)
        if os.path.exists(new_path_filename):
            os.remove(new_path_filename)
        time_counter = 0
        filename = max([f for f in os.listdir(folder_of_download)],
                       key=lambda xa: os.path.getctime(os.path.join(folder_of_download,
                                                                    xa)))
        while '.part' in filename:
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                raise Exception(f'Waited too long for file to download for {appid}')
        filename = max([f for f in os.listdir(folder_of_download)],
                       key=lambda xa: os.path.getctime(os.path.join(folder_of_download,
                                                                    xa)))
        os.rename(os.path.join(folder_of_download, filename),
                  new_path_filename)
        return new_path_filename

    # appid is ignored
    assert user, "Needs parameter user"
    # url = "https://testpsp.uvt.nl/Transactions/GetOrderInformation/1234567890120008"
    url_psp = 'https://{}psp.uvt.nl/Transactions'.format("test" if use_test else "")  # getting this url at end
    dirpath = os.getcwd()
    download_dir = os.path.join(dirpath, "applications", "dibsa", "private")
    chrome_options = Options()
    chrome_options.headless = False
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    # path_to_driver = 'C:/chromedriver.exe' # location of chromedriver
    # assume chromedriver is in the path
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_psp)
    # we get redirected to sso page @sso.uvt.nl
    logger.warning('log in')
    # driver.find_element_by_id('username').send_keys(user.name)  
    driver.find_element(By.ID, "username").send_keys(user.name)  # the ID would be different for different website/forms
    driver.find_element(By.ID, 'password').send_keys(str(user.passwd))
    driver.find_element(By.NAME, 'login').click()  # submit() not working on W2012 Chrome

    session = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    time.sleep(3)

    logger.warning('search from {}'.format(date))
    driver.find_element(By.ID, 'Fromdate').send_keys('\b' * 10 + date)
    driver.find_element(By.ID, 'Fromdate').send_keys(Keys.TAB)
    # driver.find_element(By.ID, 'Searchtext').click()
    # (not working on W2012 Chrome) just to remove the calendar so the search button can be clicked
    driver.find_element(By.XPATH, "//*[@value='search']").click()
    time.sleep(4)
    # we are now in the internetkassa
    # select an app_id
    # s = Select(driver.find_element(By.ID, 'SelectedApplicationId'))
    # s.select_by_visible_text(appid)
    # driver.find_elements_by_name("command")[1].click()
    logger.warning('start download to {}'.format(download_dir))
    driver.find_element(By.XPATH, "//*[@value='export']").click()
    time.sleep(6)

    driver.close()
    ffn = rename_download_file('transactions.csv', download_dir)
    return ffn


def alert(msg):
    print((sys.stderr, msg))
    sys.exit(1)


# noinspection PyTypeChecker
def sso_user(is_web=False, reset_user=False, logger=None):
    @define
    class User(object):
        name: str
        passwd: str

    dirs = os.path.dirname(__file__)
    ini_name = 'sso_config.ini'
    appname = PurePath(dirs).parts[-2]
    if not logger:
        logger = logging.getLogger(__name__)

    # raise NameError("You need to pass logger as a parameter in sso_user()")

    def sso_config():
        """
        open ini file report or create if not already present
        :return: parser object for ini file
        """

        sso_config = ConfigParser()

        path = os.path.join('applications',
                            appname,
                            'private',
                            ini_name) if is_web else ini_name
        if not os.path.exists(path):
            logger.warning("Creating sss_config.ini file in {}".format(path))
            sso_config = ConfigParser()
            sso_config.add_section('user')
            with open(path, "w") as config_file:
                # noinspection PyTypeChecker
                sso_config.write(config_file)
                logger.info("Created SSO_Config file")
        sso_config.read(path)
        sso_config.path = path  # monkey patch

        return sso_config

    sso_config = sso_config()
    # reset_user = False
    if not sso_config.has_option('user', 'name') or reset_user:
        if is_web:
            msg = "ERROR create a valid sso_config.ini"
            logger.error(msg)
        username = input('Enter SSO username')
        sso_config.set('user', 'name', username)
        passwd = getpass.getpass(prompt='Enter SSO password')
        # store the password
        keyring.set_password('sso_login', username, passwd)
        with open(sso_config.path, "w") as config_file:
            sso_config.write(config_file)

    username = sso_config.get('user', 'name')

    passwd = None
    if username != '':
        passwd = keyring.get_password('sso_login', username)
    user = User(name=username,
                passwd=passwd)

    return user


@define
class Failed:
    order_id: int
    error: str
    person_id: int


@define
class Corrected:
    order_id: int
    orig_balance: float
    amount: float
    person_id: int


@dataclass
class PaymentResults:
    ok: Optional[list[str]]
    corrected: Optional[list[Corrected]]
    not_found: list[str]
    failed: Optional[list[Failed]]


@dataclass
class Result:
    results: str


@dataclass
class P2A:
    person_id: int
    activity_id: int


@dataclass
class ResultsAndData:
    results: PaymentResults
    data_for_correction_mails: list[P2A]


class CheckPayments:
    """
    read csv file(s) downloaded from Internetkassa
    """

    def __init__(self,
                 db=None,
                 logger=mod_logger,
                 report_only=False,
                 folder=None,
                 in_test=False) -> None:
        assert db, "Needs a (PyDAL) db"
        self.db = db
        self.logger = logger

        self.report_only = report_only
        self.in_test = in_test
        self.results = PaymentResults(ok=[], corrected=[], not_found=[], failed=[])
        self.logbook = ""
        self.data = {"time": dt.datetime.now().isoformat(), "changes": []}
        self.data_for_correction_mails: list[P2A] = []

        appname = os.path.split(__file__)[0].split(os.path.altsep)[-2]
        self.folder = folder or os.path.join('applications', appname)

    def run(self) -> Union[Result, ResultsAndData]:
        try:
            user = sso_user(is_web=False)
            self.logger.info("User set :-)")
        except Exception as e:
            msg = "Failed to set user: {}".format(e)
            self.logger.error(msg)
            return Result(results=msg)

        appid = 'TESTTST'
        try:
            _ = download_transactions(appid=appid,
                                      date=(dt.datetime.now() -
                                            dt.timedelta(days=365
                                                         )).strftime('%d-%m-%Y'),
                                      user=user,
                                      use_test=self.in_test)
            self.logger.info("Downloaded transaction file")
        except Exception as e:
            msg = f"Failed to download transaction file: due to {e}"
            self.logger.error(msg)
            return Result(results=msg)

        try:
            filename = os.path.join(self.folder, 'private', 'transactions.csv')
        except Exception as e:
            msg = f"couldn't get filename using self.folder:{self.folder} due to {e}"
            self.logger.error(msg)
            return Result(results=msg)
        try:
            with open(filename, 'r', encoding='utf-8-sig') as csv_file:
                # an utf file might start with a BOM char, should be recognised utf8 is not enough
                reader = csv.DictReader(csv_file, delimiter=';')
                assert reader.fieldnames == ['Application', 'Amount', 'Timestamp (GMT)',
                                             'Timestamp (W. Europe Standard Time)', 'Prefix', 'OrderReference',
                                             'Name', 'Status', 'Statusreferentie', 'PaymentMethod'], \
                    "Wrong fieldnames in header"
                self.check(reader)
                self.logger.info("Results OK: {} \tNOT FOUND: {} \tFAILED: {} \tCORRECTED: {}\n".format(
                    len(self.results.ok) if self.results.ok else 0,
                    len(self.results.not_found) if self.results.not_found else 0,
                    len(self.results.failed) if self.results.failed else 0,
                    len(self.results.corrected)) if self.results.corrected else 0)
        except Exception as e:
            msg = f"Could not open transactions file or check rows. Due to {e}"
            self.logger.error(msg)
            return Result(results=msg)
        return ResultsAndData(results=self.results,
                              data_for_correction_mails=self.data_for_correction_mails)

    def check(self, reader):
        for row in reader:
            # skip tst myprint transaction and failed ones
            if (row['Application'] == 'tstmyprint') or (row['Status'] != "Y"):
                self.logger.warning("Application == tstmyprint or Status != Y, {}".format(row))
                continue
            self.check_row(row)
        return

    def check_row(self, csv_row):
        """ lookup transaction id. Should be there. And check if balance ok
             otherwise correct it"""
        db = self.db
        order_id = csv_row['OrderReference']
        if len(order_id) > 5:
            order_id = order_id[12:]
        payment_time = dateutil.parser.parse(csv_row['Timestamp (W. Europe Standard Time)'])
        amount = float(csv_row['Amount'].replace(',', '.'))

        # check if orderid from csv exists in db
        # changed db.person2activity.orderid to db.person2activity.id
        found = db(db.person2activity.id == order_id).select(db.person2activity.ALL)
        if not found:
            self.results.not_found.append(order_id)
            return

        found = found[0]
        person_id = found.person
        activity_id = found.activity
        if found.balance == 0.0:
            self.results.ok.append(order_id)
        else:
            try:
                orig_balance = found.balance
                if orig_balance == amount and found.amount == amount:
                    # case when feedback url didn't fire and amount didn't change
                    found.balance -= amount
                    if not self.report_only:
                        found.update_record()
                    self.logger.info("{} database record for transaction-id "
                                     "{} from €{} to €{} by subtracting €{}.\n"
                                     .format("Would change" if self.report_only else "Changed",
                                             order_id,
                                             orig_balance,
                                             found.balance,
                                             amount))
                    try:
                        if not self.report_only:
                            db(db.person2activity.id == order_id).update(balance=0.0,
                                                                         confirm_on=payment_time)
                            db.commit()
                        self.data['changes'].append({
                            'order_id': order_id,
                            'orig_balance': orig_balance,
                            'amount': amount,
                            'person_id': person_id,
                            'activity_id': activity_id
                        })
                        self.logger.info(
                            "Db update/commit successful for transaction id: {} \n".format(order_id))
                        self.data_for_correction_mails.append(P2A(person_id=person_id, activity_id=activity_id))
                    except Exception as e:
                        self.logger.error(f"Db update/commit NOT successful for "
                                          f"transaction id: {order_id} "
                                          f"error {e}\n")

                else:
                    raise Exception(f"Balance in database (€{orig_balance}) doesn't match "
                                    f"paid amount (€{amount}) "
                                    f"in Internetkassa or amount in db "
                                    f"has changed to {found.amount}")

            except Exception as e:
                self.logger.error("ERROR updating balance : {}.\n".format(e))
                self.results.failed.append(
                    Failed(order_id=order_id,
                           error=f"ERROR updating balance : {e}",
                           person_id=person_id))
                pass
            else:
                self.results.corrected.append(
                    Corrected(order_id=order_id,
                              orig_balance=orig_balance,
                              amount=amount,
                              person_id=person_id))
                #  outfile: TextIO[str]
                with open(Path(self.folder) / "private" / "payment_corrections.txt", 'w') as outfile:
                    # noinspection PyTypeChecker
                    json.dump(self.data, outfile)

        return


# provide ldap server object a context  manager (guaranties auto close/unbind)
# noinspection PyUnresolvedReferences
@contextmanager
def tiu_ldap():
    def check_connection():
        """ check  if LDAP server is available
        :return: True or False
        """
        (family, socktype, proto, garbage, address) = \
            socket.getaddrinfo(IP, "ldap")[0]  # Use only the first tuple
        s = socket.socket(family, socktype, proto)
        try:
            s.connect(address)
            return True
        except Exception as e:
            alert("Something is wrong with %s. Exception type is %s" % (address, e))
            return False

    check_connection()
    tiu_ld = ldap3.initialize(uri=URI)  # does not open connection just inits and always succeeds
    tiu_ld.set_option(ldap3.OPT_NETWORK_TIMEOUT, TIMEOUT)
    tiu_ld.set_option(ldap3.OPT_TIMEOUT, TIMEOUT)
    tiu_ld.set_option(ldap3.OPT_REFERRALS, 0)
    try:
        yield tiu_ld
    finally:
        tiu_ld.unbind()


def parentify(tel):
    return tel


def ldap_search(search=None, fields=None):
    """ given a search dictionary specifying field and values,
        and an optional (valid) list of ldap fields to retrieve
        get ldap info  from the ldap server
    :param search: list of dicts: conditions in each dict are added
    :param fields: list of string:
    :returns ( result, first entry (flattened),
    list of all entries (dict) found) otherwise  None, dict with error msg"""

    if search is None:
        search = dict(uid="ndegroot")
    if fields is None:
        fields = ('cn', 'sn', 'uid',
                  'initials', 'mail', 'givenName',
                  'uvt-lau', 'employeeNumber', 'telephoneNumber',
                  'roomNumber')

    # create or combination if needed
    if isinstance(search, list):

        # print search
        search_term = '(|'
        for or_part in search:
            ldap_attrs = ""
            for k, v in or_part.items():
                ldap_attrs += '({0}={1})'.format(k, v)

            part = '(&(objectclass=person)%s)' % ldap_attrs
            search_term += part
        search_term += ')'

    else:
        ldap_attrs = ""
        for k, v in search.items():
            ldap_attrs += '({0}={1})'.format(k, v)

        search_term = '(&(objectclass=person)%s)' % ldap_attrs
    server = ldap3.Server(URI, get_info=ldap3.ALL, connect_timeout=2)
    # attrs = ['*']
    try:
        with ldap3.Connection(server, auto_bind=ldap3.AUTO_BIND_DEFAULT) as conn:
            try:
                # was working with ldap.SCOPE_SUBTREE is std with ldap3
                rs = conn.search('o=Universiteit van Tilburg,c=NL',
                                 search_term,
                                 attributes=fields)
                try:
                    return rs, conn.entries
                except IndexError as e:
                    return rs, dict(msg='while searching: {}'.format(e))

            except ldap3.core.exceptions.LDAPException as e:
                return None, dict(msg='LDAPExc. while searching: {}'.format(e))
            except Exception as e:
                return None, dict(msg='other exception: {}'.format(e))

    except ldap3.core.exceptions.LDAPSocketOpenError as e:
        msg = f"LDAP server {URI} not accessible. Error:{e}. Maybe start GlobalProtect VPN?"
        if not noprint:
            print(msg)
        return None, dict(msg=msg)


def ldap_search_staff():
    return ldap_search([dict(organizationalstatus='Staff', ou='TST*'),
                        dict(organizationalstatus='PNIL', ou='TST*'),
                        dict(organizationalstatus='Staff', ou='AS: Education Support Team TST'),
                        dict(organizationalstatus='Staff', RoomNumber='N*'),
                        dict(organizationalstatus='PNIL', RoomNumber='N*')])


def lookup_user(db_, user):
    username = user.registration_id.split('/')[3]
    # record is present (created now or earlier by CAS
    # lets update the other fields
    result, info = ldap_search(dict(uid=username))
    if result:
        # sometimes givenName is missing in Ldap: prevent overwriting it
        # use first element
        info = info[0]
        registration_id = "https://sso.uvt.nl/%s" % username
        try:
            if info['givenName']:
                db_(db_.auth_user.registration_id == registration_id).update(
                    username=username,
                    email=info['mail'],
                    first_name=info['givenName'],
                    last_name=info['sn'])
            else:
                db_(db_.auth_user.registration_id == registration_id).update(
                    username=username,
                    email=info['mail'],
                    last_name=info['sn'])
        except AttributeError:
            msg = "No update, couldn't find registration_id {} in db[{}].auth_user".format(registration_id, db_)
            if not noprint:
                print(msg)


def beheer_check_time_since(datafile):
    time_df = dateutil.parser.parse(datafile['time'])
    time_fr = time_df.strftime("%d-%m-%Y %H:%M:%S")
    time_fr = "{}".format(time_fr)
    since = dt.datetime.now() - time_df
    since_fr = ("{} day(s) "
                "{} hour(s) "
                "and {} minute(s) ago ").format(since.days,
                                                since.seconds // 3600,
                                                (since.seconds // 60) % 60)
    return time_fr, since_fr


def beheer_get_previous_corrections():
    # dibsa
    upload_folder = "applications/dibsa/private"
    # sl = "\\"
    # path = upload_folder + sl
    datafile = None
    try:
        with open(upload_folder + '/payment_corrections.txt', 'r') as infile:
            try:
                datafile = json.load(infile)
            except ValueError:
                print("Couldn't jsonify")
        return datafile
    except IOError:
        print("failed to open payment_corrections.txt")
        return datafile


def initials_to_initialsfield(db):
    # dibsa

    persons = db(db.person).select(orderby=db.person.id,
                                   limitby=(0, 100000000)).as_list()
    logbook = ""
    count_failed = 0
    count_changed = 0
    folder = 'applications/dibsa'
    for person in persons:
        new_initials = ""
        init = person['initials']
        f_n = person['firstname']

        # if equal we're done also if we don't have a first name
        if f_n == init or f_n == "" or f_n is None or f_n == "-":
            continue

        if (init != '' and init is not None and init != '-') or '.' in init:
            logbook += ("Personid {} already has {} as initials!'"
                        "Did not change to {}.\n").format(person['id'],
                                                          init,
                                                          f_n)
            count_failed += 1
            continue

        try:
            if "." in f_n:
                new_initials = f_n.upper()
            elif f_n.isupper():
                new_initials = '.'.join(f_n)
            if new_initials != "":
                # db(db.person.id == person['id']).update(initials=new_initials, firstname='')
                # db.commit()
                count_changed += 1
                print(("Initials {} successfully moved to initials field "
                       "for personid {}").format(new_initials,
                                                 person['id']))
        except Exception as e:
            msg = "Not able to move initials ({}) from firstname field ({}) to initials field!".format(new_initials,
                                                                                                       f_n)
            print(msg)
            print(e)
            logbook += msg + '\n' + str(e) + '\n'
    logbook += "Failed to change {} initials because they already have initials!\n".format(count_failed)
    logbook += "Moved {} initials in the firstname field to initials field.".format(count_changed)
    print("Failed to change: {}".format(count_failed))
    print("Moved: {}".format(count_changed))
    with open(folder + '/private/initials_logbook.txt', 'w+') as writer:
        writer.writelines(logbook)


@define
class CField:
    msg: str = ""
    key: str = ""
    default: str = ""


@define
class BaseConfig:
    """ model for the safe keyring storage of login data in a namespace"""
    namespace: str = ""
    url: str = ""
    name: str = ""
    pw: str = ""
    default_url: str = ""

    _cfields: list[CField] = []
    reset_keys: bool = False
    app_window = None

    def __attrs_post_init__(self):
        if self.reset_keys:
            self.reset_the_keys()
        try:
            self.get_values()
        except ImportError:  # when in GUI but failing
            return

    def get_values(self):
        """ get (or first ask for) field values, uses keyring to
        store them in a safe space"""

        for c_field in self._cfields:
            value = self.get_value(c_field)
            object.__setattr__(self, c_field["key"], value)

    def get_value(self, c_field) -> Optional[str]:
        if self.app_window:
            from tkinter import simpledialog
        value = keyring.get_password(self.namespace, c_field.key)
        if value in (None, ""):
            value = simpledialog.askstring("Input",
                                           c_field.msg,
                                           parent=self.app_window) \
                if self.app_window \
                else Prompt.ask(c_field.msg,
                                default=c_field.default,
                                password=c_field.key in 'pw/password')
            if value:
                keyring.set_password(self.namespace, c_field.key, value)
                value = keyring.get_password(self.namespace, c_field.key)
        return value

    def reset_the_keys(self):
        for c_field in self._cfields:
            try:
                keyring.delete_password(self.namespace, c_field.key)
            except keyring.errors.PasswordDeleteError:
                logging.info(f"key '{c_field.key}' not found in "
                             f"'{self.namespace}' keyring storage")
                # happens only the first time, ignore it
                pass


@define
class OpenAICloudConfig(BaseConfig):
    """ model for the safe keyring storage of login data in a namespace"""
    namespace: str = "openai"
    prj_key: str = ""
    _cfields: list[CField] = [
        CField(msg=f"Enter the {namespace} prj_key)",
               key="prj_key"),
        ]


@define
class SsoConfig:
    """ model for the safe keyring storage of login data in a namespace"""
    namespace: str = "sso"
    url: str = ""
    name: str = ""
    pw: str = ""
    default_url: str = ""
    _sso_fields = (
        dict(msg=f"Enter the {namespace} URL (like {default_url})",
             key="url",
             default=default_url),
        dict(msg="Enter your login name",
             key="name",
             default=""),
        dict(msg="Enter your password",
             key="pw",
             default=""),
    )
    reset_keys: bool = False
    app_window = None

    def __attrs_post_init__(self):
        if self.reset_keys:
            self.reset_the_keys()
        try:
            self.get_values()
        except ImportError:  # when in GUI but failing
            return

    def get_values(self):
        """ get (or first ask for) field values, uses keyring to
        store them in a safe space"""

        for sso_field in self._sso_fields:
            value = self.get_value(sso_field)
            object.__setattr__(self, sso_field["key"], value)

    def get_value(self, field_) -> Optional[str]:
        if self.app_window:
            from tkinter import simpledialog
        value = keyring.get_password(self.namespace, field_["key"])
        if value in (None, ""):
            value = simpledialog.askstring("Input",
                                           field_["msg"],
                                           parent=self.app_window) \
                if self.app_window \
                else Prompt.ask(field_["msg"],
                                default=field_["default"],
                                password=field_['key'] in 'pw/password')
            if value:
                keyring.set_password(self.namespace, field_["key"], value)
                value = keyring.get_password(self.namespace, field_["key"])
        return value

    def reset_the_keys(self):
        for field_ in self._sso_fields:
            try:
                keyring.delete_password(self.namespace, field_['key'])
            except keyring.errors.PasswordDeleteError:
                logging.info(f"key '{field_['key']}' not found in "
                             f"'{self.namespace}' keyring storage")
                # happens only the first time, ignore it
                pass


# noinspection PyMethodParameters,PyUnresolvedReferences,PyClassHasNoInit
@define(kw_only=True)
class UserModel:
    """ used to validate user data """
    geslacht: str = field()

    @geslacht.validator
    def _geslacht_check(self, _attribute, value):
        """ validation """
        if value not in "MVX":
            raise ValueError(f"Veld Geslacht moet M, X of V zijn maar is nu {value}")
        return value

    voorletters: str
    voorvoegsels: str = ""
    achternaam: str
    roepnaam: str = ""
    straat: str = ""
    nummer: str = ""
    toevoeging_nummer: str = ""
    aanvulling: str = ""
    postcode: str = field()

    @postcode.validator
    def _postcode_not_empty(self, _attribute, value):
        """ validation """
        if len(value) == 0:
            raise ValueError("Veld postcode mag niet leeg zijn")
        return value

    woonplaats: str = ""
    land: str = "Nederland"
    telefoonnummer: str = ""
    geboortedatum: str = field()

    @geboortedatum.validator
    def _geboortedatum_separator(self, _attribute, value):
        """ validation """
        if value and '-' not in value:
            raise ValueError("geboortedatum bevat geen '-' als scheidingsteken")
        return value

    email: str = field()

    @email.validator
    def _email_ok(self, _attribute, value):
        if value and "@" not in value:
            raise ValueError("E-mail bevat altijd een @")

    memo: str = ""
