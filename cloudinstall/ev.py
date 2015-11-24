# Copyright 2014, 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urwid
import sys
import asyncio
from cloudinstall.ui.palette import STYLES

import logging

log = logging.getLogger('cloudinstall.ev')


class EventLoop:

    """ Abstracts out event loop
    """
    loop = None
    config = None
    error_code = 0

    @classmethod
    def build_loop(cls, ui, config, **kwargs):
        """ Returns event loop configured with color palette """
        cls.config = config

        if not cls.config.getopt('headless'):
            additional_opts = {
                'screen': urwid.raw_display.Screen(),
                'handle_mouse': True
            }
            additional_opts['screen'].set_terminal_properties(colors=256)
            additional_opts['screen'].reset_default_terminal_palette()
            additional_opts.update(**kwargs)
            evl = asyncio.get_event_loop()
            cls.loop = urwid.MainLoop(
                ui, STYLES,
                event_loop=urwid.AsyncioEventLoop(loop=evl), **additional_opts)

    @classmethod
    def exit(cls, err=0):
        cls.error_code = err
        log.info("Stopping eventloop")
        if cls.config.getopt('headless'):
            sys.exit(err)

        raise urwid.ExitMainLoop()

    @classmethod
    def redraw_screen(cls):
        if not cls.config.getopt('headless'):
            try:
                cls.loop.draw_screen()
            except AssertionError as e:
                log.exception("exception failure in redraw_screen")
                raise e

    @classmethod
    def set_alarm_in(cls, interval, cb):
        if not cls.config.getopt('headless'):
            return cls.loop.set_alarm_in(interval, cb)
        return

    @classmethod
    def remove_alarm(cls, handle):
        if not cls.config.getopt('headless'):
            return cls.loop.remove_alarm(handle)
        return False

    @classmethod
    def run(cls, cb=None):
        """ Run eventloop

        :param func cb: (optional) callback
        """
        if not cls.config.getopt('headless'):
            try:
                cls.loop.run()
            except:
                log.exception("Exception in ev.run():")
                raise
        return
