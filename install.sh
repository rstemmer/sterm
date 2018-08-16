#!/usr/bin/env bash

PREFIX=/usr/local

echo -e "sterm  Copyright (C) 2018  Ralf Stemmer <ralf.stemmer@gmx.net>"
echo -e "This program comes with \e[1;33mABSOLUTELY NO WARRANTY\e[0m."
echo -e "This is free software, and you are welcome to redistribute it"
echo -e "under certain conditions.\n"

install -m 755 -v -g root -o root sterm4.py -D $PREFIX/bin/sterm
install -m 644 -v -g root -o root sterm.1   -D $PREFIX/share/man/man1/sterm.1


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

