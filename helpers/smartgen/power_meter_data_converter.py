 the `hexdump -Cv` tool.


.. _cbus_func:

CBUS function
`````````````

The following table describes the CBUS pin alternate functions. Note that
depending on the actual device, some alternate function may not be available.

+-----------------+--------+--------------------------------------------------------------------------------+
| Name            | Active | Description                                                                    |
+=================+========+================================================================================+
| ``TRISTATE``    | Hi-Z   | IO Pad is tri-stated                                                           |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``TXLED``       | Low    | TX activity, can be used as status for LED                                     |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``RXLED``       | Low    | RX activity, can be used as status for LED                                     |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``TXRXLED``     | Low    | TX & RX activity, can be used as status for LED                                |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``PWREN``       | Low    | USB configured, USB suspend: high                                              |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``SLEEP``       | Low    | USB suspend, typically used to power down external devices.                    |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``DRIVE0``      | Low    | Drive a constant (FT232H and FT-X o