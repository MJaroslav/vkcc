import npyscreen as nps
import vkcc.ui.wgformswitchbutton
from vkcc.config import translate


class MainForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = translate("button.exit.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def __init__(self, *args, **keywords):
        self.__login__ = None
        self.__settings__ = None
        super().__init__(name=translate("form.MAIN.title"), *args, **keywords)

    def create(self):
        self.__login__ = self.add(vkcc.ui.wgformswitchbutton.FormSwitchButton, form="LOGIN",
                                  name=translate("button.form.MAIN.login.title"))
        self.__settings__ = self.add(vkcc.ui.wgformswitchbutton.FormSwitchButton, rely=4, form="SETTINGS",
                                     name=translate("button.form.MAIN.settings.title"))

    def login_click(self):
        self.parentApp.setNextForm(None)

    def on_ok(self):
        self.parentApp.setNextForm(None)
