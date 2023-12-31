PyFtdi
======

.. cannot use defs.rst here, as PyPi wants a standalone file.
.. |I2C| replace:: I\ :sup:`2`\ C

Documentation
-------------

The latest PyFtdi online documentation is always available from
`here <https://eblot.github.io/pyftdi>`_.

Beware the online version may be more recent than the PyPI hosted version, as
intermediate development versions are not published to
`PyPi <https://pypi.org/project/pyftdi>`_.

PyFtdi documentation can be locally build with Sphinx, see the installation
instructions.

Source code
-----------

PyFtdi releases are available from the Python Package Index from
`PyPi <https://pypi.org/project/pyftdi>`_.

PyFtdi development code is available from
`GitHub <https://github.com/eblot/pyftdi>`_.

Overview
--------

PyFtdi aims at providing a user-space driver for popular FTDI devices,
implemented in pure Python language.

Suported FTDI devices include:

* UART and GPIO bridges

  * FT232R (single port, 3Mbps)
  * FT230X/FT231X/FT234X (single port, 3Mbps)

* UART and multi-serial protocols (SPI, |I2C|, JTAG) bridges

  * FT2232C/D (dual port, clock up to 6 MHz)
  * FT232H (single port, clock up to 30 MHz)
  * FT2232H (dual port, clock up to 30 MHz)
  * FT4232H (quad port, clock up to 30 MHz)

Features
--------

PyFtdi currently supports the following features:

* UART/Serial USB converter, up to 12Mbps (depending on the FTDI device
  capability)
* GPIO/Bitbang support, with 8-bit asynchronous, 8-bit synchronous and
  8-/16-bit MPSSE variants
* SPI master, with simultanous GPIO support, up to 12 pins per port,
  with support for non-byte sized transfer
* |I2C| master, with simultanous GPIO support, up to 14 pins per port
* Basic JTAG master capabilities
* EEPROM support (some parameters cannot yet be modified, only retrieved)
* Experimental CBUS support on selected devices, 4 pins per port

Supported host OSes
-------------------

* macOS
* Linux
* FreeBSD
* Windows, although not officially supported

.. EOT

Warning
-------

Starting with version *v0.40.0*, several API changes are being introduced.
While PyFtdi tries to maintain backward compatibility with previous versions,
some of these changes may require existing clients to update calls to PyFtdi.

Do not upgrade to *v0.40.0* or above without testing your client against the
new PyFtdi releases. PyFtdi versions up to *v0.39.9* keep a stable API
with *v0.22+* series.

See the *Major Changes* section on the online documentation for details about
potential API breaks.


Major changes
~~~~~~~~~~~~~

 * *read* methods now return ``bytearray`` instead of `Array('B')` so that
   pyserial ``readline()`` may be used. It also brings some performance
   improvements.
 * PyFtdi URLs now supports ``bus:address`` alternative specifiers, which
   required to augment the ``open_*()`` methods with new, optional parameters.
 * ``SpiController`` reserves only one slave line (*/CS*) where it used to
   reserve 4 slave lines in previous releases. This frees more GPIOs when
   default value is used - it is nevertheless still possible to reserve up to 5
   slave lines.
 * type hinting is used for most, if not all, public methods.
 * simplified baudrate divider calculation.

PyFTDI in details
-----------------

.. toctree::
   :maxdepth: 1
   :glob:

   features
   requirements
   installation
   urlscheme
   tools
   api/index
   pinout
   gpio
   eeprom
   testing
   troubleshooting
   authors
   license
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           .. include:: defs.rst

EEPROM management
-----------------

.. warning::
   Writing to the EEPROM can cause very **undesired** effects if the wrong
   value is written in the wrong place. You can even essentially **brick** your
   FTDI device. Use this function only with **extreme** caution.

   It is not recommended to use this application with devices that use an
   internal EEPROM such as FT232R or FT-X series, as if something goes wrong,
   recovery options are indeed limited. FT232R internal EEPROM seems to be
   unstable, even the official FT_PROG_ tool from FTDI may fail to fix it on
   some conditions.

   If using a Hi-Speed Mini Module and you brick for FTDI device, see
   FTDI_Recovery_


Supported features
~~~~~~~~~~~~~~~~~~

EEPROM support is under active development.

Some features may be wrongly decoded, as each FTDI model implements a different
feature map, and more test/validation are required.

The :doc:`EEPROM API <api/eeprom>` implements the upper API to access the
EEPROM content.

.. _ftconf:

EEPROM configuration tool
~~~~~~~~~~~~~~~~~~~~~~~~~

``ftconf.py`` is a companion script to help managing the content of the FTDI
EEPROM from the command line. See the :ref:`tools` chapter to locate this tool.

