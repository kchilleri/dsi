"""Environment Plugin drivers.

A home for environment plugin parsers.
"""

from collections import OrderedDict
import os
import socket

from dsi.plugins.structured_metadata_plugin import Plugin

class EnvPlugin(Plugin):

    def __init__(self, path=None) -> None:
        """Load valid environment plugin file.

        Environment plugin files assume a POSIX-compliant
        filesystem and always collect UID/GID information.
        """
        # Get POSIX info
        self.posix_info = OrderedDict()
        self.posix_info['uid'] = os.getuid()
        self.posix_info['effective_gid'] = os.getgid()
        egid = self.posix_info['effective_gid']
        self.posix_info['moniker'] = os.getlogin()
        moniker = self.posix_info['moniker']
        self.posix_info['gid_list'] = os.getgrouplist(moniker, egid)
        # Plugin output collector
        self.output_collector = OrderedDict()
        # class bool to track whether header has been written.
        self.header_exist = False
        # Once we start writing structured data, the column count is fixed
        self.column_cnt = None
        
class HostnamePlugin(EnvPlugin):
    """An example Plugin implementation.

    This plugin collects the hostname of the machine,
    the UID and effective GID of the plugin collector, and
    the Unix time of the collected information.
    """

    def __init__(self) -> None:
        """Load valid environment plugin file.

        Environment plugin files assume a POSIX-compliant
        filesystem and always collect UID/GID information.
        """
        super().__init__()

    def pack_header(self) -> None:
        for key in self.posix_info:
            self.output_collector[key] = []
        self.output_collector['hostname'] = []
        self.column_cnt = len(self.output_collector.keys())

    def add_row(self) -> None:
        if not self.header_exist:
            self.pack_header()
            self.header_exist = True
        row = list(self.posix_info.values()) + [socket.gethostname()]
        for key,row_elem in zip(self.output_collector, row):
            self.output_collector[key].append(row_elem) 
