import npyscreen as nps
import curses


class SplitVerticalForm(nps.Form):
    MOVE_LINE_ON_RESIZE = False
    """Just the same as the SplitForm, but with a vertical line"""

    def __init__(self, draw_line_at=None, *args, **keywords):
        super(SplitVerticalForm, self).__init__(*args, **keywords)
        if not hasattr(self, 'draw_line_at'):
            if draw_line_at is not None:
                self.draw_line_at = draw_line_at
            else:
                self.draw_line_at = self.get_half_way()

    def draw_form(self, ):
        MAXY, MAXX = self.curses_pad.getmaxyx()
        super(SplitVerticalForm, self).draw_form()
        self.curses_pad.vline(1, self.normalize_line_pos(), curses.ACS_VLINE, MAXY - 2)
        # self.curses_pad.hline(self.draw_line_at, 1, curses.ACS_HLINE, MAXX - 2)

    def normalize_line_pos(self):
        if self.draw_line_at < 0:
            return self.curses_pad.getmaxyx()[1] + self.draw_line_at
        else:
            return self.draw_line_at

    def get_half_way(self):
        return self.curses_pad.getmaxyx()[1] // 2

    def resize(self):
        super(SplitVerticalForm, self).resize()
        if self.MOVE_LINE_ON_RESIZE:
            self.draw_line_at = self.get_half_way()
