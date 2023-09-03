      | Output 6 MHz clock (FT232R and FT-X only)                                      |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``BAT_DETECT``  | High   | Battery Charger Detect (FT-X only)                                             |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``BAT_NDETECT`` | Low    | Inverse signal of BAT_DETECT (FT-X only)                                       |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``I2C_TXE``     | Low    | Transmit buffer empty (FT-X only)                                              |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``I2C_RXF``     | Low    | Receive buffer full  (FT-X only)                                               |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``VBUS_SENSE``  | High   | Detect when VBUS is present via the appropriate AC IO pad (FT-X only)          |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``BB_WR``       | Low    | Synchronous Bit Bang Write strobe (FT232R and FT-X only)                       |
+-----------------+--------+--------------------------------------------------------------------------------+
| ``BB_RD``       | Low    | Synchronous Bit Bang Read strobe (FT232R and FT-X only)                        |
+-----------------+--------+---------------------------------------------------------------