from machine import Pin, SPI
import knight_sprites as knight_bitmap
import time
import keyboard
import tft_config
import s3lcd
import vga1_bold_16x32 as big_font
import vga1_8x8 as small_font
import random

class Obstacle:
    def __init__(self):
        self.col = 238
        self.row = 100
        self.width = 16
        self.height = 28
        self.color = s3lcd.WHITE
        self.overshoot = random.randint(4, 60)
        self.speed = 7
        self.count = 0

    def move(self):
        self.col -= self.speed
        if self.col < - self.width - self.overshoot:
            self.col = 240 + self.width
            self.randomize()
            self.count +=1
            if self.count > 10:
                self.count = 0
                self.speed +=1
            
    def randomize(self):
        self.width = random.randint(4,20)
        self.height = random.randint(12,32)
        self.row = 128 - self.height
        self.color = random.getrandbits(16)
        self.overshoot = random.randint(4, 60)
    
    def draw(self):
        tft.fill_rect(self.col, self.row, self.width, self.height, self.color)

class Knight:
    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.col = 1
        self.row = 100
        self.width = bitmap.WIDTH
        self.height = bitmap.HEIGHT
        self.frame = 0
        self.y_velocity = 0
        self.grounded = True
        self.buffered_jump = False
        self.dead = False
        self.visible = True
        
        # used in the opening
        self.introComplete = False
        self.inCollision = False
        self.inTransition = False
        self.waitingForInput = False
        
    def animateOpening(self):
        if self.inTransition:
            # slide everything left
            self.col -= 2
            if self.col < 10:
                self.col = 10
                self.inTransition = 0
                self.introComplete = True
            return
        
        if self.inCollision:
            self.row += self.y_velocity
            self.y_velocity += 3
            if self.row > 100:
                self.row = 100
                self.inCollision = False
                self.waitingForInput = True
            return
        
        if not self.waitingForInput:
            if self.col < 224:
                # no collision yet
                self.col += 2
                self.frame += 1
                if self.frame > 3:
                    self.frame = 0
            else:
                self.inCollision = True
                self.y_velocity = -10
                self.col = 224
                self.frame = 4
            
        
        
    def move(self, obstacle):
        if not self.visible:
            return
        # y position    
        if not self.grounded or self.dead:
            if self.row + self.y_velocity > 100 and not self.dead:
                # would touch ground next frame
                self.row = 100
                self.y_velocity = 0
                self.grounded = True
                
                if self.buffered_jump and not self.dead:
                    self.jump()
                    self.buffered_jump = False
            elif self.row + self.y_velocity > 100 and self.dead:
                self.visible = False
            else:
                self.row += self.y_velocity
                self.y_velocity += 3
        
        # check death
        if (
            self.col < obstacle.col + obstacle.width and
            self.col + self.width > obstacle.col and
            self.row < obstacle.row + obstacle.height and
            self.row + self.height > obstacle.row
          ) :
            self.dead = True
            self.y_velocity = -20
            
            
        # animation
        if self.dead:
            self.frame = 4
        elif self.grounded:
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        else:
            self.frame = 1
        
    def jump(self):
        if not self.visible:
            return
        if self.grounded:
            self.y_velocity = -20
            self.row = 99
            self.grounded = False
        elif self.row > 60:
            self.buffered_jump = True
    
    def draw(self):
        if not self.visible:
            return
        tft.bitmap(self.bitmap, self.col, self.row, self.frame)
        
def show_menu(sprite):
    title = "tinyKnight"
    length = len(title)
    
    tft.fill(s3lcd.BLACK)
    tft.text(big_font, title, tft.width() // 2 - length // 2 * big_font.WIDTH,
        tft.height() // 2 - big_font.HEIGHT)
    
    tft.show()
    
    play_game = False
    
    while not play_game:
        pressed_keys = kb.get_pressed_keys()
        if pressed_keys != prev_pressed_keys:
            if "ENT" in pressed_keys and "ENT" not in prev_pressed_keys: # up arrow
                sprite.inTransition = True
                sprite.waitingForInput = False
        
        if sprite.introComplete:
            play_game = True
                
        sprite.animateOpening()
        tft.fill(s3lcd.BLACK)
        tft.text(big_font, title, tft.width() // 2 - length // 2 * big_font.WIDTH,
            tft.height() // 2 - big_font.HEIGHT)
        tft.hline(0, 128, 240, s3lcd.WHITE)
        if sprite.waitingForInput:
            tft.text(small_font, "ok to start", 126, 116)
        sprite.draw()
        tft.show()
    
tft = tft_config.config(tft_config.WIDE)  # configure display
tft.init()
tft.fill(s3lcd.BLACK)
tft.show()

kb = keyboard.KeyBoard()
pressed_keys = []
prev_pressed_keys = []

sprite = Knight(knight_bitmap)

obstacle = Obstacle()

show_menu(sprite)
    

while True:
    pressed_keys = kb.get_pressed_keys()
    if pressed_keys != prev_pressed_keys:
        if ";" in pressed_keys and ";" not in prev_pressed_keys: # up arrow
            sprite.jump()
            
    prev_pressed_keys = pressed_keys
    
    tft.fill(s3lcd.BLACK)
    tft.hline(0, 128, 240, s3lcd.WHITE)
    
    sprite.move(obstacle)
    obstacle.move()
    
    sprite.draw()
    obstacle.draw()
    tft.show()
    
    time.sleep(0.03)