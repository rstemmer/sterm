
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from sterm.cli import VERSION

setuptools.setup(
        name            = "sterm",
        version         = VERSION,
        author          = "Ralf Stemmer",
        author_email    = "ralf.stemmer@gmx.net",
        description     = "A minimal serial / UART command line terminal that focus on being easy to use.",
        long_description= long_description,
        long_description_content_type   = "text/markdown",
        url             = "https://github.com/rstemmer/sterm",
        project_urls    = {
                "Documentation": "https://github.com/rstemmer/sterm",
                "Source":  "https://github.com/rstemmer/sterm",
                "Tracker": "https://github.com/rstemmer/sterm/issues",
            },
        packages        = setuptools.find_packages(),
        data_files      = [("man/man1", ["sterm.1"])],
        entry_points={
                "console_scripts": [
                    "sterm=sterm.cli:main",
                    ],
                },
        install_requires= ["pyserial"],
        python_requires = ">=3.8",
        keywords        = "serial-communication serial-terminal terminal uart rs232 monitoring tty pyserial serial",
        license         = "GPL",
        classifiers     = [
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Topic :: Terminals",
            "Topic :: Terminals :: Serial",
            "Topic :: Communications",
            "Topic :: Scientific/Engineering",
            "Topic :: Software Development :: Debuggers",
            "Topic :: Software Development :: Embedded Systems",
            "Topic :: System :: Logging",
            "Topic :: System :: Monitoring",
            "Topic :: Utilities",
            ],
            #"Development Status :: 3 - Alpha",
        )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

