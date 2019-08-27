# STERM, a serial communication terminal                                 #
# Copyright (C) 2013-2019  Ralf Stemmer (ralf.stemmer@gmx.net)           #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #

# Based on the config-module from MusicDB https://github.com/rstemmer/musicdb
"""
This module handles the reading of sterms configuration files in .ini-format.
The definition of names is shown in the ini file example below.

    .. code-block:: ini

        [section]
        option = value
"""

import configparser
from sterm.uart import UARTMode

class CONNECTION:
    pass
class TERMINAL:
    pass
class REMOTE:
    pass

class Config(configparser.ConfigParser):
    """
    Args:
        paths (list): List of possible config files, order defines priority. Last one hast highest.
    """

    def __init__(self, paths):
        super(Config, self).__init__()

        # Set default values
        self.connection = CONNECTION()
        self.connection.format      = "8N1"
        self.connection.baudrate    = 115200
        self.connection.device      = None

        self.terminal   = TERMINAL()
        self.terminal.echo          = True
        self.terminal.logfile       = None
        self.terminal.escape        = "\x1F"
        self.terminal.mode          = "text"

        self.remote     = REMOTE()
        self.remote.newline         = "\n"

        for path in paths:
            self.read(path)
            self.connection.format      = self.__Get(str,  "connection", "format",     self.connection.format)
            self.connection.baudrate    = self.__Get(int,  "connection", "baudrate",   self.connection.baudrate)
            self.connection.device      = self.__Get(str,  "connection", "device",     self.connection.device)
            self.terminal.echo          = self.__Get(bool, "terminal",   "echo",       self.terminal.echo)
            self.terminal.logfile       = self.__Get(str, "terminal",   "logfile",    self.terminal.logfile)
            self.terminal.escape        = self.__Get(str, "terminal",   "escape",     self.terminal.escape)
            self.terminal.mode          = self.__Get(str, "terminal",   "mode",       self.terminal.mode)
            self.remote.newline         = self.__Get(str, "remote",     "newline",    self.remote.newline)

        # TODO: Make this better: (make string to lower case and check if value is valid)
        if self.terminal.mode == "text":
            self.terminal.mode = UARTMode.TEXT
        else:
            self.terminal.mode = UARTMode.BINARY


  
    def __Get(self, datatype, section, option, fallback=None):
        """
        This method reads a value from the configuration.
        The values in the file are all stored as string.
        Using the *datatype* parameter will convert that string into a python data type.

        The *fallback* parameter can be used to define a value that shall be returned in case the option does not exist.
        This value can be of a different type than defined by the datatype parameter.

        Args:
            datatype: The data type of the value. This can be ``bool``, ``int``, ``float`` or ``str``.
            section (str): Name of the section to read from
            option (str): Name of the option to read
            fallback: Default value in case the option does not exist

        Returns:
            The value of an option
        """
  
        if not self.has_option(section, option):
            return fallback

        try:
            if datatype is bool:
                value = self.getboolean(section, option, fallback=fallback)
            elif datatype is int:
                value = self.getint(section, option, fallback=fallback)
            elif datatype is str:
                value = self.get(section, option, fallback=fallback)
            elif datatype is float:
                value = self.getfloat(section, option, fallback=fallback)
        except ValueError:
            return fallback
  
        return value
  
  

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

