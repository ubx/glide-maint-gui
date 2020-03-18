import urwid
import json
import subprocess

XCSOAR = 'xcsoar'
CAN_VIEWER = 'can.viewer'


class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker
                                ([urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
                                  urwid.AttrMap(line, 'line'),
                                  urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        top.open_box(self.menu)


class Choice(urwid.WidgetWrap):
    def __init__(self, caption, key=None):
        self.key = key
        super().__init__(MenuButton(caption, self.item_chosen))
        self.caption = caption

    def item_chosen(self, button):
        run_program(self.key)
        mainloop.screen.clear()


def run_program(key):
    if key is XCSOAR:
        subprocess.call(config[XCSOAR]['run'])
    elif key is CAN_VIEWER:
        subprocess.run(
            config[CAN_VIEWER]['run'] + ['-i'] + [config['canbus']['interface']]
            + ['-c'] + [config['canbus']['channel']])


menu_top = SubMenu(u'Main Menu', [
    Choice(u'Run XCSoar', key=XCSOAR),
    Choice(u'CAN Player', key=CAN_VIEWER),
])

palette = [
    (None, 'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super().__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
                              self.options('given', 24)))
        self.focus_position = len(self.contents) - 1


def show_or_exit(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


with open('config.json', 'r') as read_file:
    config = json.load(read_file)

top = HorizontalBoxes()
top.open_box(menu_top.menu)
mainloop = urwid.MainLoop(urwid.Filler(top, 'top', 10), palette, unhandled_input=show_or_exit)
mainloop.run()
