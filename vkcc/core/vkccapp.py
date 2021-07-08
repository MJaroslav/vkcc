from vkcc.core import *
import npyscreen as nps
from vkcc.ui.fmMain import MainForm
from vkcc.ui.fmLogin import LoginForm
from vkcc.ui.fmLoginNew import LoginNewForm
from vkcc.ui.fmSettings import SettingsForm
import vkcc.ext


class VKCCApp(nps.StandardApp):
    def onStart(self):
        nps.setTheme(nps.Themes.TransparentThemeLightText)
        self.addForm(FORM_MAIN, MainForm)
        self.addForm(FORM_LOGIN, LoginForm)
        self.addForm(FORM_LOGIN_NEW, LoginNewForm)
        self.addForm(FORM_SETTINGS, SettingsForm)

    def onCleanExit(self):
        vkcc.ext.get_render_method().dispose()

    def has_form(self, fmid):
        return fmid in self._Forms
