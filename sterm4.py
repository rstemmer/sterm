#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# STERM, a serial communication terminal with server capabilities        #
# Copyright (C) 2013,2014,2015,2016,2017  Ralf Stemmer (ralf.stemmer@gmx.net)
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
import time
import argparse
import binascii
from threading import Thread

try:
    from serial import *
except:
    print("\033[1;31mModule \033[1;37mpyserial \033[1;31mmissing!")
    print("\033[1;34m Try \033[1;36mpip\033[1;30m3\033[1;36m install pyserial\033[1;34m as root to install it.\033[1;30m")
    exit(1)



VERSION = "4.2.0"

# CHANGELOG
#
# 4.2.0
#  + "--binary" option added
#  * shebang fixed
#


ShutdownReceiver = False


cli = argparse.ArgumentParser(
    description="A minimal serial ternimal.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

cli.add_argument(      "--binary",      default=False,                action="store_true",
    help="Display raw data instead of UTF-8 encoded. (read only)")
cli.add_argument("-b", "--baudrate",    default=115200,     type=int, action="store",
    help="The baudrate used for the communication.")
cli.add_argument("-f", "--format",      default="8N1",      type=str, action="store",
    help="Configuration-triple: xyz with x=bytelength in bits {5,6,7,8}, y=parity {N,E,O}, z=stopbits {1,2}.")
cli.add_argument("device",                                  type=str, action="store",
    help="Path to the serial communication device.")

# Mapping the format-string to the pyserial-parameters.
# This is just a subset. See pyserial-docs to extend these maps.
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



def rec_thread(rs232, binary=False):
    data = ""
    while not ShutdownReceiver:

        try:
            data = rs232.read(rs232.inWaiting())
        except:
            return

        if data:

            if binary:
                string = binascii.hexlify(data).decode("utf-8")
                string = " ".join(["0x"+string[i:i+2] for i in range(0, len(string), 2)]) + " "
            else:
                string = data.decode("utf-8")

            sys.stdout.write(string)
            sys.stdout.flush()
      
        time.sleep(0.1);



if __name__ == '__main__':

    # handle command line arguments
    args     = cli.parse_args()
    DEVICE   = args.device
    BAUDRATE = args.baudrate
    FORMAT   = args.format

    # translate format-string
    try:
        BYTESIZE = BYTESIZEMAP[FORMAT[0]]
        PARITY   = PARITYMAP  [FORMAT[1]]
        STOPBITS = STOPBITMAP [FORMAT[2]]
    except Exception as e:
        print("\033[1;31mFormat \033[1;37m" + FORMAT + " \033[1;31minvalid!\033[0m")
        print("Use --help as argument to display the help including the format-description.")
        exit(1)

    # Open terminal device
    try:
        uart = Serial(
            port    = DEVICE,
            baudrate= BAUDRATE,
            bytesize= BYTESIZE,
            parity  = PARITY,
            stopbits= STOPBITS,
            timeout = 0.1,
            xonxoff = 0,
            rtscts  = 0,
            interCharTimeout=None
        )
    except Exception as e:
        print("\033[1;31mAccessing \033[1;37m" + DEVICE + " \033[1;31mfailed with the following excpetion:\033[0m")
        print(e)
        exit(1)
    
    print("\n\033[1;31m --[ \033[1;34msterm \033[1;31m//\033[1;34m " + VERSION + "\033[1;31m ]-- \033[0m\n")

    ReceiverThread = Thread(target=rec_thread, args=(uart,args.binary))
    ReceiverThread.start()

    cmd = ""

    while cmd != ".exit":
        cmd = input("")

        if cmd == ".exit":
            print("\n\033[1;37m\033[44m >> Stopping all Threads… << \033[0m\n")
            ShutdownReceiver = True

            if ReceiverThread.isAlive():
                ReceiverThread.join()
            break

        elif cmd == ".version":
            print("Version: " + VERSION)

        else:
            cmd += "\n"
            data = cmd.encode("utf-8")
            uart.write(data)


    uart.close()



# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

