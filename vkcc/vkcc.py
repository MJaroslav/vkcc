import npyscreen as nps
import vkcc.utils as utils
import vkcc.localization as l10n
from vkcc.vk import VK
from vkcc.settings import SETTINGS
import curses


class App(nps.StandardApp):
    def onStart(self):
        nps.setTheme(nps.Themes.TransparentThemeLightText)
        self.addForm("MAIN", MainForm, name=l10n.translate("form.MAIN.title"))
        self.addForm("LOGIN_NEW", LoginNewForm, name=l10n.translate("form.LOGIN_NEW.title"))
        self.addForm("LOGIN", LoginForm, name=l10n.translate("form.LOGIN.title"))

    # def onCleanExit(self):
    #     if utils.W3MIMGDISPLAY_PROCESS:
    #         utils.W3MIMGDISPLAY_PROCESS.kill()


class ConfirmCancelPopupTranslated(nps.utilNotify.ConfirmCancelPopup):
    OK_BUTTON_TEXT = l10n.translate("button.ok.title")
    CANCEL_BUTTON_TEXT = l10n.translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)


def notify_auth_handler():
    f = ConfirmCancelPopupTranslated(name=l10n.translate("popup.TWO_AUTH.title"), color='STANDOUT')
    f.preserve_selected_widget = True

    code = f.add(nps.TitleText, name=l10n.translate("titletext.popup.TWO_AUTH.code.title"))
    remember = f.add(nps.Checkbox, name=l10n.translate("checkbox.popup.TWO_AUTH.remember.title"))

    f.editw = 0
    f.edit()

    return code.value, remember.value


def draw_border_with_title(widget):
    HEIGHT = widget.height - 1
    WIDTH = widget.width - 1

    widget.parent.curses_pad.hline(widget.rely, widget.relx, curses.ACS_HLINE, WIDTH)
    widget.parent.curses_pad.hline(widget.rely + HEIGHT, widget.relx, curses.ACS_HLINE, WIDTH)
    widget.parent.curses_pad.vline(widget.rely, widget.relx, curses.ACS_VLINE, widget.height)
    widget.parent.curses_pad.vline(widget.rely, widget.relx + WIDTH, curses.ACS_VLINE, HEIGHT)

    widget.parent.curses_pad.addch(widget.rely, widget.relx, curses.ACS_ULCORNER, )
    widget.parent.curses_pad.addch(widget.rely, widget.relx + WIDTH, curses.ACS_URCORNER, )
    widget.parent.curses_pad.addch(widget.rely + HEIGHT, widget.relx, curses.ACS_LLCORNER, )
    widget.parent.curses_pad.addch(widget.rely + HEIGHT, widget.relx + WIDTH, curses.ACS_LRCORNER, )

    if widget.name:
        if isinstance(widget.name, bytes):
            name = widget.name.decode(widget.encoding, 'replace')
        else:
            name = widget.name
        name = widget.safe_string(name)
        name = " " + name + " "
        if isinstance(name, bytes):
            name = name.decode(widget.encoding, 'replace')
        name_attributes = curses.A_NORMAL
        if widget.do_colors() and not widget.editing:
            name_attributes = name_attributes | widget.parent.theme_manager.findPair(widget, widget.color)  # | curses.A_BOLD
        elif widget.editing:
            name_attributes = name_attributes | widget.parent.theme_manager.findPair(widget, 'HILIGHT')
        else:
            name_attributes = name_attributes  # | curses.A_BOLD

        if widget.editing:
            name_attributes = name_attributes | curses.A_BOLD

        widget.add_line(widget.rely, widget.relx + 4, name,
                        widget.make_attributes_list(name, name_attributes),
                        widget.width - 8)


