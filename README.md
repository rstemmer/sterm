<h3 align="center">sterm</h3>

<div align="center">
  Status: 🟢 Active - License: GPL v3
</div>

---

<p align="center"> sterm is a minimal serial terminal that focus on being easy to use. - This client just does its job.
    <br/>
</p>

```bash
pip install sterm
sterm --help
sterm /dev/ttyUSB0
```


## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Related Work](#related_work)
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
**A:** Directly using `pip` or **B:** from the cloned repository.

### Precondition

_sterm_ requires Python 3.8+ to run.
Before you start installing _sterm_ make sure you use the correct version.
Depending on your distribution, the you may need to use `pip3` instead of `pip`.
You can check your Python version by executing the following commands:

```bash
python --version
pip --version
```

Both should print a version number beginning with 3.
If not, you need to use `pip3` to explicit use Python 3.

For a user-only installation, call `pip ...` as user.
For a system-wide installation you need to be root, or call `sudo pip ...`.

### A: Installation using pip

```bash
pip install sterm
```

### B: Installation from Repository

```bash
# Download
git clone https://github.com/rstemmer/sterm.git
cd sterm

# Dependencies
pip install pyserial

# Install Package
pip install .

```

### Check installation

After installation you can check if _sterm_ is successfully installed using `whereis`.
```bash
whereis sterm
#Outpu: sterm: /usr/bin/sterm /usr/man/man1/sterm.1
```
There should be two files listed.
 - `sterm` is the executable, the command you run.
 - `sterm.1` is the manual for `sterm` that can be read by executing `man sterm` on the command line.

On a system-wide installation, _sterm_ is usually installed to /usr/bin.
If you only installed to for a single user, it is usually installed to ~/.local/bin

During the installation process, `pip` should install all dependencies recursively.
To be sure nothing is missing, you can run `pip check sterm`.
It prints all missing dependencies or version conflicts.
You can install missing dependencies via `pip`.
When version conflicts are listed, you can hope they do not matter or install an explicit version via `pip` as well.


## 🎈 Usage <a name="usage"></a>

To execute _sterm_ you just have to call the `sterm` command in your shell.
`sterm` requires one argument, the device you want to access.
All other arguments listed in the subsection below are optional.

UART-Devices are listed in the /dev directory with the prefix `tty`.
Most UART-Devices are addressable via /dev/ttyUSBx or /dev/ttyACMx were x is a number depending on the order they got recognized by the Linux kernel.


*sterm* has two interfaces:

1. The command line interface
2. Escape commands


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

## ⛓ Related Work <a name ="related_work"></a>

 - [tio](https://github.com/tio/tio) A more feature rich alternative to `sterm` with a similar motivation

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [@kylelobo](https://github.com/kylelobo) for [this README template](https://github.com/kylelobo/The-Documentation-Compendium)
- [The pyserial project](https://github.com/pyserial/pyserial) that is the base of _sterm_

