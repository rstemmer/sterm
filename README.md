
# sterm

sterm is a minimal serial terminal that focus on being easy to use and not sucking. - This client simply works.
It has inline input and supports Unicode (utf-8).
Each character typed gets directly send to the connected device without buffering.
It writes whatever it receives to *stdout* so that also ANSI escape sequences work as expected.

*Ideal for debugging:*
With the ``--binary`` option, the received data will be output byte wise as hexadecimal numbers.

*Ideal for a remote Linux shell:*
With the ``--noecho`` option, each character typed gets directly send to the connected device without buffering and echoing.
This makes the Linux console usage seamlessly like using telnet or ssh.

**Project State:** Alive and maintained

## Installation

There are two ways to install _sterm_.
Directly using `pip` or from the cloned repository.

### Using pip

```bash
pip install sterm
```

### From Repository

```bash
# Download
git clone https://github.com/rstemmer/sterm.git
cd sterm

# Dependencies
pip install pyserial

# Install Package
pip install .

```

## Usage

### Command Line Arguments

```bash
sterm [-h] [--noecho] [--escape character] [--binary] [-b BAUDRATE] [-f FORMAT] [-w logfile] DEVICE
```

  * __-h__: Print help.
  * __-n__: Enable _noecho_ mode. _Default_ is echoing each entered key to _stdout_.
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
sterm --noecho --escape _ /dev/ttyUSB0
~# whoami
root
~# _exit
```

Communicating with two _sterm_ instances via a pseudo terminal for testing:
![A picture that demonstrates the possibility of receiving ANSI escape sequences and unicode charaters](/stermscreenshot.png?raw=true "Testrun showing some capabilities of sterm")


