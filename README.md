
# sterm

sterm is a minimal serial terminal that focus on being easy to use and not sucking. - This client simply works.
It has inline input and supports Unicode (utf-8).
It writes whatever it receives to *stdout* so that also ANSI escape sequences work as expected.

*Ideal for debugging:*
With the ``--binary`` option, the received data will be output byte wise as hexadecimal numbers.

*Ideal for a remote Linux shell:*
With the ``--unbuffered`` option, each character typed gets directly send to the connected device without buffering and echoing.

**Project State:** Alive and maintained

## Installation

You should check the `install.sh` script before executing.
The default installation path is _/usr/local/bin_

```bash
# Download
git clone https://github.com/rstemmer/sterm.git
cd sterm

# Install
sudo ./install.sh

# Dependencies
pip3 install pyserial
```

## Usage

### Command Line Arguments

```bash
sterm [-h] [--unbuffered] [--escape character] [--binary] [-b BAUDRATE] [-f FORMAT] [-w logfile] DEVICE
```

  * __-h__: Print help.
  * __-u__: Enable unbuffered mode
  * __--escape__: Define an alternative escape character. _Default_ is escape ("\e").
  * __--binary__: Print hexadecimal values instead of Unicode characters. (Only applied on output, input will still be UTF-8)
  * __-b__: Baudrate. _Default:_ 115200 baud.
  * __-f__: Configuration-triple: xyz with x = bytelength in bits {5,6,7,8}; y = parity {N,E,O}; z = stopbits {1,2}. _Default:_ "8N1" - _8_ data bits, _no_ parity bits and _1_ stop bit.
  * __-w__: Write received data into a file.

_DEVICE_ is the path to the serial terminal.
For example _/dev/ttyS0_, _/dev/ttyUSB0_, _/dev/ttyUART0_, _/dev/ttyACM0_, _/dev/pts/42_.

For details read the man-page.

### Internal commands

The following strings get not send to the device. Instead they are interpreted by _sterm_.
They have a preceded escape character defined with --escape. Default is the escape key ("\e").

  * __exit__: quit sterm
  * __version__: print version

### Examples

Send _ping_ to UART0 and exit:
```
sterm /dev/ttyUART0
ping
pong
^[exit
```

Send _hello_ to a serial device with 9600 baud, 7 data bits, even parity, and 2 stop bits. Then exit:
```
sterm -b 9600 -f 7E2 /dev/ttyS0
hello
world
^[exit
```

Connecting to a Linux device
```
sterm --unbuffered --escape _ /dev/ttyUSB0
~# whoami
root
~# _exit
```

Communicating with two _sterm_ instances via a pseudo terminal for testing:
![A picture that demonstrates the possibility of receiving ANSI escape sequences and unicode charaters](/stermscreenshot.png?raw=true "Testrun showing some capabilities of sterm")


