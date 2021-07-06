import json
import os

DEFAULT_OPTIONS = {
    "profiles": {
        "mate-terminal": {
            "images": {
                "offset": {
                    "x": 0,
                    "y": 13
                }
            }
        }
    },
    "profile": "",
    "language": "english",
    "images": {
        "w3mimgdisplay": "",
        "offset": {
            "x": 0,
            "y": 0
        }
    },
    "accounts": []
}


class Settings(object):
    def __init__(self):
        self.__data__ = {}
        self.__config_dir__ = os.path.expanduser("~/.config/")
        if not os.path.exists(self.__config_dir__):
            os.makedirs(self.__config_dir__)
        self.__settings_file__ = self.__config_dir__ + "vkcc"
        self.__load__()

    def __load__(self):
        if os.path.exists(self.__settings_file__):
            with open(self.__settings_file__, "r") as file:
                self.__data__ = json.load(file)
        else:
            with open(self.__settings_file__, "w") as file:
                json.dump(DEFAULT_OPTIONS, file, indent=4)
            self.__data__ = DEFAULT_OPTIONS

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
        return self.get_option("images.w3mimgdisplay")

    def get_render_method(self):
        return self.get_option("images.render_method")

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
        self.__data__["accounts"].append(account)
        self.save()

    def save(self):
        with open(self.__settings_file__, "w") as file:
            json.dump(self.__data__, file, indent=4)


SETTINGS = Settings()