::

  ftconf.py [-h] [-x] [-X HEXBLOCK] [-i INPUT] [-l {all,raw,values}]
                   [-o OUTPUT] [-s SERIAL_NUMBER] [-m MANUFACTURER] [-p PRODUCT]
                   [-c CONFIG] [-e] [-u] [-P VIDPID] [-V VIRTUAL] [-v] [-d]
                   [device]

  Simple FTDI EEPROM configurator.

  positional arguments:
    device                serial port device name

  optional arguments:
    -h, --help            show this help message and exit
    -x, --hexdump         dump EEPROM content as ASCII
    -X HEXBLOCK, --hexblock HEXBLOCK
                          dump EEPROM as indented hexa blocks
    -i INPUT, --input INPUT
                          input ini file to load EEPROM content
    -l {all,raw,values}, --load {all,raw,values}
                          section(s) to load from input file
    -o OUTPUT, --output OUTPUT
                          output ini file to save EEPROM content
    -s SERIAL_NUMBER, --serial-number SERIAL_NUMBER
                          set serial number
    -m MANUFACTURER, --manufacturer MANUFACTURER
                          set manufacturer name
    -p PRODUCT, --product PRODUCT
                          set product name
    -c CONFIG, --config CONFIG
                          change/configure a property as key=value pair
    -e, --erase           erase the whole EEPROM content
    -u, --update          perform actual update, use w/ care
    -P VIDPID, --vidpid VIDPID
                          specify a custom VID:PID device ID, may be repeated
    -V VIRTUAL, --virtual VIRTUAL
                          use a virtual device, specified as YaML
    -v, --verbose         increase verbosity
    -d, --debug           enable debug mode


**Again, please read the** :doc:`license` **terms before using the EEPROM API
or this script. You may brick your device if something goes wrong, and there
may be no way to recover your device.**

Note that to protect the EEPROM content of unexpected modification, it is
mandatory to specify the :ref:`-u <option_u>` flag along any alteration/change
of the EEPROM content. Without this flag, the script performs a dry-run
execution of the changes, *i.e.* all actions but the write request to the
EEPROM are executed.

Once updated, you need to unplug/plug back the device to use the new EEPROM
configuration.

It is recommended to first save the current content of the EEPROM, using the
:ref:`-o <option_o>` flag, to have a working copy of the EEPROM data before any
attempt to modify it. It can help restoring the EEPROM if something gets wrong
during a subsequence update, thanks to the :ref:`-i <option_i>` option switch.

Most FTDI device can run without an EEPROM. If something goes wrong, try to
erase the EEPROM content, then restore the original content.


Option switches
```````````````
In addition to the :ref:`common_option_switches` for  PyFtdi_ tools,
``ftconf.py`` support the following arguments:

.. _option_c:

``-c name=value``
  Change a configuration in the EEPROM. This flag can be repeated as many times
  as required to change several configuration parameter at once. Note that
  without option ``-u``, the EEPROM content is not actually modified, the
  script runs in dry-run mode.

  The name should be separated from the value with an equal ``=`` sign or
  alternatively a full column ``:`` character.

  * To obtain the list of supported name, use the `?` wildcard: ``-c ?``.
  * To obtain the list of supported values for a namw, use the `?` wildcard:
    ``-c name=?``, where *name* is a supported name.

  See :ref:`cbus_func` table for the alternate function associated with each
  name.

.. _option_e:

``-e``
  Erase the whole EEPROM. This may be useful to recover from a corrupted
  EEPROM, as when no EEPROM or a blank EEPROM is detected, the FTDI falls back
  to a default configuration. Note that without option :ref:`-u <option_u>`,
  the EEPROM content is not actually modified, the script runs in dry-run mode.

.. _option_i:

``-i``
  Load a INI file (as generated with the :ref:`-o <option_o>` option switch. It
  is possible to select which section(s) from the INI file are loaded, using
  :ref:`-l <option_l>` option switch. The ``values`` section may be modified,
  as it takes precedence over the ``raw`` section. Note that without option
  :ref:`-u <option_u>`, the EEPROM content is not actually modified, the script
  runs in dry-run mode.

.. _option_l:

``-l <all|raw|values>``
  Define which section(s) of the INI file are used to update the EEPROM content
  along with the :ref:`-i <option_i>` option switch. Defaults to ``all``.

  The supported feature set of the ``values`` is the same as the one exposed
  through the :ref:`-c <option_c>` option switch. Unsupported feature are
  ignored, and a warning is emitted for each unsupported feature.

.. _option_m:

``-m <manufacturer>``
  Assign a new manufacturer name to the device. Note that without option
  :ref:`-u <option_u>`, the EEPROM content is not actually modified, the script
  runs in dry-run mode. Manufacturer names with ``/`` or ``:`` characters are
  rejected, to avoid parsing issues with FTDI :ref:`URLs <url_scheme>`.


.. _option_o:

``-o <output>``
  Generate and write to the specified file the EEPROM content as decoded
  values and a hexa dump. The special ``-`` file can be used as the output file
  to print to the standard output. The output file contains two sections:

  * ``[values]`` that contain the decoded EEPROM configuration as key, value
    pair. Note that the keys and values can be used as config