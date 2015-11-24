#!/usr/bin/env python
#
# Copyright 2015 Canonical, Ltd.
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

import logging
import unittest
import urwid
from unittest.mock import MagicMock, patch
from cloudinstall.ev import EventLoop
from cloudinstall.config import Config
from cloudinstall.core import Controller
from tempfile import NamedTemporaryFile
log = logging.getLogger('cloudinstall.test_ev')


class EventLoopCoreTestCase(unittest.TestCase):

    def setUp(self):
        self._temp_conf = Config({}, save_backups=False)
        with NamedTemporaryFile(mode='w+', encoding='utf-8') as tempf:
            # Override config file to save to
            self.conf = Config(self._temp_conf._config, tempf.name,
                               save_backups=False)
        self.mock_ui = MagicMock(name='ui')
        self.mock_log = MagicMock(name='log')
        self.mock_loop = MagicMock(name='loop')
        EventLoop.config = self.conf

    @patch('cloudinstall.ev.EventLoop.run')
    def test_validate_loop(self, run):
        """ Validate eventloop runs """
        self.conf.setopt('headless', False)
        self.conf.setopt('openstack_release', 'kilo')
        dc = Controller(
            ui=self.mock_ui, config=self.conf)
        dc.initialize = MagicMock()
        dc.start()
        run.assert_called_once_with()

    @patch('cloudinstall.core.Controller.update_node_states')
    def test_validate_redraw_screen_commit_placement(self, update_node_states):
        """ Validate redraw_screen on commit_placement """
        self.conf.setopt('headless', False)
        dc = Controller(
            ui=self.mock_ui, config=self.conf)
        dc.initialize = MagicMock()
        dc.commit_placement()
        update_node_states.assert_called_once_with()

    @patch('cloudinstall.core.Controller.update_node_states')
    def test_validate_redraw_screen_enqueue(self, update_node_states):
        """ Validate update_node_states on enqueue_deployed_charms """
        self.conf.setopt('headless', False)
        dc = Controller(
            ui=self.mock_ui, config=self.conf)
        dc.initialize = MagicMock()
        dc.enqueue_deployed_charms()
        update_node_states.assert_called_once_with()

    def test_validate_exit(self):
        """ Validate error code set with eventloop """
        dc = Controller(
            ui=self.mock_ui, config=self.conf)
        dc.initialize = MagicMock()
        with self.assertRaises(urwid.ExitMainLoop):
            EventLoop.exit(1)
        self.assertEqual(EventLoop.error_code, 1)

    def test_validate_exit_no_ev(self):
        """ Validate SystemExit with no eventloop """
        self.conf.setopt('headless', True)
        dc = Controller(
            ui=self.mock_ui, config=self.conf)
        dc.initialize = MagicMock()
        with self.assertRaises(SystemExit) as cm:
            EventLoop.exit(1)
        exc = cm.exception
        self.assertEqual(EventLoop.error_code, exc.code, "Found loop")