class ImageWidget(nps.wgwidget.Widget):
    def __init__(self, screen, img=None, autohide=False, border=False, name=None, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.__img__ = img
        self.name = name
        self.__saved_name__ = name
        if autohide:
            self.hidden = not self.__img__ or ("hidden" in keywords and keywords["hidden"])
        self.autohide = autohide
        self.border = border
        self.errored = False

    def set_img(self, img, errored=False):
        self.errored = errored
        self.__img__ = img
        if self.autohide:
            self.hidden = not self.__img__
        if self.border and not self.hidden:
            if self.__img__:
                self.name = self.__saved_name__
            elif self.errored:
                self.name = l10n.translate("img.no.title")
            else:
                self.name = self.__saved_name__
        self.update()

    def clear(self, usechar=' '):
        super().clear('X')
        self.parent.refresh()
        super().clear(usechar)
        if self.border and not self.hidden:
            draw_border_with_title(self)
        # x = self.relx
        # y = self.rely
        # w = self.width
        # h = self.height
        # x, y = utils.scale_by_char(x, y)
        # w, h = utils.scale_by_char(w, h)
        # utils.clear_image(x, y, w, h)

    def display(self):
        super().display()
        if self.hidden:
            self.__clear_image__()
        else:
            self.__draw_image__()

    def __draw_image__(self):
        x = self.relx
        y = self.rely
        w = self.width
        h = self.height
        if self.border:
            x += 1
            y += 1
            w -= 2
            h -= 2
        x, y = utils.scale_by_char(x, y)
        w, h = utils.scale_by_char(w, h)
        draw_border_with_title(self)
        utils.draw_image(self.__img__, x, y, w, h)

    def __clear_image__(self):
        self.clear('X')
        self.parent.refresh()
        self.clear()

    def update(self, clear=True):
        draw_border_with_title(self)


class FormButton(nps.ButtonPress):
    def __init__(self, screen, form=None, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        if self.name:
            self.name += ".."
        self.__form__ = form

    def whenPressed(self):
        if self.__form__:
            self.find_parent_app().switchForm(self.__form__)


class AccountButton(FormButton):
    def __init__(self, screen, account, form=None, *args, **keywords):
        super().__init__(screen, form, *args, **keywords)
        self.account = account

    def _pre_edit(self):
        super()._pre_edit()
        self.parent.set_account(self.account)

    def _post_edit(self):
        super()._post_edit()
        self.parent.set_account(None)

    def whenPressed(self):
        if VK.login_by_token(self.account):
            super().whenPressed()


class MainForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = l10n.translate("button.exit.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def create(self):
        self.login = self.add(FormButton, form="LOGIN", name=l10n.translate("button.form.MAIN.login.title"))
        self.settings = self.add(FormButton, rely=4, form="SETTINGS", name=l10n.translate("button.form.MAIN.settings.title"))

    def login_click(self):
        self.parentApp.setNextForm(None)

    def on_ok(self):
        self.parentApp.setNextForm(None)


class LoginForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = l10n.translate("button.back.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False
    _accounts_ = []

    def afterEditing(self):
        self.avatar.set_img(None)
        self.login_as.value = None
        self.accounts.reset()

    def create(self):
        self.add(FormButton, form="LOGIN_NEW", name=l10n.translate("button.form.LOGIN.login_new.title"))
        # i = 0
        # for account in SETTINGS.get_accounts():
        #     self.add(AccountButton, rely=4 + i, form=None, account=account, name=account["name"])
        #     i += 1
        # self.accounts.reload_values()
        self.accounts = self.add(AccountsBox, contained_widget_arguments={"slow_scroll": True}, rely=4, scroll_exit=True, width=57, max_width=-18, name=l10n.translate("box.form.LOGIN.accounts.title"))
        self.avatar = self.add(ImageWidget, rely=1, relx=-21, editable=False, name=l10n.translate("img.form.LOGIN.avatar.title"), border=True, width=20, height=10)
        self.login_as = self.add(nps.FixedText, rely=11, relx=-20, hidden=True, editable=False)
        self.login = self.add(FormButton, rely=13, relx=-20, hidden=True, name=l10n.translate("button.form.LOGIN.login.title"))

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def set_account(self, account):
        if account:
            avatar = VK.get_avatar(account["id"], size="large")
            self.avatar.set_img(avatar, True)
        else:
            self.avatar.set_img(None)
        self.avatar.display()
        self.login_as.value = account["name"] if account else None
        self.login_as.hidden = not self.login_as.value
        self.login_as.display()
        self.login.hidden = not self.login_as.value
        self.login.display()


class AccountSelect(nps.SelectOne):
    def h_select(self, ch):
        super().h_select(ch)
        index = self.cursor_line
        account = SETTINGS.get_accounts()[index]
        self.parent.set_account(account)


class AccountsBox(nps.BoxTitle):
    _contained_widget = AccountSelect

    def update(self, clear=True):
        self.entry_widget.values = list(map(lambda account: account["name"], SETTINGS.get_accounts()))
        super().update(clear)

    def reset(self):
        self.entry_widget.value = None


class LoginNewForm(nps.ActionForm):
    OK_BUTTON_TEXT = l10n.translate("button.ok.title")
    CANCEL_BUTTON_TEXT = l10n.translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def afterEditing(self):
        self.login.value = None
        self.password.value = None
        self.remember.value = False

    def create(self):
        self.login = self.add(nps.TitleText, name=l10n.translate("titletext.form.LOGIN_NEW.login.title"))
        self.password = self.add(nps.TitlePassword, name=l10n.translate("titlepassword.form.LOGIN_NEW.password.title"))
        self.remember = self.add(nps.Checkbox, name=l10n.translate("checkbox.form.LOGIN_NEW.remember.title"))

    def on_ok(self):
        result = VK.login_by_pass(self.login.value, self.password.value, notify_auth_handler, self.remember.value)
        if result:
            self.parentApp.switchFormPrevious()
            self.parentApp.getForm("LOGIN").reload_accounts()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class ProfileForm(nps.ActionForm):
    def create(self):
        pass

    def display(self, clear=True):
        super().display(clear)

    def on_ok(self):
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")
