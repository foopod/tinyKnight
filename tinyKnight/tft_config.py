""" M5STACK Cardputer 135x240 display """

from machine import Pin, freq
import s3lcd

BL = Pin(38, Pin.OUT)

TFA = 1
BFA = 1
WIDE = 1
TALL = 0

freq(240_000_000)

def config(rotation=0, options=0):
    """Configure the display and return an ESPLCD instance."""

    BL.value(1)

    custom_rotations = (
        (135, 240, 52, 40, False, False, False),
        (240, 135, 40, 53, True, True, False),
        (135, 240, 53, 40, False, True, True),
        (240, 135, 40, 52, True, False, True))

    bus = s3lcd.SPI_BUS(
        2, mosi=35, sck=36, dc=34, cs=37, pclk=40000000, swap_color_bytes=True
    )

    return s3lcd.ESPLCD(
        bus,
        135,
        240,
        inversion_mode=True,
        reset=33,
        rotations=custom_rotations,
        rotation=rotation,
        dma_rows=32,
        options=options,
    )


def deinit(tft, display_off=False):
    """Take an ESPLCD instance and Deinitialize the display."""
    tft.deinit()
    if display_off:
        BL.value(0)
