<h3 align="center">sterm</h3>

<div align="center">
  Status: Active - License: GPL v3
</div>

---

<p align="center"> sterm is a minimal serial terminal that focus on being easy to use. - This client just does its job.
    <br/>
</p>


## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Acknowledgments](#acknowledgement)


## 🧐 About <a name = "about"></a>

**sterm** is a minimal serial terminal that focus on being easy to use and not sucking. - This client simply works.
It has inline input and supports Unicode (utf-8).
Each character typed gets directly send to the connected device without buffering.
It writes whatever it receives to *stdout* so that also Unicode and ANSI escape sequences work as expected.

### Core Use-Cases

*Ideal for debugging:*<br/>
With the ``--binary`` option, the received data will be output byte wise as hexadecimal numbers.

*Ideal for a remote Linux shell:*<br/>
With the ``--noecho`` option, each character typed gets directly send to the connected device without buffering and echoing.
This makes the Linux console usage seamlessly like using telnet or ssh.

### Core Features

- Inline input
- No line buffering
- Unicode support
- ANSI Escape Sequences supported
- No GUI


## 🏁 Getting Started <a name = "getting_started"></a>

There are two ways to install _sterm_.
Directly using `pip` or from the cloned repository.

### Installation using pip

```bash
pip install sterm
```

### Installation from Repository

```bash
# Download
git clone https://github.com/rstemmer/sterm.git
cd sterm

# Dependencies
pip install pyserial

# Install Package
pip install .

```


## 🎈 Usage <a name="usage"></a>

*sterm* has three interfaces:

1. Configuration files
2. The command line interface
3. Escape commands

### Configuration via files

TODO - Not yet implemented.

### Command Line Arguments

```bash
sterm [-h] [--noecho] [--escape character] [--binary] [-b BAUDRATE] [-f FORMAT] [-w logfile] DEVICE
```

When a command line argument is contradictory to a setting in the configuration files, the command line argument has higher priority.

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

### Escape commands

The following strings can be entered while _sterm_ is running.
Just hit the escape-key and then enter the commands.
They get not send to the device.
Instead they are interpreted by _sterm_.
The preceded escape character can be defined with --escape.
Default is the escape key ("\e").

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


## ⛏️ Building and Testing <a name = "built_using"></a>

### Testing

To test _sterm_ from the sources, just call the `test.py` script.
It runs the command line interface of _sterm_.

You can use `socat` to create a virtual serial connection with two endings, so that you can use two `sterm` processes to communicate with each other:

```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```

### Building a new Package

To build a new package from the source code, just execute the `pkg-make.sh` script.
Make sure to update the version number in the `sterm/cli.py` file.
This version number, as well as the README.md file gets read by the setup.py file.

```bash
vim sterm/cli.py
./pkg-make.sh
```


## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@kylelobo](https://github.com/kylelobo) for [this README template](https://github.com/kylelobo/The-Documentation-Compendium)
- [The pyserial project](https://github.com/pyserial/pyserial) that is the base of _sterm_

