import json
import os

CONFIG_DIR = os.path.expanduser("~/.config/vkcc/")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

AUTH_FILE = os.path.join(CONFIG_DIR, "auth.json")

DEFAULT_CONFIGURATION = {
    "language": "english",
    "accounts": []
}


class Configuration(object):
    def __init__(self):
        self.__data__ = {}
        self.__load__()

    def __load__(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                self.__data__ = json.load(file)
        else:
            with open(CONFIG_FILE, "w") as file:
                json.dump(DEFAULT_CONFIGURATION, file, indent=4)
            self.__data__ = DEFAULT_CONFIGURATION

    def __get_option__(self, key, default=None):
        keys = key.split(".")
        data = self.__data__.copy()
        while len(keys) > 1:
            if keys[0] in data:
                data = data[keys[0]]
                del keys[0]
            else:
                return default
        return data[keys[0]] if keys[0] in data else default

    def get_profile(self):
        return self.__get_option__("profile")

    def get_option(self, key, default=None):
        return self.__get_option__("profiles.{}.{}".format(self.get_profile(), key), self.__get_option__(key, default))

    def get_w3mimgdisplay(self):
        return self.get_option("images.render.w3mimgdisplay.path")

    def get_render_method(self):
        return self.get_option("images.render.method")

    def get_images_offset(self):
        return self.get_option("images.offset.x", 0), self.get_option("images.offset.y", 0)

    def get_language(self):
        return self.get_option("language", "english")

    def get_accounts(self):
        return self.__data__["accounts"]

    def get_char_scale_size(self):
        return self.get_option("chars.width", -1), self.get_option("chars.height", -1)

    def add_account(self, user_id, name, token):
        account = {
            "id": user_id,
            "name": name,
            "access_token": token
        }
        # Just reset list without arg account
        self.__data__["accounts"] = [account for account in self.__data__["accounts"] if account["id"] != user_id]
        self.__data__["accounts"].append(account)
        self.save()

    def remove_account(self, acc):
        # Just reset list without arg account
        self.__data__["accounts"] = [account for account in self.__data__["accounts"] if account["id"] != acc["id"]]
        self.save()

    def save(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.__data__, file, indent=4)


configuration = Configuration()
