.. include:: defs.rst

.. _url_scheme:

URL Scheme
----------

There are two ways to open a connection to an `Ftdi` object.

The recommended way to open a connection is to specify connection details
using a URL. The URL scheme is defined as:

::

    ftdi://[vendor][:[product][:serial|:bus:address|:index]]/interface

where:

* vendor: the USB vendor ID of the manufacturer

  * ex: ``ftdi`` or ``0x403``

* product: the USB product ID of the device

  * ex: ``232h`` or ``0x6014``
  * Supported product IDs: ``0x6001``, ``0x6010``, ``0x6011``, ``0x6014``,
    ``0x6015``
  * Supported product aliases:

    * ``232``, ``232r``, ``232h``, ``2232d``, ``2232h``, ``4232h``, ``230x``
    * ``ft`` prefix for all aliases is also accepted, as for example ``ft232h``

* ``serial``: the serial number as a string. This is the preferred method to
  uniquely identify a specific FTDI device. However, some FTDI device are not
  fitted with an EEPROM, or the EEPROM is either corrupted or erased. In this
  case, FTDI devices report no serial number

  Examples:
     * ``ftdi://ftdi:232h:FT0FMF6V/1``
     * ``ftdi://:232h:FT0FMF6V/1``
     * ``ftdi://::FT0FMF6V/1``

* ``bus:addess``: it is possible to select a FTDI device through a bus:address
  pair, specified as *hexadecimal* integer values.

  Examples:
     * ``ftdi://ftdi:232h:10:22/1``
     * ``ftdi://ftdi:232h:10:22/1``
     * ``ftdi://::10:22/1``

  Here, bus ``(0x)10`` = 16 (decimal) and address ``(0x)22`` = 34 (decimal)

* ``index``: an integer - not particularly useful, as it depends on the
  enumeration order on the USB buses, and may vary from on session to another.

* ``interface``: the interface of FTDI device, starting from 1

  * ``1`` for 230x and 232\* devices,
  * ``1`` or ``2`` for 2232\* devices,
  * ``1``, ``2``, ``3`` or ``4`` for 4232\* devices

All parameters but the interface are optional, PyFtdi tries to find the best
match. Therefore, if you have a single FTDI device connected to your system,
``ftdi:///1`` should be enough.

You can also ask PyFtdi to enumerate all the compatible devices with the
special ``ftdi:///?`` syntax. This syntax is useful to retrieve the available
FTDI URLs with serial number and/or bus:address selectors.

There are several APIs available to enumerate/filter available FTDI device.
See :doc:`api/ftdi`.

Note that opening an FTDI connection with a URL ending with `?` is interpreted
as a query for matching FTDI devices and immediately stop. With this special
URL syntax, the avaialble devices are printed out to the standard output, and
the Python interpreter is forced to exit (`SystemExit` is raised).

When simple enumeration of the available FTDI devices is needed - so that
execution is not interrupted, two helper methods are available as
:py:meth:`pyftdi.ftdi.Ftdi.list_devices` and
:py:meth:`pyftdi.ftdi.Ftdi.show_devices` and accept the same URL syntax.

Opening a connection
~~~~~~~~~~~~~~~~~~~~

URL-based methods to open a connection
``````````````````````````````````````

.. code-block:: python

   open_from_url()
   open_mpsse_from_url()
   open_bitbang_from_url()


Device-based methods to open a connection
`````````````````````````````````````````

You may also open an Ftdi device from an existing PyUSB_ device, with the help
of the ``open_from_device()`` helper method.

.. code-block:: python

   open_from_device()
   open_mpsse_from_device()
   open_bitbang_from_device()


Legacy methods to open a connection
```````````````````````````````````

The old, deprecated method to open a connection is to use the ``open()``
methods without the ``_from_url`` suffix, which accept VID, PID, and serial
parameters (among others).

.. code-block:: python

   open()
   open_mpsse()
   open_bitbang()

