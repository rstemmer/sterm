#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# STERM, a serial communication terminal with server capabilities        #
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
import os
import tty
import termios
import time
import argparse
from threading      import Thread
from sterm.uart     import UART, UARTMode
from sterm.terminal import Terminal



VERSION = "6.0.0a5"


# This global variable is used to shutdown the thread used
# for the ReceiveData function.
ShutdownReceiver = False


cli = argparse.ArgumentParser(
    description="A minimal serial ternimal.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

cli.add_argument(      "--binary",      default=False,                action="store_true",
    help="Display raw data instead of UTF-8 encoded. (read only)")
cli.add_argument("-u", "--unbuffered",  default=False,                action="store_true",
    help="Direct character transmission. Does not buffer a whole line for the user input.")
cli.add_argument(      "--escape",      default="\033",     type=str, action="store",
    help="Change the default escape character (escape)")
cli.add_argument("-b", "--baudrate",    default=115200,     type=int, action="store",
    help="The baudrate used for the communication.")
cli.add_argument("-f", "--format",      default="8N1",      type=str, action="store",
    help="Configuration-triple: xyz with x=bytelength in bits {5,6,7,8}, y=parity {N,E,O}, z=stopbits {1,2}.")
cli.add_argument("-w", "--write",       metavar="logfile",  type=str, action="store",
    help="Write received data into a file")
cli.add_argument("device",                                  type=str, action="store",
    help="Path to the serial communication device.")

UNBUFFERED = False      # Enable the unbuffered mode
ESCAPECHAR = "\033"     # Escape character to start an escape command sequence


def ReceiveData(uart, term):
    """
    This function reads every 0.1 seconds all data from the serial input buffer.
    The read data then gets printed to the screen (stdout).
    After writing to the output buffer, the buffer gets flushed so that the data is visible to the user
    as soon as possible.
    The function is blocking and runs until the global variable ``ShutdownReveiver`` get set to ``False``
    or when reading from the input buffer raises an exception.

    The behavior of this function depends on the ``binary`` argument:

    In *binary mode* the received bytes get encoded as one byte hexadecimal numbers with ``0x`` prefix,
    space separated and a space at the end of the byte stream.
    So when receiving the two bytes ``23``, ``42`` the output is ``0x23 0x42 ``.

    In *UTF-8 mode* the received data gets interpreted as UTF-8 encoded Unicode string.
    When an UnicodeDecodeError-Exception occurs, the raw data gets printed between ``[]``.

    Is the ``logfile`` parameter a sting, then all received data gets written into that file.
    In *binary mode* the data gets stored binary, otherwise it gets stored UTF-8 encoded.
    Also ANSI-Escape-Sequences will be stored in the file.
    The file gets opened in *append mode*. Old data will not be overwritten.

    This function is intended to run in a separate thread.
    The following example shows how to handle this function.

    .. code-block::

        # Start receiver thread
        ReceiverThread = Thread(target=ReceiveData, args=(uart, ))
        ReceiverThread.start()

        # …

        # Shutdown receiver thread
        ShutdownReceiver = True
        if ReceiverThread.isAlive():
            ReceiverThread.join()


    Args:
        uart: Instance of the *pyserial* ``Serial`` class.

    Returns:
        *Nothing*
    """

    data = ""
    while not ShutdownReceiver:

        string = uart.Receive()
        term.Write(string)
        time.sleep(0.1)



def ReadCommand(term):
    """
    Returns:
        A command string
    """
    char    = ""
    command = ""

    while True:
        char = term.ReadCharacter()
        if char == "\r":
            break
        elif char == ESCAPECHAR:
            if len(command) == 0:
                command = ESCAPECHAR
            break
        else:
            term.Write(char)
            command += char

    term.Write("\n")
    return command

def HandleUnbufferedUserInput(uart, term):
    """
    This function handles the user input in *Unbuffered Mode*.
    It reads the input from *stdin* byte by byte and sends it directly UTF-8 encoded to the UART device.

    When the escape character gets entered, the function starts to record a command instead of sending
    the data to the UART device.
    The escape character is defined in the global variable ``ESCAPECHAR`` that can be set via the
    command line parameter ``--escape``.
    The default character is *escape* (``\e``).
    Valid escape commands are ``exit`` to leave this function and exit ``sterm``,
    or ``version`` to print the version number of ``sterm`` to *stdout*.
    Enter the escape character twice send one escape character to the UART device.

    When the TTY is set to unbuffered mode, it expects the sequence ``\r\n`` for line breaks.
    This function takes care the ``\r\n`` sequences and ``\n``-only line breaks are handled correctly.

    The function expects UTF-8 encoded input.

    Args:
        uart: Instance of the *pyserial* ``Serial`` class.

    Returns:
        *Nothing*
    """
    char = ""

    while True:
        char = term.ReadCharacter()

        # Handle escape sequences
        if char == ESCAPECHAR:
            command = ReadCommand(term)

            if command == ESCAPECHAR:
                uart.write(ESCAPECHAR.encode("utf-8"))

            if command == "exit":
                break

            elif command == "version":
                print("Version: " + VERSION, end="\r\n")

        # Send character to UART-Device
        else:
            # In this mode, \n needs to be added manually to get a new line
            if char == "\r":
                char += "\n"
            uart.Transmit(char)

    return



def HandleBufferedUserInput(uart, term):
    r"""
    This function handles the user input in *Bufferd Mode*.
    It reads a complete line until the user hits the enter-key into a buffer.
    Then the whole buffer gets send UTF-8 encoded to the UART device.

    This function provides to escape commands.
    The escape character is defined in the global variable ``ESCAPECHAR`` that can be set via the
    command line parameter ``--escape``.
    The default character is *escape* (``\e``).
    When the line is ``"\033exit"`` this function gets left and ``sterm`` will shut down.
    On ``"\033version"`` the version number gets printed to *stdout*.

    The function expects UTF-8 encoded input.

    Args:
        uart: Instance of the *pyserial* ``Serial`` class.

    Returns:
        *Nothing*
    """
    command = ""

    while True:
        command = term.ReadLine()

        if command == ESCAPECHAR + "exit":
            break

        elif command == ESCAPECHAR + "version":
            print("Version: " + VERSION)

        else:
            command += "\n"
            uart.Transmit(command)
    return



def main():
    print("\n\033[1;31m --[ \033[1;34msterm \033[1;31m//\033[1;34m " + VERSION + "\033[1;31m ]-- \033[0m\n")

    # Handle command line arguments
    args       = cli.parse_args()
    DEVICE     = args.device
    BAUDRATE   = args.baudrate
    FORMAT     = args.format
    UNBUFFERED = args.unbuffered
    ESCAPECHAR = args.escape

    if args.binary:
        UARTMODE = UARTMode.BINARY
    else:
        UARTMODE = UARTMode.TEXT

    # Open remote terminal device
    uart = UART(args.device, args.baudrate, args.format, uartmode=UARTMODE, logpath=args.write)
    term = Terminal(buffered= not args.unbuffered, escape=args.escape)

    # Start receiver thread
    ReceiverThread = Thread(target=ReceiveData, args=(uart, term))
    ReceiverThread.start()

    # this is the main loop of this software
    try:
        if UNBUFFERED:
            HandleUnbufferedUserInput(uart, term);
        else:
            HandleBufferedUserInput(uart, term);
    except:
        # catch all to be able to clean up
        pass

    # Shutdown receiver thread
    global ShutdownReceiver
    ShutdownReceiver = True
    if ReceiverThread.isAlive():
        ReceiverThread.join()

    # Clean up everything
    uart.Disconnect()


if __name__ == '__main__':
    main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

