import subprocess
import shlex
import re
from vkcc.settings import SETTINGS


def draw_image(img, x, y, w, h, cx=-1, cy=-1, cw=-1, ch=-1):
    if img:
        command = SETTINGS.get_w3mimgdisplay()
        if command:
            if x < 0 or y < 0:
                _, _, ww, wh = get_window_size()
                if x < 0:
                    x = ww - w + x
                if y < 0:
                    y = wh - h + y
            ox, oy = SETTINGS.get_images_offset()
            if cx < 0:
                cx = ""
            if cy < 0:
                cy = ""
            if cw < 0:
                cw = ""
            if ch < 0:
                ch = ""
            args = "0;1;{};{};{};{};{};{};{};{};{}\n4;\n3;".format(int(x + ox), int(y + oy), w, h, cx, cy, cw, ch, img)
            subprocess.run([command], input=args.encode('utf-8'))


def get_window_size():
    window = popen(r'xdotool getactivewindow')
    command = r'xwininfo -id ' + window
    out = popen(command)
    # ox = re.findall(r'\n +Absolute upper-left X: +([0-9]+).*\n', out)[0]
    # oy = re.findall(r'\n +Absolute upper-left Y: +([0-9]+).*\n', out)[0]
    w = re.findall(r'\n +Width: +([0-9]+).*\n', out)[0]
    h = re.findall(r'\n +Height: +([0-9]+).*\n', out)[0]
    # return list(map(int, (ox, oy, w, h)))
    return list(map(int, (w, h)))


def get_window_size_is_chars():
    ch, cw = list(map(int, popen("stty size").split()))
    return cw, ch


def test():
    w, h = get_window_size()
    cw, ch = get_window_size_is_chars()
    return w / cw, h / ch


def scale_by_char(x, y):
    w, h = get_window_size()
    ox, oy = SETTINGS.get_images_offset()
    w -= ox
    h -= oy
    cw, ch = get_window_size_is_chars()
    sx, sy = list(map(int, (w / cw, h / ch)))
    osx, osy = SETTINGS.get_char_scale_size()
    if not osx < 0:
        sx = osx
    if not osy < 0:
        sy = osy
    return list(map(int, (x * sx, y * sy)))


def popen(command, shell=False):
    stdout, stderr = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell).communicate()
    return stdout.decode("utf-8").strip()