See the :ref:`ftdi_urls` tool to obtain the URLs for the connected FTDI
devices.
                                                                                                                                                                                                                                                                                     .. include:: defs.rst

FTDI device pinout
------------------

============ ============= ======= ====== ============== ========== ====== ============
 IF/1 [#ih]_ IF/2 [#if2]_  BitBang  UART   |I2C|          SPI        JTAG   C232HD cable
============ ============= ======= ====== ============== ========== ====== ============
 ``ADBUS0``   ``BDBUS0``   GPIO0    TxD    SCK            SCLK       TCK   Orange
 ``ADBUS1``   ``BDBUS1``   GPIO1    RxD    SDA/O [#i2c]_  MOSI       TDI   Yellow
 ``ADBUS2``   ``BDBUS2``   GPIO2    RTS    SDA/I [#i2c]_  MISO       TDO   Green
 ``ADBUS3``   ``BDBUS3``   GPIO3    CTS    GPIO3          CS0        TMS   Brown
 ``ADBUS4``   ``BDBUS4``   GPIO4    DTR    GPIO4          CS1/GPIO4        Grey
 ``ADBUS5``   ``BDBUS5``   GPIO5    DSR    GPIO5          CS2/GPIO5        Purple
 ``ADBUS6``   ``BDBUS6``   GPIO6    DCD    GPIO6          CS3/GPIO6        White
 ``ADBUS7``   ``BDBUS7``   GPIO7    RI     RSCK [#rck]_   CS4/GPIO7  RCLK  Blue
 ``ACBUS0``   ``BCBUS0``                   GPIO8          GPIO8
 ``ACBUS1``   ``BCBUS1``                   GPIO9          GPIO9
 ``ACBUS2``   ``BCBUS2``                   GPIO10         GPIO10
 ``ACBUS3``   ``BCBUS3``                   GPIO11         GPIO11
 ``ACBUS4``   ``BCBUS4``                   GPIO12         GPIO12
 ``ACBUS5``   ``BCBUS5``                   GPIO13         GPIO13
 ``ACBUS6``   ``BCBUS6``                   GPIO14         GPIO14
 ``ACBUS7``   ``BCBUS7``                   GPIO15         GPIO15
============ ============= ======= ====== ============== ========== ====== ============

.. [#ih]  16-bit port (ACBUS, BCBUS) is not available with FT4232H_ series, and
          FTDI2232C/D only support 12-bit ports.
.. [#i2c] FTDI pins are either configured as input or output. As |I2C| SDA line
          is bi-directional, two FTDI pins are required to provide the SDA
          feature, and they should be connected together and to the SDA |I2C|
          bus line. Pull-up resistors on SCK and SDA lines should be used.
.. [#if2] FT232H_ does not support a secondary MPSSE port, only FT2232H_ and
          FT4232H_ do. Note that FT4232H_ has 4 serial ports, but only the
          first two interfaces are MPSSE-capable. C232HD cable only exposes
          IF/1 (ADBUS).
.. [#rck] In order to support I2C clock stretch mode, ADBUS7 should be
          connected to SCK. When clock stretching mode is not selected, ADBUS7
          may be used as GPIO7.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           License
-------

.. include:: defs.rst

For historical reasons (PyFtdi has been initially developed as a compatibility
layer with libftdi_), the main ``ftdi.py`` file had originally been licensed
under the same license as the libftdi_ project, the GNU Lesser General Public
License LGPL v2 license. It does not share code from this project anymore, but
implements a similar API.

From my perspective, you may use it freely in open source or close source, free
or commercial projects as long as you comply with the BSD 3-clause license.


BSD 3-clause
~~~~~~~~~~~~

::

  Copyright (c) 2008-2020 Emmanuel Blot <emmanuel.blot@free.fr>
  All Rights Reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of the author nor the names of its contributors may
        be used to endorse or promote products derived from this software
        without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL NEOTION BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           