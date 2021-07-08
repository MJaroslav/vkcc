import npyscreen as nps
from vkcc.config import translate
from vkcc.ui.vk.fmVKBase import VKFormBase


class VKMessagesForm(VKFormBase):
    def __init__(self, *args, **keywords):
        super().__init__(name=translate("form.MESSAGES.title"), *args, **keywords)

    def _vk_create(self):
        nps.TitleText

    def beforeEditing(self):
        super().beforeEditing()

