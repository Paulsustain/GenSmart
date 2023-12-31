
�.�_�W  �               @   s�   d  Z  d d l m Z m Z d d l m Z m Z m	 Z	 m
 Z
 d d l m Z m Z d d l m Z Gd d �  d e � Z Gd	 d
 �  d
 � Z Gd d �  d e � Z Gd d �  d e � Z e Z Gd d �  d e � Z Gd d �  d e � Z d S)zGPIO/BitBang support for PyFdti�    )�calcsize�unpack)�Iterable�Optional�Tuple�Union�   )�Ftdi�	FtdiError)�is_iterablec               @   s   e  Z d  Z d Z d S)�GpioExceptionz Base class for GPIO errors.
    N)�__name__�
__module__�__qualname__�__doc__� r   r   �-/tmp/pip-build-56fysi8s/pyftdi/pyftdi/gpio.pyr   %   s   r   c               @   s   e  Z d  Z d Z d S)�GpioPortz2Duck-type GPIO port for GPIO all controllers.
    N)r   r   r   r   r   r   r   r   r   *   s   r   c               @   s�  e  Z d  Z d Z d d �  Z e e d d d � �  � Z e e d d d � �  � Z	 d	 e
 e e d
 d d � � Z d d �  Z e d d d � �  Z e e d d d � �  � Z e e d d d � �  � Z e e d d d � �  � Z e e d d d � �  � Z e e d d d � �  � Z e e e f d d d d � �  Z e e d d d  d! � �  Z d e
 e e e e d f e d" d# d$ � � Z d d d% d& � �  Z d S)'�GpioBaseControllerz�GPIO controller for an FTDI port, in bit-bang legacy mode.

       GPIO bit-bang mode is limited to the 8 lower pins of each GPIO port.
    c             C   s4   t  �  |  _ d |  _ d |  _ d |  _ d |  _ d  S)Nr   )r	   �_ftdi�
_direction�_width�_mask�
_frequency)�selfr   r   r   �__init__5   s
    			zGpioBaseController.__init__)�returnc             C   s   |  j  S)zIReturn the Ftdi instance.

           :return: the Ftdi instance
        )r   )r   r   r   r   �ftdi<   s    zGpioBaseController.ftdic             C   s
   |  j  j S)z{Reports whether a connection exists with the FTDI interface.

           :return: the FTDI slave connection status
        )r   �is_connected)r   r   r   r   r   D   s    zGpioBaseController.is_connectedr   )�url�	directionr   c             K   s�   |  j  r t d � � t | � } | j d d � } | d k rQ | j d d � } x! d D] } | | k rX | | =qX W|  j | | | | � |  _ d S)a�  Open a new interface to the specified FTDI device in bitbang mode.

           :param str url: a FTDI URL selector
           :param int direction: a bitfield specifying the FTDI GPIO direction,
                where high level defines an output, and low level defines an
                input
           :param initial: optional initial GPIO output value
           :param pace: optional pace in GPIO sample per second
           :return: actual bitbang pace in sample per second
        zAlready connected�	frequencyN�baudrater    �sync)r    r#   r!   r"   )r   r
   �dict�get�
_configurer   )r   r   r    �kwargsr!   �kr   r   r   �	configureL   s    	zGpioBaseController.configurec             C   s   |  j  j r |  j  j �  d S)z"Close the FTDI interface.
        N)r   r   �close)r   r   r   r   r*   c   s    zGpioBaseController.closec             C   s   |  S)z�Retrieve the GPIO port.

           This method is mostly useless, it is a wrapper to duck type other
           GPIO APIs (I2C, SPI, ...)

           :return: GPIO port
        r   )r   r   r   r   �get_gpioi   s    zGpioBaseController.get_gpioc             C   s   |  j  S)z�Reports the GPIO direction.

          :return: a bitfield specifying the FTDI GPIO direction, where high
                level reports an output pin, and low level reports an input pin
        )r   )r   r   r   r   r    s   s    zGpioBaseController.directionc             C   s   |  j  S)z�Report the configured GPIOs as a bitfield.

           A true bit represents a GPIO, a false bit a reserved or not
           configured pin.

           :return: always 0xFF for GpioController instance.
        )r   )r   r   r   r   �pins|   s    	zGpioBaseController.pinsc             C   s   |  j  S)z�Report the addressable GPIOs as a bitfield.

           A true bit represents a pin which may be used as a GPIO, a false bit
           a reserved pin

           :return: always 0xFF for GpioController instance.
        )r   )r   r   r   r   �all_pins�   s    	zGpioBaseController.all_pinsc             C   s   |  j  S)zdReport the FTDI count of addressable pins.

           :return: the width of the GPIO port.
        )r   )r   r   r   r   �width�   s    zGpioBaseController.widthc             C   s   |  j  S)z[Return the pace at which sequence of GPIO samples are read
           and written.
        )r   )r   r   r   r   r!   �   s    zGpioBaseController.frequencyN)r!   r   c             C   s   t  d � � d S)z�Set the frequency at which sequence of GPIO samples are read
           and written.

           :param frequency: the new frequency, in GPIO samples per second
        z)GpioBaseController cannot be instanciatedN)�NotImplementedError)r   r!   r   r   r   �set_frequency�   s    z GpioBaseController.set_frequency)r,   r    r   c             C   sL   | |  j  k r t d � � |  j | M_ |  j | | @O_ |  j �  d S)a4  Update the GPIO pin direction.

           :param pins: which GPIO pins should be reconfigured
           :param direction: a bitfield of GPIO pins. Each bit represent a
                GPIO pin, where a high level sets the pin as output and a low
                level sets the pin as input/high-Z.
        zInvalid direction maskN)r   r   r   �_update_direction)r   r,   r    r   r   r   �set_direction�   s
    z GpioBaseController.set_direction)r   r    r!   r   c             K   s   t  d � � d  S)Nz)GpioBaseController cannot be instanciated)r/   )r   r   r    r!   r'   r   r   r   r&   �   s    zGpioBaseController._configurec             C   s   t  d � � d  S)NzMissing implementation)r/   )r   r   r   r   r1   �   s    z$GpioBaseController._update_direction)r   r   r 