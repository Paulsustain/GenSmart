.. include:: defs.rst

Requirements
------------

Python_ 3.5 or above is required; new tests require 3.6 or above, as they rely
on fstring_ syntax (PEP_498_) and variable annotation syntax (PEP_526_).

PyFtdi_ relies on PyUSB_, which itself depends on one of the following native
libraries:

* libusb_, currently tested with 1.0.23

PyFtdi_ does not depend on any other native library, and only uses standard
Python modules along with PyUSB_ and pyserial_.

PyFtdi_ is beeing tested with PyUSB_ 1.0.2.

Development
~~~~~~~~~~~

PyFtdi_ is developed on macOS platforms (64-bit kernel), and is validated on a
regular basis on Linux hosts.

As it contains no native code, it should work on any PyUSB_ and libusb_
supported platforms. However, M$ Windows is a seamless source of issues and is
not officially supported, although users have reported successful installation
with Windows 7 for example. Your mileage may vary.

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            