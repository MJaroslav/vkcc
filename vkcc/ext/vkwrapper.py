from vk_api import VkApi
from vkcc.config import accounts
from vkcc.config.configuration import CONFIG_DIR
import shutil
import os
import requests


IMAGE_CACHE_DIR = os.path.expanduser("~/.cache/vkcc/")
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)

AUTH_API_LIB_FILE = os.path.join(CONFIG_DIR, "auth_vk_api_lib.json")


class VKWrapper(object):
    def __init__(self):
        self.__session__ = None
        self.__api__ = None
        self.__user__ = None
        self.__user_id__ = None
        self.__user_name__ = None

    @staticmethod
    def clear_cache():
        for filename in os.listdir(IMAGE_CACHE_DIR):
            file_path = os.path.join(IMAGE_CACHE_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s".format(file_path, e))

    def login_by_token(self, account):
        self.__session__ = VkApi(token=account["access_token"], config_filename=AUTH_API_LIB_FILE)
        if self.__session__._check_token():
            self.__api__ = self.__session__.get_api()
            self.__user__ = self.__api__.users.get(fields="domain")[0]
            self.__user_id__ = self.__user__["id"]
            self.__user_name__ = self.__user__["first_name"] + " " + self.__user__["last_name"]
            self.get_avatar(self.__user_id__, "large", True)
            return True
        else:
            return False

    def login_by_pass(self, login, password, auth_handler, save):
        self.__session__ = VkApi(login=login, password=password, auth_handler=auth_handler,
                                 config_filename=AUTH_API_LIB_FILE)
        self.__session__.auth(token_only=True)
        if self.__session__._check_token():
            self.__api__ = self.__session__.get_api()
            self.__user__ = self.__api__.users.get(fields="domain")[0]
            self.__user_id__ = self.__user__["id"]
            self.__user_name__ = self.__user__["first_name"] + " " + self.__user__["last_name"]
            if save:
                accounts.add(self.__user_id__, self.__user_name__, self.__session__.token["access_token"])
                self.get_avatar(self.__user_id__, "large", True)
                return {
                    "name": self.__user_name__,
                    "access_token": self.__session__.token["access_token"],
                    "id": self.__user_id__
                }
            return True
        else:
            return False

    def get_avatar(self, user_id, size, update=False):
        filename = IMAGE_CACHE_DIR + str(user_id) + "_avatar_" + size + ".jpg"
        if not update and os.path.exists(filename):
            return filename
        else:
            if size == "small":
                fields = "photo_50"
            elif size == "medium":
                fields = "photo_100"
            else:
                fields = "photo_200"
            if self.__api__:
                url = self.__api__.users.get(ids=user_id, fields=fields)[0][fields]
                if url:
                    r = requests.get(url, allow_redirects=True)
                    with open(filename, "wb") as file:
                        file.write(r.content)
                    return filename

    def get_photo(self, photo, size_type, update=False):
        filename = IMAGE_CACHE_DIR + photo + "_" + size_type + ".jpg"
        if not update and os.path.exists(filename):
            return filename
        else:
            sizes = self.__api__.photos.getById(photos=photo, photo_sizes=1)[0]["sizes"]
            url = None
            for size in sizes:
                if size["type"] == size_type:
                    url = size["url"]
                    break
            if url:
                r = requests.get(url, allow_redirects=True)
                with open(filename, "wb") as file:
                    file.write(r.content)
                return filename

    def api(self):
        return self.__api__


VK = VKWrapper()
