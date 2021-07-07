import npyscreen as nps
from vkcc.config import translate
from vkcc.ext import get_render_method


class ConfirmCancelPopupTranslated(nps.utilNotify.ConfirmCancelPopup):
    OK_BUTTON_TEXT = translate("button.ok.title")
    CANCEL_BUTTON_TEXT = translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)


class YesNoPopupTranslated(nps.utilNotify.YesNoPopup):
    OK_BUTTON_TEXT = translate("button.yes.title")
    CANCEL_BUTTON_TEXT = translate("button.no.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)


def notify_ok_cancel_translated(message, title=translate("popup.DEFAULT.title"), form_color='STANDOUT', wrap=True,
                                editw=0,):
    get_render_method().clear_all()
    message = nps.utilNotify._prepare_message(message)
    f = ConfirmCancelPopupTranslated(name=title, color=form_color)
    f.preserve_selected_widget = True
    mlw = f.add(nps.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = nps.utilNotify._wrap_message_lines(message, mlw_width)
    mlw.values = message
    f.editw = editw
    f.edit()
    return f.value


def notify_yes_no_translated(message, title=translate("popup.DEFAULT.title"), form_color='STANDOUT', wrap=True,
                                editw=0,):
    get_render_method().clear_all()
    message = nps.utilNotify._prepare_message(message)
    f = YesNoPopupTranslated(name=title, color=form_color)
    f.preserve_selected_widget = True
    mlw = f.add(nps.Pager,)
    mlw_width = mlw.width-1
    if wrap:
        message = nps.utilNotify._wrap_message_lines(message, mlw_width)
    mlw.values = message
    f.editw = editw
    f.edit()
    return f.value
