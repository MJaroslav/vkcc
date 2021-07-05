import subprocess
import shlex
import re
import os
from vkcc.settings import SETTINGS


__W3MIMGDISPLAY_PATHS__ = [
    '/usr/lib/w3m/w3mimgdisplay',
    '/usr/libexec/w3m/w3mimgdisplay',
    '/usr/lib64/w3m/w3mimgdisplay',
    '/usr/libexec64/w3m/w3mimgdisplay',
    '/usr/local/libexec/w3m/w3mimgdisplay',
]


def __find_w3mimgdisplay__():
    path = SETTINGS.get_w3mimgdisplay()
    if path:
        return path
    else:
        for path in __W3MIMGDISPLAY_PATHS__:
            if os.path.exists(path):
                return path


# def __run_w3mimgdisplay_process__():
#     runnable_path = __find_w3mimgdisplay__()
#     if runnable_path:
#         return subprocess.Popen([runnable_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
#                                 universal_newlines=True)


# W3MIMGDISPLAY_PROCESS = __run_w3mimgdisplay_process__()


# TODO: Make different render types
def draw_image(img, x, y, w, h, cx=-1, cy=-1, cw=-1, ch=-1):
    if not img:
        return  # TUI don't work normally if try render no image
    command = __find_w3mimgdisplay__()
    # if W3MIMGDISPLAY_PROCESS:
    if command:
        if x < 0 or y < 0:
            # _, _, ww, wh = get_window_size()
            ww, wh = get_window_size()
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
        # W3MIMGDISPLAY_PROCESS.stdin.write(args)
        # W3MIMGDISPLAY_PROCESS.stdin.flush()
        # W3MIMGDISPLAY_PROCESS.stdout.readline()
        subprocess.run([command], input=args.encode('utf-8'))


# TODO: Try to fix this with all terms
# def clear_image(x, y, w, h):
#     if W3MIMGDISPLAY_PROCESS:
#         if x < 0 or y < 0:
#             # _, _, ww, wh = get_window_size()
#             ww, wh = get_window_size()
#             if x < 0:
#                 x = ww - w + x
#             if y < 0:
#                 y = wh - h + y
#         ox, oy = SETTINGS.get_images_offset()
#         args = "6;{};{};{};{}\n4;\n3;\n".format(int(x + ox), int(y + oy), w, h)
#         W3MIMGDISPLAY_PROCESS.stdin.write(args)
#         W3MIMGDISPLAY_PROCESS.stdin.flush()
#         W3MIMGDISPLAY_PROCESS.stdout.readline()
#         # subprocess.run([command], input=args.encode('utf-8'))


# TODO: Try make this cross platform
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
    # w, h = os.get_terminal_size()
    # return w, h
    ch, cw = list(map(int, popen("stty size").split()))
    return cw, ch


def test():
    w, h = get_window_size()
    cw, ch = get_window_size_is_chars()
    return w / cw, h / ch


# TODO: Make more efficient method for finding font size
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

