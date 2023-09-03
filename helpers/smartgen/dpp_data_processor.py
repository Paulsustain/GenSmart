.. include:: defs.rst

Troubleshooting
---------------

Reporting a bug
~~~~~~~~~~~~~~~

Please do not contact the author by email. The preferered method to report bugs
and/or enhancement requests is through
`GitHub <https://github.com/eblot/pyftdi/issues>`_.

Please be sure to read the next sections before reporting a new issue.

Logging
~~~~~~~

FTDI uses the `pyftdi` logger.

It emits log messages with raw payload bytes at DEBUG level, and data loss
at ERROR level.

Common error messages
~~~~~~~~~~~~~~~~~~~~~

"Error: No backend available"
`````````````````````````````

libusb native library cannot be loaded. Try helping the dynamic loader:

* On Linux: ``export LD_LIBRARY_PATH=<path>``

  where ``<path>`` is the directory containing the ``libusb-1.*.so``
  library file

* On macOS: ``export DYLD_LIBRARY_PATH=.../lib``

  where ``<path>`` is the directory containing the ``libusb-1.*.dylib``
  library file


"Error: Access denied (insufficient permissions)"
`````````````````````````````````````````````````

The system may already be using the device.

* On macOS: starting with 10.9 "*Mavericks*", macOS ships with a native FTDI
  kernel extension that preempts access to the FTDI device.

  Up to 10.13 "*High Sierra*", this driver can be unloaded this way:

  .. code-block:: shell

      sudo kextunload [-v] -bundle com.apple.driver.AppleUSBFTDI

  You may want to use an alias or a tiny script such as
  ``pyftdi/bin/uphy.sh``

  Please note that the system automatically reloads the driver, so it may be
  useful to move the kernel extension so that the system never loads it.

  .. warning::

     From macOS 10.14 "*Mojave*", the Apple kernel extension peacefully
     co-exists with libusb_ and PyFtdi_, so you no longer need - and **should
     not attempt** - to unload the kernel extension. If you still experience
     this error, please verify you have not installed anothe