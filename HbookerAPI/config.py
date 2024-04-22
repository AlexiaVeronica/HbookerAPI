from . import point


class Config:
    TIMEOUT = 20
    MAX_RETRY = 10
    APP_VERSION = '2.9.290'
    DEVICE_TOKEN = 'ciweimao_'
    ACCOUNT = ""
    LOGIN_TOKEN = ""
    USER_AGENT = 'Android com.kuangxiang.novel {app_version}'
    WEB_SITE = point.WEB_SITE

    @staticmethod
    def set_user_agent(user_agent):
        Config.USER_AGENT = user_agent

    @staticmethod
    def set_app_version(app_version):
        Config.APP_VERSION = app_version

    @staticmethod
    def set_device_token(device_token):
        Config.DEVICE_TOKEN = device_token

    @staticmethod
    def set_max_retry(max_retry):
        Config.MAX_RETRY = max_retry

    @staticmethod
    def set_timeout(timeout):
        Config.TIMEOUT = timeout

    @staticmethod
    def set_web_site(web_site):
        Config.WEB_SITE = web_site

    @staticmethod
    def set_account(account):
        Config.ACCOUNT = account

    @staticmethod
    def set_login_token(login_token):
        if len(login_token) != 32:
            raise Exception("login_token error: %s" % login_token)
        Config.LOGIN_TOKEN = login_token

    @staticmethod
    def get_common_params() -> dict:
        common_params = {
            "app_version": Config.APP_VERSION,
            "device_token": Config.DEVICE_TOKEN,
        }
        if Config.ACCOUNT and Config.LOGIN_TOKEN:
            common_params.update({"account": Config.ACCOUNT, "login_token": Config.LOGIN_TOKEN})
        return common_params

    @staticmethod
    def get_user_agent():
        if "{app_version}" in Config.USER_AGENT:
            Config.USER_AGENT = Config.USER_AGENT.format(app_version=Config.APP_VERSION)
        return Config.USER_AGENT

    @staticmethod
    def get_web_site():
        return Config.WEB_SITE

    @staticmethod
    def verify_token_empty():
        if not Config.ACCOUNT:
            print("account is empty,you can use auto_sign to get account")
        elif not Config.LOGIN_TOKEN:
            print("login_token is empty,you can use auto_sign to get login_token")
        else:
            return True
        return False
