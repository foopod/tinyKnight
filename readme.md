![](title.png)

tinyKnight is a simple game made for micropython on the Cardputer.

## Installation

1. Flash your cardputer with the S3LCD MicroPython firmware (found [here](https://github.com/russhughes/s3lcd/tree/main/firmware/ESP32_GENERIC_S3_8MiB)).
2. Copy the files from the `tinyKnight` folder in this repo to your cardputer using a MicroPython IDE (like Thonny).
3. Turn on the cardputer and the game should start.

## FAQ

> Why not a different micropython firmware?

The Cardputer uses the ST7789 display driver for its 240x135 LCD. To get the most out of it and play the game at a reasonable framerate we use S3LCD which is a driver written in C and baked into the MicroPython firmware linked above. This performs ~10 times faster than using a similar driver written in Python (like [this](https://github.com/russhughes/st7789py_mpy/)).

## To-do

- Display a score in the top right
- Display score and high score on death
- Handle death properly (at the moment you must reset the device)
- Powerups (temp invincibility, speed boost, etc)
