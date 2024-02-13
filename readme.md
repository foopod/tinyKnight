![](title.png)

tinyKnight is a simple game made for micropython on the Cardputer.

## Installation

This uses the S3LCD driver in micropython for best performance of the LCD, so for this game to work you need to be on this particular micropython firmware...
https://github.com/russhughes/s3lcd/tree/main/firmware/ESP32_GENERIC_S3_8MiB

Then just drag and drop the files from the `tinyKnight` folder in this repo to your cardputer (but you don't need the readme or knight_sprites.png).

## To-do

- Display a score in the top right
- Display score and high score on death
- Handle death properly (at the moment you must reset the device)
- Powerups (temp invincibility, speed boost, etc)