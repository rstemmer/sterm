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

import sys
import binascii
from enum import Enum
from serial import *



class UARTMode(Enum):
    BINARY  = 1
    TEXT    = 2

# Mapping the format-string (--format) to the pyserial-parameters.
# This is just a subset of possible parameters. See pyserial-docs to extend these maps.
BYTESIZEMAP = {}
BYTESIZEMAP["5"] = FIVEBITS
BYTESIZEMAP["6"] = SIXBITS
BYTESIZEMAP["7"] = SEVENBITS
BYTESIZEMAP["8"] = EIGHTBITS
PARITYMAP = {}
PARITYMAP["N"] = PARITY_NONE
PARITYMAP["E"] = PARITY_EVEN
PARITYMAP["O"] = PARITY_ODD
STOPBITMAP = {}
STOPBITMAP["1"] = STOPBITS_ONE
STOPBITMAP["2"] = STOPBITS_TWO

# TODO:
# Automatic disconnect
# Support with-environment
# TODO: support path-type for devpath and logpath
# TODO: logfile currently only stores received information, not entered data

# TODO: Improve documentation:
#  - Describe format string (dataformat)
#  - Describe logging in detail
#  - Describe uart modes in detail
class UART(object):
    """
    This class manages the connection to a UART device.

    When creating an object, the connection gets automatically established.

    Whenever an exception occurs, it gets passed through.
    This class does not do any output to *stdout* or *stderr*.

    Args:
        devpath (str): Path to the UART device (like ``"/dev/ttyUSB0"``)
        baudrate (int): Baud rate used for the data transfer
        dataformat (str): The three-letter format string of defining the type of data. (like ``"8N1"``)
        uartmode (UARTMode): Definition if the methods work in *binary mode* or *text mode* (UTF-8)
        logpath (str): Write all received data into the given log file

    Raises:
        ValueError: When the format string is not following the specified scheme
    """
    def __init__(self, devpath, baudrate, dataformat, *, uartmode=UARTMode.TEXT, logpath=None):
        self.devpath    = devpath
        self.baudrate   = baudrate
        self.uartmode   = uartmode
        self.logpath    = logpath

        # Set some defaults - will be updated by calling __Connect
        self.logfile    = None
        self.uart       = None

        # Translate format-string
        try:
            self.bytesize = BYTESIZEMAP[dataformat[0]]
            self.parity   = PARITYMAP  [dataformat[1]]
            self.stopbits = STOPBITMAP [dataformat[2]]
        except KeyError as e:
            raise ValueError("dataformat argument (\"%s\") invalid! See documentation for valid formats.", dataformat)
        self.__Connect()



    def __Connect(self):
        """
        This method opens a connection to a UART device.

        If logging is enabled, the log files gets opened as well.
        In *binary mode* the files gets opened to append binary data (``"ab"``), otherwise
        it is opened to append text data (``"at"``).

        In case an expection raises, an error message gets printed to *stderr* and then the
        exception gets raised again.

        Returns:
            *Nothing*

        Raises:
            SerialException: In case the device can not be found or can not be configured.
            ValueError: When the UART configuration is out of valid range
            IOError: In case there is some trouble opening the log file
        """
        # Open remote terminal device
        self.uart = Serial(
            port    = self.devpath,
            baudrate= self.baudrate,
            bytesize= self.bytesize,
            parity  = self.parity,
            stopbits= self.stopbits,
            timeout = 0.1,
            interCharTimeout=None
        )

        # open log file
        if type(self.logpath) is str:
            if self.uartmode == UARTMode.BINARY:
                filemode = "ab" # append to binary file
            else:
                filemode = "at" # append to text file

            self.logfile = open(self.logpath, filemode)
        return



    def Disconnect(self):
        """
        This method closes the connection to the UART device.
        If a logging is enabled, the log files gets closed as well.

        Returns:
            *Nothing*
        """
        self.uart.close()
        if self.logfile:
            self.logfile.close()
        return



    def Receive(self):
        """
        This function reads all data from the serial input buffer that is available.
        The read data then gets interpreted and returned.
        The function is non-blocking since it only gets the data that is in the device's buffers,
        but it does not wait for new data.

        The way the data is interpreted depends on the UART mode set in the constructor.

        In *binary mode* (``UARTMode.BINARY``) the received bytes get encoded as one byte hexadecimal numbers with ``0x`` prefix,
        space separated and a space at the end of the byte stream.
        So when receiving the two bytes ``23``, ``42`` the output is ``0x23 0x42 ``.

        In *UTF-8 mode* (``UARTMode.TEXT``) the received data gets interpreted as UTF-8 encoded Unicode string.
        When an UnicodeDecodeError-Exception occurs, the raw data gets printed between ``[]``.

        Is logging enabled, then all received data gets written into the log file.
        In *binary mode* the data gets stored binary, otherwise it gets stored UTF-8 encoded.
        Also ANSI-Escape-Sequences will be stored in the file.
        The file gets opened in *append mode*. Old data will not be overwritten.

        Returns:
            A string of received data or ``None`` when no data is available.

        Raises:
            ValueError: When UARTMode is not supported / invalid
        """

        # Read all available data from the serial input buffer
        try:
            data = self.uart.read(self.uart.in_waiting)
        except:
            return None


        if self.uartmode == UARTMode.TEXT:
            try:
                string = data.decode("utf-8")
            except UnicodeDecodeError:
                string = "[" + str(data) + "]"

        elif self.uartmode == UARTMode.BINARY:
            string = binascii.hexlify(data).decode("utf-8")
            string = " ".join(["0x"+string[i:i+2] for i in range(0, len(string), 2)]) + " "

        else:
            raise ValueError("Unknown/Unsupported UARMode!")


        if self.logfile:
            if self.uartmode == UARTMode.TEXT:
                log.write(string)
            else:
                log.write(data)

        return string



    def Transmit(self, string):
        """
        This method transmit data to the UART device.
        The behavior of this method is independent from the UARTMode.
        Is the string argument of type ``str``, then it gets encoded as UTF-8 byte stream, otherwise
        the raw data gets transmitted.

        Args:
            string (str, bytes): String with data to transmit

        Raises:
            TypeError: When ``string`` is not of type str or bytes.
            UnicodeError: When ``str.encode("utf-8")`` fails encoding the string (only if ``type(string) == str``)
        """
        if type(string) is str:
            data = string.encode("utf-8")

        elif type(string) is bytes:
            data = string
        
        else:
            raise TypeError("UART.Transmit argument must be of type str or bytes!")

        self.uart.write(data)
        return None


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

