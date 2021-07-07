# TODO: Try do borders by Box wrapping, don't by this function
# import curses
# def draw_border_with_title(widget):
#     HEIGHT = widget.height - 1
#     WIDTH = widget.width - 1
#
#     widget.parent.curses_pad.hline(widget.rely, widget.relx, curses.ACS_HLINE, WIDTH)
#     widget.parent.curses_pad.hline(widget.rely + HEIGHT, widget.relx, curses.ACS_HLINE, WIDTH)
#     widget.parent.curses_pad.vline(widget.rely, widget.relx, curses.ACS_VLINE, widget.height)
#     widget.parent.curses_pad.vline(widget.rely, widget.relx + WIDTH, curses.ACS_VLINE, HEIGHT)
#
#     widget.parent.curses_pad.addch(widget.rely, widget.relx, curses.ACS_ULCORNER, )
#     widget.parent.curses_pad.addch(widget.rely, widget.relx + WIDTH, curses.ACS_URCORNER, )
#     widget.parent.curses_pad.addch(widget.rely + HEIGHT, widget.relx, curses.ACS_LLCORNER, )
#     widget.parent.curses_pad.addch(widget.rely + HEIGHT, widget.relx + WIDTH, curses.ACS_LRCORNER, )
#
#     if widget.name:
#         if isinstance(widget.name, bytes):
#             name = widget.name.decode(widget.encoding, 'replace')
#         else:
#             name = widget.name
#         name = widget.safe_string(name)
#         name = " " + name + " "
#         if isinstance(name, bytes):
#             name = name.decode(widget.encoding, 'replace')
#         name_attributes = curses.A_NORMAL
#         if widget.do_colors() and not widget.editing:
#             name_attributes = name_attributes | widget.parent.theme_manager.findPair(widget, widget.color)  # | curses.A_BOLD
#         elif widget.editing:
#             name_attributes = name_attributes | widget.parent.theme_manager.findPair(widget, 'HILIGHT')
#         else:
#             name_attributes = name_attributes  # | curses.A_BOLD
#
#         if widget.editing:
#             name_attributes = name_attributes | curses.A_BOLD
#
#         widget.add_line(widget.rely, widget.relx + 4, name,
#                         widget.make_attributes_list(name, name_attributes),
#                         widget.width - 8)

