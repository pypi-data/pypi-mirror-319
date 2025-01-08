from typing import Optional, Union
import logging
import time
from functools import wraps

import selenium.common
import selenium.webdriver
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
# from selenium.webdriver.common.action_chains import ActionChains

from .tiutools import SsoConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# file_handler = logging.FileHandler("scrape_factory.log")
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.WARNING)
#
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

def check_auth(method):
    @wraps(method)
    def _imp(self, *method_args, **method_kwargs):
        self._open()  # check if open and authenticated or make it happen
        return method(self, *method_args, **method_kwargs)

    return _imp


class ScrapeFactory:
    def __init__(self,
                 options: Optional[list] = None,
                 db=None,
                 namespace: Optional[str] = None,
                 reset_keys: bool = False,
                 gui_app: bool = False,
                 login_page: Optional[str] = ""):

        self.options = options if options else ["--headless=new"]
        self._readconfig(namespace, reset_keys)
        self.db = db
        self.gui_app = gui_app
        self.login_page = login_page
        self.base_url = self.config.url
        self.driver: Optional[webdriver.Chrome] = None
        self.is_authenticated = False
        self.is_open = None
        self.retry = False
        self.guests = None

    def _readconfig(self, namespace="sso", reset_keys=False):
        self.config = SsoConfig(namespace=namespace,
                                default_url="https://tiuapp.uvt.nl/"
                                            "ords/idomeneo/!gastdb.gastdb.",
                                reset_keys=reset_keys)

    # The two context manager methods
    def __enter__(self):
        self._open()  # open browser using selenium
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()  # close selenium instance

    def _open(self):
        """ Open browser and authenticate """
        if not self.driver:
            logger.info("Open browser")
            options = webdriver.ChromeOptions()
            for option in self.options:
                if "window-size" in option:
                    width, height = option.split('=')[1].split(",")
                    self.headless_width = int(width)
                options.add_argument(option)
            self.driver = webdriver.Chrome(options=options)
            self._authenticate()
            self.wait = webdriver.support.ui.WebDriverWait(self.driver, 10)
        else:
            self.is_open = True

    def print(self, msg, **kwargs):
        if self.gui_app:
            self.gui_app.show_info(msg)
        else:
            console = Console()
            console.print(msg, **kwargs)

    def _authenticate(self):
        """
        after opening authenticate SSO
        set flag is_authenticate if successful
        @return:
        """
        if self.is_authenticated:
            return
            # nothing to do
        url = self.base_url + self.login_page
        self.driver.get(url)  # should cause a redirect to SSO page

        wait = WebDriverWait(self.driver, 15)
        # timeout after 15 seconds
        # wait for the SSO username field
        try:
            username = wait.until(lambda driver: driver.find_element(By.ID, 'username'))
            # was name, worked in FF
        except selenium.common.exceptions.TimeoutException:
            self.print("TimeOut Exception in _authenticate")
        else:
            try:
                # fill the two fields
                username.send_keys(self.config.name)
                self.driver.find_element(By.ID, 'password').send_keys(self.config.pw)
                self.click_submit_name('login')
                # if correct we return to the main page otherwise a Timeout occurs
            except selenium.common.exceptions.WebDriverException:  # in Chrome
                self.print("please give Chrome focus and type name and password ")
                time.sleep(20)

    def close(self):
        """ close browser connection"""
        logger.info("Close browser")
        if self.driver:
            self.driver.close()
            self.is_open = False
            self.is_authenticated = False

    @check_auth
    def get(self, command):
        """ combine url with command"""
        url = self.base_url + command
        self.driver.get(url)
        logger.debug(f"command {command} executed")

    def click_submit_name(self, name):
        """
        find element with 'name'
        fix scrolling issue
        click it
        """
        submit = self.driver.find_element(By.NAME, name)
        if submit is None:
            self.print(f"Submit knop met naam: '{name}' niet gevonden")

            return False
        # fix, note no effect when headless
        self.driver.execute_script('window.scrollTo(0, ' + str(submit.location['y']) + ');')
        submit.click()
        # self.wait_for_name()
        return True

    def wait_for(self, by_type, name, timeout=15):
        """ selenium helper: wait up to {timeout} seconds for element {name} to appear"""
        wait = selenium.webdriver.support.ui.WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: driver.find_element(by_type, name))

    def get_size_of_element(self, by_type, name):
        self.wait_for(by_type, name)
        ele = self.driver.find_element(by_type, name)
        return ele.size


class CanvasScraper(ScrapeFactory):

    @check_auth
    def get_gradebook_image(self, canvas_id: int, to_file=True) -> Union[str,bytes]:
        """ returns: filename """

        logger.info(f'Open gradebook for {canvas_id}')
        gb_url = f"https://tilburguniversity.instructure.com/courses/{canvas_id}/gradebook"
        # with webdriver.Firefox(options=options) as driver:
        self.driver.get(url=gb_url)

        try:
            last_row = self.wait.until(lambda driver: driver.find_element(By.CLASS_NAME,
                                                               "last-row"))
                                                               # "Grid__GradeCell__EndContainer"))
            time.sleep(1) # don't know what to wait for ...
        except selenium.common.exceptions.TimeoutException:
            logger.warning("Timeout Exception waiting for class 'last-row' in get_gradebook_image")
            if to_file:
                fname = f'timeout_screenshot_{canvas_id}.png'
                self.driver.save_screenshot(fname)
                return fname
            # else try to continue
        #last_row_location = last_row.location_once_scrolled_into_view
        total_column = self.driver.find_element(By.CLASS_NAME, 'total_grade')
        container = self.driver.find_element(By.CLASS_NAME, "container_1")

        # just the results, no names
        if self.headless_width - total_column.location['x'] < 25:
            raise ValueError('Restart Chrome with bigger width')

        fname = f'screenshots/{canvas_id}.png'
        container_location = container.location_once_scrolled_into_view
        time.sleep(1)  # not a clean solution...
        if to_file:
            container.screenshot(fname)
        else:
            size = container.size
            png = self.driver.get_screenshot_as_png()  # whole page
            im = Image.open(BytesIO(png))
            im = im.crop((container_location['x'],  # left
                          container_location['y'],  # top
                          container_location['x'] + size['width'],  # right
                          container_location['y'] + size['height']  # bottom
                         ))
            img_byte_arr = BytesIO()
            im.save(img_byte_arr, format="PNG")

        # self.driver.save_screenshot(fname)
        # crop empty space at end
        real_width = total_column.rect['x'] + total_column.rect['width']
        # get last-row again
        last_row = self.driver.find_element(By.CLASS_NAME,
                                            "last-row")
        try:
            real_height = last_row.location['y'] + last_row.rect['height'] - container_location['y']
        except (selenium.common.exceptions.StaleElementReferenceException, 
                selenium.common.exceptions.TimeoutException,
                selenium.common.exceptions.WebDriverException) as exc:
            logger.warning(f"{exc} element {last_row=} {container=}")
            logger.info(f"https://tilburguniversity.instructure.com/courses/{canvas_id}/gradebook"
                        f" {fname}/{canvas_id} NOT cropped")
            # lets just record the uncropped img...
            if not to_file:
                return img_byte_arr.getvalue()
        else:
            img = Image.open(fname if to_file else img_byte_arr)  # was BytesIO(png))
            img_crop = img.crop((0, 0, real_width, real_height))
            if to_file:
                img_crop.save(fname)
                logger.info(f"{fname} saved and cropped")
                return fname
            else:
                img_byte_arr = BytesIO()
                img_crop.save(img_byte_arr, format='PNG')
                return img_byte_arr.getvalue()
