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

from __future__ import unicode_literals
from urwid import Text, WidgetWrap, Divider
from cloudinstall.ui.lists import SimpleList
from cloudinstall.ui.utils import Color, Padding


class HelpView(WidgetWrap):

    def __init__(self):
        help_text = [
            Padding.line_break(""),
            Text("OpenStack Installer - Help \u21C5 Scroll "
                 "(S) To go back to Status screen",
                 align="center"),
            Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}", 1, 1),
            Text("For full documentation, please refer to "
                 "https://help.ubuntu.com/lts/clouddocs/installer/"),
            Padding.line_break(""),
            Text("Bug reports can be filed at http://git.io/p7IF"),
            Padding.line_break(""),
            Color.header_title(Text("Command Reference")),
            Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}", 1, 1),
            Text("""
- Keyboard Shortcuts

  'A'   Add additional services to your cloud
  'S'   Shows the status view
  'Q'   Quit the application
  'R'   Refreshes current view
  'H'   Shows this help
            """),
            Color.header_title(Text("Overview")),
            Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}", 1, 1),
            Text("""
- Layout

  - Header
    The header shows a few common command keys for quick reference.

  - Main Table
    The main table has a row for each Juju service in the current environment,
    updated every ten seconds. Each row will contain a status icon indicator,
    agent state, ip address, machine type, and hardware specifications.

    There may also be an additional status field with information in the event
    of provisioning errors or additional status notifications.

  - Footer
    The footer displays a status message
            """),
            Color.header_title(Text("Actions")),
            Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}", 1, 1),
            Text("""

- Adding Services
  (A) brings up a dialog box for adding additional units. This is how to
  add compute units or a storage service. This dialog takes care of launching
  required dependencies, so for example, launching swift here will add a
  swift-proxy service and enough swift-storage nodes to meet the replica
  criterion (currently 3).
            """),
            Color.header_title(Text("Troubleshooting")),
            Divider("\N{BOX DRAWINGS LIGHT HORIZONTAL}", 1, 1),
            Text("""
The installation log can be found at:
  ~/.cloud-install/commands.log

Note: In a multi-install, MAAS may be unable to find machines that match the
default constraints set for one of the services the installer deploys. This
will be shown in the table under the service's heading, along with detail
about what those constraints were.
            """)]
        w = Padding.center_79(SimpleList(help_text))
        super().__init__(w)
