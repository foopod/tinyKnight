![](title.png)

tinyKnight is a simple game made for micropython on the Cardputer.

## Installation

1. Flash your cardputer with the S3LCD MicroPython firmware (found [here](https://github.com/russhughes/s3lcd/tree/main/firmware/ESP32_GENERIC_S3_8MiB)).
2. Copy the files from the `tinyKnight` folder in this repo to your cardputer using a MicroPython IDE (like Thonny).
3. Turn on the cardputer and the game should start.

## Notes

> Why not use the stock micropython firmware?

The Cardputer uses the ST7789 display driver for its 240x135 LCD. To get the most out of it and play the game at a reasonable framerate we use S3LCD which is a driver written in C and baked into the MicroPython firmware linked above. This performs ~10 times faster than using a similar driver written in Python (like [this](https://github.com/russhughes/st7789py_mpy/)).

> How do I change/edit/update the sprites?

Included in this repo is `sprites2bitmap.py` from the s3lcd library, this will convert the sprites (knight_sprites.png) to python code. To do this just running the command `python sprites2bitmap.py knight_sprites.png 16 28 3 > tinyKnight/knight_sprites.py` will update the sprites. Feel free to have fun, change the colour of our tinyKnight or make your own character to play with.

## To-do

- Save high scores (maybe even publish online)
- Powerups (temp invincibility, speed boost, etc)
