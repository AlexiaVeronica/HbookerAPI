import logging
import requests
import json
from . import point, decode, config
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def new_client(account: str = "", login_token: str = "", logger: bool = False) -> 'HbookerClient':
    _client = HbookerClient(logger=logger)
    if not account or not login_token:
        auto_sign = _client.auto_sign()
        if auto_sign.get("code") == "100000":
            account = auto_sign.get("data").get("reader_info").get("account")
            login_token = auto_sign.get("data").get("login_token")
        else:
            raise Exception("auto_sign error: %s" % auto_sign.get("tip"))

    if len(login_token) != 32:
        raise Exception("login_token error: %s" % login_token)
    _client.set_common_params(account, login_token)
    _client.configure_logging()
    if not _client.verify_common_params():
        raise Exception("account or login_token is error")
    return _client


class HbookerClient:
    def __init__(self, logger: bool = False, proxies: dict = None, verify: bool = True, **kwargs):
        self.logger = logger
        self.common_params_config = config.Config
        self.session = self._configure_session(verify, proxies)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _configure_session(self, verify, proxies):
        session = requests.Session()
        http_adapter_retry = Retry(total=self.common_params_config.MAX_RETRY, backoff_factor=1,
                                   status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=http_adapter_retry))
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            "Connection": "Keep-Alive",
        })
        session.verify = verify
        if proxies:
            session.proxies.update(proxies)
        return session

    def configure_logging(self):
        if self.logger:
            logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            logging.basicConfig(level=logging.DEBUG, filename="requests_log.txt", format=logging_format)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            logging.getLogger().addHandler(console_handler)

    def set_common_params(self, account, login_token, **kwargs):
        self.common_params_config.set_account(account)
        self.common_params_config.set_login_token(login_token)
        if kwargs.get('app_version'):
            self.common_params_config.set_app_version(kwargs.get('app_version'))
        if kwargs.get('device_token'):
            self.common_params_config.set_device_token(kwargs.get('device_token'))

    @property
    def get_common_params(self):
        return self.common_params_config.get_common_params()

    def verify_common_params(self):
        if self.common_params_config.verify_token_empty():
            user_info = self.get_user_info()
            if user_info.get('code') == '100000':
                print("account: {} is login success".format(self.get_common_params.get('account')))
                return True
            print("account or login_token is error:{}".format(user_info.get('tip')))
        return False

    def _post(self, api_url: str, data=None):
        data = data or {}
        data.update(self.get_common_params)
        self.session.headers.update({'User-Agent': self.common_params_config.get_user_agent()})

        result = self.session.post(self.common_params_config.get_web_site() + api_url, data=data,
                                   timeout=self.common_params_config.TIMEOUT)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Request Error: {e}')
        except Exception as e:
            print(f'Error: {e}')
        else:
            return json.loads(decode.Decode(result.text).decrypt())

    def login(self, login_name, passwd) -> dict:
        data = {'login_name': login_name, 'passwd': passwd}
        return self._post(point.MY_SIGN_LOGIN, data)

    def get_shelf_list(self) -> dict:
        return self._post(point.BOOKSHELF_GET_SHELF_LIST)

    def get_shelf_book_list(self, shelf_id, last_mod_time='0', direction='prev') -> dict:
        data = {'shelf_id': shelf_id, 'last_mod_time': last_mod_time, 'direction': direction}
        return self._post(point.BOOKSHELF_GET_SHELF_BOOK_LIST, data)

    def get_division_list(self, book_id) -> dict:
        data = {'book_id': book_id}
        return self._post(point.GET_DIVISION_LIST, data)

    def get_updated_chapter_by_division_new(self, book_id: str) -> dict:
        return self._post(point.GET_DIVISION_LIST_NEW, {'book_id': book_id})

    def get_chapter_update(self, division_id, last_update_time='0') -> dict:
        data = {'division_id': division_id, 'last_update_time': last_update_time}
        return self._post(point.GET_CHAPTER_UPDATE, data)

    def get_info_by_id(self, book_id) -> dict:
        data = {'book_id': book_id, 'recommend': '', 'carousel_position': '', 'tab_type': '', 'module_id': ''}
        return self._post(point.BOOK_GET_INFO_BY_ID, data)

    def get_chapter_command(self, chapter_id) -> dict:
        data = {'chapter_id': chapter_id}
        return self._post(point.GET_CHAPTER_COMMAND, data)

    def get_cpt_ifm(self, chapter_id, chapter_command) -> dict:
        data = {'chapter_id': chapter_id, 'chapter_command': chapter_command}
        return self._post(point.GET_CPT_IFM, data)

    def get_chapter_content(self, chapter_id) -> [dict, None]:
        command = self.get_chapter_command(chapter_id).get('data', {}).get('command')
        response2 = self.get_cpt_ifm(chapter_id, self.get_chapter_command(chapter_id).get('data', {}).get('command'))
        if response2.get('code') != '100000':
            print("get_cpt_ifm error: %s" % response2.get('tip'))
            return
        response2 = response2["data"]["chapter_info"]
        response2['txt_content'] = decode.Decode(response2['txt_content'], aes_key=command).decrypt()
        return response2

    def get_buy_cpt_ifm(self, chapter_id) -> dict:
        data = {'chapter_id': chapter_id, }
        return self._post(point.CHAPTER_BUY, data)

    def get_book_by_tag(self, tag_name, page: int = 0, count: int = 15) -> dict:
        data = {'count': count, 'page': page, "tag": tag_name, 'type': 0}
        return self._post(point.BOOKCITY_GET_TAG_BOOK_LIST, data)

    def get_search(self, keyword, page=0, page_size=10) -> dict:
        data = {'count': page_size, 'page': page, 'category_index': '0', 'key': keyword}
        return self._post(point.BOOKCITY_GET_FILTER_LIST, data)

    def get_user_info(self) -> dict:
        return self._post(point.MY_DETAILS_INFO)

    def get_pson_prop_data(self) -> dict:
        return self._post(point.MY_PSON_PROP_DATA)

    def get_rank_list(self, time_type='week', count=10, page=0, order='fans_value') -> dict:
        data = {'time_type': time_type, 'count': count, 'page': page, 'order': order}
        return self._post(point.BOOKCITY_GET_RANK_lIST, data)

    def get_book_review_list(self, book_id, page=0, count=10, type_choice=1) -> dict:
        data = {'book_id': book_id, 'count': count, 'page': page, 'type': type_choice}
        return self._post(point.GET_REVIEW_LIST, data)

    def get_review_comment_list(self, review_id, page=0, count=10) -> dict:
        data = {'review_id': review_id, 'count': count, 'page': page}
        return self._post(point.GET_REVIEW_COMMENT_LIST, data)

    def get_bbs_comment_reply_list(self, comment_id, page=0, count=10) -> dict:
        data = {'comment_id': comment_id, 'count': count, 'page': page}
        return self._post(point.GET_REVIEW_COMMENT_REPLY_LIST, data)

    def get_money_fans_list(self, book_id, page=0, count=10) -> dict:
        data = {'book_id': book_id, 'count': count, 'page': page}
        return self._post(point.GET_MONEY_FANS_LIST, data)

    def get_discount_list(self) -> dict:
        data = {"theme_type": "NORMAL"}
        return self._post(point.BOOKCITY_DIS_DATA, data)

    def get_check_in_records(self) -> dict:
        return self._post(point.SIGN_RECORD, {})

    def do_check_in(self) -> dict:
        return self._post(point.SING_RECORD_TASK, {'task_type': 1})

    def get_version(self) -> dict:
        return self._post(point.MY_SETTING_UPDATE)

    def auto_sign(self) -> dict:
        data = {
            "oauth_type": "",
            "uuid": "android" + decode.generate_uuid(),
            "oauth_union_id": "",
            "gender": "1",
            "channel": "PCdownloadC",
            "oauth_open_id": ""
        }
        return self._post(point.SIGNUP_AUTO_REQ_V2, data)
