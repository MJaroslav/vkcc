import npyscreen as nps
from vkcc.config import translate
from vkcc.ext import VK
from vkcc.ui.wgimage import Image
from vkcc.ext.vkwrapper import SIZE_AVATAR_SMALL
from vkcc.ui.fmSplitVerticalForm import SplitVerticalForm
from vkcc.ui.wgformswitchbutton import FormSwitchButton
from vkcc.core import *


class VKFormBase(nps.ActionFormMinimal, SplitVerticalForm):
    OK_BUTTON_TEXT = translate("button.exit.title")

    def __init__(self, *args, **keywords):
        self.__avatar__ = None
        self.__user_name__ = None
        self.__id__ = None
        super().__init__(draw_line_at=-22, *args, **keywords)

    def _vk_create(self):
        pass

    def create(self):
        self._vk_create()
        self.__id__ = self.add(nps.FixedText, rely=2, relx=-20, editable=False)
        self.__avatar__ = self.add(Image, rely=1, relx=-7, width=4, height=2)
        self.__user_name__ = self.add(nps.FixedText, rely=4, relx=-20, editable=False)

        self.add(FormSwitchButton, form=FORM_VK_FEED, name=translate("button.form.VK.feed.title"), rely=6, relx=-20)
        self.add(FormSwitchButton, form=FORM_VK_MESSAGES, name=translate("button.form.VK.messages.title"), rely=7,
                 relx=-20)
        self.add(FormSwitchButton, form=FORM_VK_FRIENDS, name=translate("button.form.VK.friends.title"), rely=8,
                 relx=-20)
        self.add(FormSwitchButton, form=FORM_VK_GROUPS, name=translate("button.form.VK.groups.title"), rely=9, relx=-20)

    def beforeEditing(self):
        self.__id__.value = "@" + VK.get_self_domain()
        self.__avatar__.set_image(VK.get_self_avatar(SIZE_AVATAR_SMALL))
        self.__user_name__.value = VK.get_self_name()

    def afterEditing(self):
        self.__avatar__.set_image(None)

    def on_ok(self):
        VK.logout()
        self.parentApp.switchForm(FORM_LOGIN)


class VKFeedForm(VKFormBase):
    def __init__(self, *args, **keywords):
        super().__init__(name=translate("form.FEED.title"), *args, **keywords)


# TODO: Dummies
class VKFriendsForm(VKFormBase):
    pass


class VKGroupsForm(VKFormBase):
    pass
