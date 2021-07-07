import npyscreen as nps
from vkcc.config import translate


class ConfirmCancelPopupTranslated(nps.utilNotify.ConfirmCancelPopup):
    OK_BUTTON_TEXT = translate("button.ok.title")
    CANCEL_BUTTON_TEXT = translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)


