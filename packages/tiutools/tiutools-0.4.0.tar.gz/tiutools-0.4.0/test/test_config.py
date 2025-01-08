from tiutools import SsoConfig, UserModel


def tst_init():
    """"runs in debug only and not allways, remember to use -s"""
    sso_config = SsoConfig(url="https://tilburguniversity.instructure.com",
                           reset_keys=True)
    assert sso_config.url == "https://tilburguniversity.instructure.com"

def test_user_model():
    user = UserModel(voorletters="N.C",
                     achternaam="Groot",
                     postcode="1218 HA",
                     geslacht="X",
                     geboortedatum="14-03-1961",
                     email="nico@ocinet.nl")

    assert user.postcode == "1218 HA"