'''
main.py
by Suraj Rampure
Started on April 30, 2014
Submitted on June 16, 2014

Fruit Surge - ICS3U Final Project
This is my replica of Fruit Ninja's Arcade Mode. This version features no frills (bombs, powerups, etc.) -- pure fruit slicing.
The user, with their supplied knife, must cut as many fruits as they can in one minute.

'''

#Module imports
from __future__ import division
from pygame import *
from math import *
from random import randint, choice, uniform
from time import localtime as local
from time import time as clock
import datetime

#Initializations
init()
mixer.init()
font.init()

#Time object that helps get and set FPS
fps = time.Clock()

#Creating the display surface, setting the caption and icon
width, height = 1280,720
screen = display.set_mode((width, height))
display.set_caption("Fruit Surge")
icon = transform.scale(image.load("Other Images/Icon.png"), (64, 64))
display.set_icon(icon)

#Opening file for writing high scores
highFile = open("Files/High Scores.txt")
oldHS = int(highFile.read()); highscore = oldHS

#Variable for the current screen
mode = "Splash Screen"

'''Importing and setting up all gameplay images'''
#Importing of core gameplay images - fruits and "bits" (fallen halves)
    #The dimensions of these images are doubled (the real images look 8-bit so I can scale without pixelation)
apple_main = transform.scale(image.load("Fruit Images/apple.png"), (128, 128)).convert()
apple_bit1 = transform.scale(image.load("Fruit Images/applebit1.png"), (36, 48)).convert()
apple_bit2 = transform.scale(image.load("Fruit Images/applebit2.png"), (44, 68)).convert()

banana_main = transform.scale(image.load("Fruit Images/banana.png"), (128, 128)).convert()
banana_bit1 = transform.scale(image.load("Fruit Images/bananabit1.png"), (56, 56)).convert()
banana_bit2 = transform.scale(image.load("Fruit Images/bananabit2.png"), (92, 62)).convert()

coconut_main = transform.scale(image.load("Fruit Images/coconut.png"), (128, 128)).convert()
coconut_bit1 = transform.scale(image.load("Fruit Images/coconutbit1.png"), (74, 102)).convert()
coconut_bit2 = transform.scale(image.load("Fruit Images/coconutbit2.png"), (64, 100)).convert()

lemon_main = transform.scale(image.load("Fruit Images/lemon.png"), (128, 128)).convert()
lemon_bit1 = transform.scale(image.load("Fruit Images/lemonbit1.png"), (76, 70)).convert()
lemon_bit2 = transform.scale(image.load("Fruit Images/lemonbit2.png"), (74, 84)).convert()

pear_main = transform.scale(image.load("Fruit Images/pear.png"), (128, 128)).convert()
pear_bit1 = transform.scale(image.load("Fruit Images/pearbit1.png"), (56, 66)).convert()
pear_bit2 = transform.scale(image.load("Fruit Images/pearbit2.png"), (36, 68)).convert()

watermelon_main = transform.scale(image.load("Fruit Images/watermelon.png"), (128, 128)).convert()
watermelon_bit1 = transform.scale(image.load("Fruit Images/watermelonbit1.png"), (84, 98)).convert()
watermelon_bit2 = transform.scale(image.load("Fruit Images/watermelonbit2.png"), (128, 132)).convert()

#Correlating the fruit types with their respective images in dictionaries
Fruit_Images = {"apple": apple_main, "banana": banana_main, "coconut": coconut_main, "lemon": lemon_main, \
                "pear": pear_main, "watermelon": watermelon_main}

Bit_Images1 = {"apple": apple_bit1, "banana": banana_bit1, "coconut": coconut_bit1, "lemon": lemon_bit1, \
               "pear": pear_bit1, "watermelon": watermelon_bit1}

Bit_Images2 = {"apple": apple_bit2, "banana": banana_bit2, "coconut": coconut_bit2, "lemon": lemon_bit2, \
               "pear": pear_bit2, "watermelon": watermelon_bit2}

#Putting all core gameplay images in a list just so that I can change the alpha in a for loop quickly
imgs = [apple_main, apple_bit1, apple_bit2, banana_main, banana_bit1, banana_bit2, 
        coconut_main, coconut_bit1, coconut_bit2, lemon_main, lemon_bit1, lemon_bit2, 
        pear_main, pear_bit1, pear_bit2, watermelon_main, watermelon_bit1, watermelon_bit2]

#Every bit image has an alpha of 160, every splash image has an alpha of 100 and every fruit image is untouched
for img in imgs:
    img.set_colorkey((0, 0, 0))
    if imgs.index(img) % 3 == 0:
        img.set_alpha(250)
    else:
        img.set_alpha(125)

#Importing of game wallpaper images and setting the game text colours for each respective wallpaper
wall1 = image.load("Wallpapers/Wallpaper1.png").convert()
wall1.set_alpha(255)
wall1List = [(0, 0, 0), (235, 61, 0), (0, 0, 0), (247, 237, 0)]     #List of the colours of the score, high score, time and FPS fonts

wall2 = image.load("Wallpapers/Wallpaper2.png").convert()
wall2.set_alpha(150)
wall2List = [(0, 179, 224), (247, 237, 0), (163, 232, 255), (188, 226, 158)]

wall3 = image.load("Wallpapers/Wallpaper3.png").convert()
wall3.set_alpha(255)
wall3List =  [(255, 250, 80), (255, 255, 255), (98, 222, 253), (244, 101, 36)]

wall4 = image.load("Wallpapers/Wallpaper4.png").convert()
wall4.set_alpha(255)
wall4List = [(247, 237, 0), (0, 0, 0), (245, 182, 203), (98, 222, 253)]

#Sets the default wallpaper to wall1 and changes the text colours list to wall1List (can be changed in game)
wallpaper = wall3
wallList = wall3List

#Importing the images for the knife blades in the game
kitchenblade = transform.scale(image.load("Other Images/KitchenBlade.png"), (128, 128))
fightingblade = transform.scale(image.load("Other Images/FightingBlade.png"), (128, 128))
blade = "kitchen"

blades = {"kitchen": kitchenblade, "fighting": fightingblade}

#Indexes of the respective colours (score, HS, time, FPS)
colS = 0
colHS = 1
colT = 2
colFPS = 3

#Loading of other screens in game (credits, options, pause menu, etc.)
load_screen = image.load("Screens/PythonLoader.png").convert()

splash_screen = image.load("Screens/Loading Screen.png").convert()

credits_screen = image.load("Screens/Credits.png").convert()

options_screen = image.load("Screens/Options.png").convert()

customize_screen = image.load("Screens/Options_Customize.png").convert()

gameover_screen = image.load("Screens/Game Over.png").convert()

paused_screen = image.load("Screens/Paused.png").convert()

'''Importing Sound Effects and Background Music'''
#Sound effects
Press = mixer.Sound("Sounds/Press.wav"); Press.set_volume(0.5)
Tick = mixer.Sound("Sounds/Tick.wav"); Tick.set_volume(0.5)
Punch = mixer.Sound("Sounds/Punch.wav"); Punch.set_volume(0.5)
Splash = mixer.Sound("Sounds/Splash.wav"); Splash.set_volume(0.5)
Woosh = mixer.Sound("Sounds/Woosh.wav"); Woosh.set_volume(0.5)

#Background music
    #Each piece is exactly one minute long, and the music is determined by the current background
song1 = mixer.Sound("Sounds/Pompeii.wav"); song1.set_volume(0.25)
song2 = mixer.Sound("Sounds/All I Do Is Win.wav"); song2.set_volume(0.25)
song3 = mixer.Sound("Sounds/Animals.wav"); song3.set_volume(0.25)
song4 = mixer.Sound("Sounds/Wipe Out.wav"); song4.set_volume(0.25)
song = song3                #Since the default wallpaper is wall3, the default song must be song3

'''Importing fonts'''
#The only font used is Avenir, however I created three objects with Avenir, each a different size
smallFont = font.Font("Fonts/Avenir.ttc", 18)
medFont = font.Font("Fonts/Avenir.ttc", 40)
largeFont = font.Font("Fonts/Avenir.ttc", 60)

'''Function definitions'''
#Returns mouse position
def mp():   
    return mouse.get_pos() 

#Returns state of the left mouse button
def lclick():   
    if mouse.get_pressed()[0] == 1:
        return True
    else:
        return False

#Collision function for the fruits, either a circle (most fruits) or rectangle (banana only)
def collide(col_type, basepoint, movepoint, len1, len2 = None):

    #If the distance between the mouse and coordinates of the middle of the fruit are 
    #less than or equal to the radius of the circle wrapping around the fruit AND the
    #left mouse button is down, then the fruit is said to be colliding with the mouse
    #and the function returns True (False otherwise)
    if col_type == "circle":
        bx, by = basepoint
        mx, my = movepoint 
        if ((bx-mx)**2 + (by-my)**2)**0.5 <= len1 and lclick() == True:
            return True
        else:
            return False

    elif col_type == "rect":
        bx, by = basepoint
        mx, my = movepoint
        collideRect = Rect (bx-len1//2,by-len2//2,len1, len2)
        if collideRect.collidepoint((mx,my)) and lclick() == True:
            return True
        else:
            return False

#In the program, a Fruit object can have one of six types; 
#this function randomly returns one of them (we want the probability of all fruits appearing in the game to be equal)
def randfruit():
    fruits = ["apple", "banana", "coconut", "lemon", "pear", "watermelon"]
    return choice(fruits)

'''Setting up object classes'''
#Dictionary of the collision radiuses of all fruits
    #Note: The banana does not use this dictionary, it uses the Rect collision mode
CollisionRadius = {"apple": 35, "banana": 64, "coconut": 40, "lemon": 50, "pear": 40, "watermelon": 50}

#List of the options of x starting values
    #I wanted the majority of fruits to start in the middle half of the screen with less fruits starting on the left
    #and even less starting on the right: Three individual lists are added together here
x_choices = [x for x in range (0,width//4+1,2)] + [x for x in range (width//4, 3*width//4 + 1)] + [x for x in range (3*width//4, width+1,40)]

#Class Fruit: Contains all Fruits that have not yet been sliced, while they are on the screen
class Fruit:
    def __init__ (self, fruit_type, loading = False):
        self.x, self.y = choice(x_choices), height + 1

        self.fruit_type = fruit_type

        self.dist = abs(self.x - width//2)

        #The x velocity is proportionate to the horizontal distance to the middle of the screen
        self.vx = self.dist//70

        #The y velocity is a random floating point value between 7 and 8
        self.vy = uniform (7,8)

        self.angle = 0

        #1 means moving from left to right, -1 means moving from right to left
        if self.x > width//2: 
            self.direction = -1

        elif 0 <= self.x <= width//4:
            self.direction = 1
            
        else:
            self.direction = choice ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1])

        if self.fruit_type == "banana":
            self.collide_type = "rect"
        else:
            self.collide_type = "circle"

        self.draw_image = transform.rotate(Fruit_Images[self.fruit_type], self.angle)
        self.dx, self.dy = int(self.x - (self.draw_image.get_width()//2)), int(self.y - (self.draw_image.get_height()//2))

        self.loading = loading #In the loading screen we don't want gravity to be in effect, the default however is that it is in effect

    #Updates the x,y coordinates of the fruit object as well as the angle and drawing image
    def updatePos(self):

        #On the splash screen, the x and y coordinates of the fruits aren't supposed to change
        #By default loading is False, however while creating the splash screen fruits loading is True
        if self.loading == False:
            self.vy -= 0.07

            self.x += int(self.vx*self.direction)
            self.y -= int(self.vy)

        #Adds by self.direction so that the fruits rotate the same way they're moving
            #Multiplies by choice of this list so that the fruits occasionally rotate faster
        self.angle += self.direction*choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3]) 

        self.draw_image = transform.rotate(Fruit_Images[self.fruit_type], self.angle)

        #By creating dx and dy, x and y are at the center of the fruit image and we can draw circles for collision
        self.dx, self.dy = int(self.x - (self.draw_image.get_width()//2)), int(self.y - (self.draw_image.get_height()//2))        

    def checkCollide(self):
        if self.fruit_type != "banana":
            if collide(self.collide_type, (self.x, self.y), mp(), CollisionRadius[self.fruit_type]) == True:
                return True
            else:
                return False
        else:
            if collide(self.collide_type, (self.x, self.y), mp(), self.draw_image.get_width(), self.draw_image.get_height()) == True:
                return True
            else:
                return False             #True means colliding, False means not colliding

    #Simply draws the fruit image
    def drawFruit(self, surf):
        surf.blit(self.draw_image, (self.dx, self.dy))
        
    #Makes the corresponding sound if the fruit is sliced ("punch" for bananas, "woosh" otherwise)
    def makeSound(self):
        if self.fruit_type == "banana":
            Punch.play()
        else:
            Woosh.play()

air = []    #List of everything in the air
cut = []    #List of fruits that have already been cut

for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
    air.append(Fruit(randfruit()))

#After fruits are cut, "Bits" takes in the fruit type, coordinates and angle of rotation and creates
#a path for the two halves to fall after
class Bits:
    def __init__ (self, bit_type, startx, starty, ang, vy):
        self.bit_type = bit_type
        self.x1, self.x2, self.y = startx, startx, starty

        self.angle = ang

        self.vx = uniform (3, 4)        #Random x velocity
        self.vy = vy                    #The halves follow the same y velocity as the original fruit

        self.draw_image1 = transform.rotate (Bit_Images1[self.bit_type], self.angle)
        self.draw_image2 = transform.rotate (Bit_Images2[self.bit_type], self.angle)

    def updatePos(self):
        self.vy += 0.3                  #Positive because the sliced fruit bits are falling down

        self.x1 -= self.vx              #One half goes to the left, one to the right
        self.x2 += self.vx
        self.y += self.vy

        self.draw_image1 = transform.rotate (Bit_Images1[self.bit_type], self.angle)
        self.draw_image2 = transform.rotate (Bit_Images2[self.bit_type], self.angle)


    def drawBits(self, surf):
        surf.blit(self.draw_image1, (int(self.x1), int(self.y)))
        surf.blit(self.draw_image2, (int(self.x2), int(self.y)))  


#Makes the back, pause, customize, sounds buttons objects
#Allows the program to easy determine which button state to draw
#and if to change the mode to the button's destination
class Button:
    def __init__ (self, rect, up, down, click = None):
        self.rect = rect
        self.up = up           #Up and down are simply the different button states
        self.down = down

        if click != None:
            self.click = click 

    #If the mouse is simply over the button, this returns true to draw the "Down" image
    def checkHover(self):
        if self.rect.collidepoint(mp()):
            return True
        else:
            return False

    #If the button is being clicked, this returns True
    def checkClicked(self):
        if self.checkHover() == True and lclick():
            return True
        else:
            return False

    def drawButton(self, surf):
        surf.blit(self.up, (self.rect.x, self.rect.y))
        if self.checkHover() == True:
            surf.blit(self.down, (self.rect.x, self.rect.y))

        #If the button has a clicked image (not of all them do), then it is blitted if the button is clicked
        elif hasattr(self, "click") and self.checkClicked() == True:
            surf.blit(self.click, (self.rect.x, self.rect.y))

#Class: Blade
#There will only be one blade object in the game, the current blade
    #However I thought it would be easiest to create an object class for the blade so that I could track
    #its current orientation and image type
class Blade:
    def __init__(self, blade_type):
        self.blade_type = blade_type
        self.original_image = blades[self.blade_type]

    def updateBlade(self, pos):
        x = pos[0]
        if x >= width//2:
            self.draw_image = transform.rotate(self.original_image, 45)
        else:
            self.draw_image = transform.rotate(self.original_image, 45)
            self.draw_image = transform.flip(self.draw_image, True, False)
        return self.draw_image

    def drawBlade(self, surf, pos):
        x = pos[0]
        if x < width//2:
            surf.blit(self.updateBlade(pos), (pos[0] - self.updateBlade(pos).get_width()//2 - 50, pos[1] - self.updateBlade(pos).get_height()//2 + 50))
        else:
            surf.blit(self.updateBlade(pos), (pos[0] - 40, pos[1] - self.updateBlade(pos).get_height()//2 + 50))

'''Creating buttons'''
#Buttons for the four wallpaper options on the options/customize screen
Wall1_Button = Button(Rect (138, 396, 467, 72), image.load("Buttons/Wall1Up.png").convert(), \
        image.load("Buttons/Wall1Down.png").convert(), image.load("Buttons/Wall1Click.png").convert())

Wall2_Button = Button(Rect (675, 396, 467, 72), image.load("Buttons/Wall2Up.png").convert(), \
        image.load("Buttons/Wall2Down.png").convert(), image.load("Buttons/Wall2Click.png").convert())

Wall3_Button = Button(Rect (138, 492, 467, 72), image.load("Buttons/Wall3Up.png").convert(), \
        image.load("Buttons/Wall3Down.png").convert(), image.load("Buttons/Wall3Click.png").convert())

Wall4_Button = Button(Rect (675, 492, 467, 72), image.load("Buttons/Wall4Up.png").convert(), \
        image.load("Buttons/Wall4Down.png").convert(), image.load("Buttons/Wall4Click.png").convert())

#Buttons for the two different types of knives on the options/customize screen
Kitchen_Button = Button(Rect (138, 630, 467, 72), image.load("Buttons/KitchenUp.png").convert(), \
        image.load("Buttons/KitchenDown.png").convert())

Fighting_Button = Button(Rect (675, 630, 467, 72), image.load("Buttons/FightingUp.png").convert(), \
        image.load("Buttons/FightingDown.png").convert())

Done_Button = Button(Rect (50, 50, 150, 50), image.load("Buttons/DoneUp.png").convert(), \
        image.load("Buttons/DoneDown.png").convert())

Pause_Button = Button(Rect (50, 650, 150, 50), image.load("Buttons/PauseUp.png").convert(), \
        image.load("Buttons/PauseDown.png").convert())

Customize_Button = Button(Rect (406, 431, 467, 72), image.load("Buttons/CustomizeUp.png").convert(), \
        image.load("Buttons/CustomizeDown.png").convert())

Sound_Button = Button(Rect (406, 551, 467, 72), image.load("Buttons/SoundUp.png").convert(), \
        image.load("Buttons/SoundDown.png").convert())

PlayAgain_Button = Button(Rect (787, 428, 467, 72), image.load("Buttons/PlayAgainUp.png").convert(), \
        image.load("Buttons/PlayAgainDown.png").convert())

MainMenu_Button = Button(Rect (787, 526, 467, 72), image.load("Buttons/MainMenuUp.png").convert(), \
        image.load("Buttons/MainMenuDown.png").convert())

Quit_Button = Button(Rect (787, 624, 467, 72), image.load("Buttons/QuitUp.png").convert(), \
        image.load("Buttons/QuitDown.png").convert())

'''Creating blade'''
blade = Blade("kitchen")

'''Defining the functions for each screen'''
#Each possible screen (credits, options, pause, game) has its own function

#Splash screen
def splashScreen():
    global oldSec, oldMin, startSec, secLeft, mode, game

    splashChoice = None
    drawSplashBits = False

    #For these three fruit objects, "loading" is set to True: we don't want the x and y values to update
    splashFruits = [Fruit("banana", True), Fruit("apple", True), Fruit("watermelon", True)]
    for fruit in splashFruits:
        #This centers the fruit coordinates on the three photoshopped circles
        fruit.x = 653 + 225*splashFruits.index(fruit) + 64
        fruit.y = 394 + 64
        fruit.vx, fruit.vy = 0, 0

    #Dictionaries of the fruit on the splash screen and the respective screens they lead to
    modes = {"banana": "Credits", "apple": "Play", "watermelon": "Options"}

    running = True

    #Same for the main() function: we are replacing the mouse with a knife therefore the cursor should be invisible
    mouse.set_visible(False)

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        #Updating fruit positions
        for fruit in splashFruits:
            fruit.updatePos()

        #Updating bit positions
        if drawSplashBits == True:
            splashChoice.updatePos()

        #If the bits fall off the screen, the mode is updated
        if drawSplashBits == True:
            if splashChoice.y > height:
                mode = modes[splashChoice.bit_type]
                if mode == "Play":
                    oldSec = local(clock())[5]
                    oldMin = local(clock())[4]
                    secLeft = 60

                    air = []    #List of everything in the air
                    cut = []    #List of fruits that have already been cut

                    for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
                        air.append(Fruit(randfruit()))
                    song.play()

                running = False
                drawBits = False

        #Checking for collisions 
        #splashChoice is whichever fruit they sliced; we need to stop drawing it as a normal fruit as it will only be drawn as bits
        for fruit in splashFruits:
            if fruit.checkCollide() == True:
                fruit.makeSound()
                splashChoice = Bits(fruit.fruit_type, fruit.x, fruit.y, fruit.angle, uniform(0.5, 1.5))
                del splashFruits[splashFruits.index(fruit)]
                drawSplashBits = True

        #Drawing everything
        screen.blit(splash_screen, (0,0))

        for fruit in splashFruits:
            fruit.drawFruit(screen)

        #Only draws the bits while they are above the screen
        if drawSplashBits == True:
            if splashChoice.y < height:
                splashChoice.drawBits(screen)

        blade.drawBlade(screen, mp())

        display.flip()

        fps.tick(60)  

    return mode

#Credits menu, accessed by swiping the banana on the splash screen
def creditsMenu():
    mouse.set_visible(True)
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        if Done_Button.checkClicked() == True:
            running = False

        screen.blit(credits_screen, (0, 0))

        Done_Button.drawButton(screen)
            
        display.flip()

    return "Splash Screen"

#Pause menu, accessed while playing the game
def pauseScreen():
    global mode, song, secLeft, pauseTime, score
    mouse.set_visible(True)
    mixer.pause()
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        if Done_Button.checkClicked() == True:
            running = False

        #If we don't reset score to 0, it will use the oldest score still
        if MainMenu_Button.checkClicked() == True:
            score = 0
            return "Splash Screen"

        if Quit_Button.checkClicked() == True:
            return "exit"

        screen.blit(paused_screen, (0, 0))

        Done_Button.drawButton(screen)

        MainMenu_Button.drawButton(screen)
        Quit_Button.drawButton(screen)
        
        display.flip()

    #We need to unpause the music and feed the secLeft value back to what it was before pausing
    mixer.unpause()
    secLeft = pauseTime
    return "Play"
    
#Options menu
def optionsScreen():
    global wallpaper, wallList, blade, song
    buttons = [Wall1_Button, Wall2_Button, Wall3_Button, Wall4_Button]
    wallpapers = [wall1, wall2, wall3, wall4]
    lists = [wall1List, wall2List, wall3List, wall4List]
    songs = [song1, song2, song3, song4]

    mouse.set_visible(True)

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        for button in buttons:
            if button.checkClicked() == True:
                wallpaper = wallpapers[buttons.index(button)]
                wallList = lists[buttons.index(button)]
                song = songs[buttons.index(button)]

        if Kitchen_Button.checkClicked() == True:
            blade = Blade("kitchen")

        if Fighting_Button.checkClicked() == True:
            blade = Blade("fighting")

        if Done_Button.checkClicked() == True:
            running = False 

        screen.blit(customize_screen, (0, 0))

        for button in buttons:
            if wallpaper == wallpapers[buttons.index(button)]:
                screen.blit(button.down, (button.rect.x, button.rect.y))
            else:
                button.drawButton(screen)

        if blade.blade_type == "kitchen":
            screen.blit(Kitchen_Button.down, (Kitchen_Button.rect.x, Kitchen_Button.rect.y))
        else:
            Kitchen_Button.drawButton(screen)

        if blade.blade_type == "fighting":
            screen.blit(Fighting_Button.down, (Fighting_Button.rect.x, Fighting_Button.rect.y))
        else:
            Fighting_Button.drawButton(screen)

        Done_Button.drawButton(screen)

        display.flip()

    return "Splash Screen"

#Screen that appears after the game is over to ask the user if they want to quit, play again or go to main menu
def afterScreen():
    global score, oldSec, oldMin, secLeft, air, cut, wallList, oldScore
    mouse.set_visible(True)
    startCount = 0         #Want to make sure that the user doesn't accidentally click start right after a game; 
                            #I am making a counter such that after a certain point the user can make a selection

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        startCount += 1
        if startCount >= 120:

            if PlayAgain_Button.checkClicked() == True:
                #We must re-setup the core game variables as they have been altered in the past session
                oldSec = local(clock())[5]
                oldMin = local(clock())[4]

                air = []
                cut = []
                for i in range (choice([1, 1, 2, 2, 2, 3, 3, 4, 5])):
                    air.append(Fruit(randfruit()))

                song.play()
                return "Play"

            if MainMenu_Button.checkClicked() == True:
                return "Splash Screen"

            if Quit_Button.checkClicked() == True:
                return "exit"

        screen.blit(gameover_screen, (0, 0))

        scoreBlit = largeFont.render("Score: " + str(oldScore), True, wallList[colS])
        screen.blit(scoreBlit, (950, 350))

        PlayAgain_Button.drawButton(screen)
        MainMenu_Button.drawButton(screen)
        Quit_Button.drawButton(screen)


        display.flip()

#Function for the actual game
score = 0         #The score begins outside of the function because when we return to main() after going to pause, we want the score to be retained
def main():

    count = False
    counter = 0
    counter2 = 0

    #All of these variables had to be defined before the actual main() function so that they would not be reset
        #once we return to the function after pausing
    global mode, song, secLeft, oldSec, oldMin, pauseTime, air, cut, score, blade, oldScore

    mouse.set_visible(False)

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        'Updating fruit positions'
        for fruit in air:
            fruit.updatePos()

        'Updating bit positions'
        for bit in cut:
            bit.updatePos()

        'Interactions'
        #In case the user pauses for exactly a minute and they return back to the exact same second, we don't want the program to glitch out
        	#Instead, I created two "if" options: if the current second value doesn't equal the previous recorded second value OR the current second value equals
        	#the previous recorded second value however the minutes are different, then the seconds left counter should be decreased
        if local(clock())[5] != oldSec or (local(clock())[4] != oldMin and local(clock())[5] == oldSec):
        	secLeft -= 1
        	oldSec = local(clock())[5] 
        	oldMin = local(clock())[4]

        if secLeft <= 0:
            endScore = score
            running = False

        #After a fruit is cut, we want to randomly add more
        if count == True:
            counter += 1
        if count == False:
            counter = 0

        #Adding more based on a random time after a fruit is cut
        if counter >= choice ([10, 20, 20, 30, 30, 30, 50, 50, 100, 100, 100, 200, 200, 300]):
            for i in range (choice([1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5])):
                air.append(Fruit(randfruit()))
                count = False

        #We also want more fruits to appear even if the player isn't slicing: this randomly
        #adds more fruit to the "air" list after an interval of time
        counter2 += 1
        if counter2 >= choice ([100, 100, 100, 200, 200, 300, 300, 400]):
            for i in range (choice([1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5])):
                air.append(Fruit(randfruit()))
                counter2 = 0

        #Determines what the current high score is
        if oldHS > score:
            highscore = oldHS
        else:
            highscore = score

        'Checking for collision'
        for fruit in air:
            if fruit.checkCollide() == True:
                fruit.makeSound()
                if blade.blade_type == "kitchen":
                    point = choice ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])
                    score += point
                else:
                    point = choice ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10])         #The fighting blade gives a higher change of getting 10 points on a slice (user doesn't need to know)
                    score += point
                del air[air.index(fruit)]
                cut.append(Bits(fruit.fruit_type, fruit.x, fruit.y, fruit.angle, fruit.vy))
                count = True

        'Checking if buttons are clicked'
        if Pause_Button.checkClicked() == True:
            pauseTime = secLeft
            return "Pause"

        'Deleting fruits from air list if they are off the screen'
        for fruit in air:
            if fruit.y > height:
                del air[air.index(fruit)]

        '''Drawing'''
        screen.blit(wallpaper, (0, 0))

        #Fruits
        for fruit in air:
            fruit.drawFruit(screen)

        #Bits
        for bit in cut:
            bit.drawBits(screen)

        #Buttons
        Pause_Button.drawButton(screen)

        #Blade
        blade.drawBlade(screen, mp())

        #Seconds left
        if secLeft % 10 == 0 or secLeft <= 9:   #Makes every interval or single digit second light up red
            timeCol = (255, 23, 34)
        else:
            timeCol = wallList[colT]
        secBlit = medFont.render(str(secLeft), True, timeCol)
        screen.blit(secBlit, (width//2 - (secBlit.get_width()//2), 15))

        #Current Score
        scoreBlit = largeFont.render(str(score), True, wallList[colS])
        screen.blit(scoreBlit, (50, 15))

        #High Score
        highBlit = smallFont.render("High Score: " + str(highscore), True, wallList[colHS])
        screen.blit(highBlit, (50, 88))

        #FPS
        fpsBlit = smallFont.render("FPS: " + str(fps.get_fps())[0:2], True, wallList[colFPS])
        screen.blit(fpsBlit, (1190, 15))

        display.flip()

    mouse.set_visible(True)
    mixer.stop()

    #oldScore is the score that will be drawn on the 'after' screen
    #score is set to 0, and secLeft is set to 60 for the next time the user plays
    oldScore = score
    score = 0
    secLeft = 60

    return "After"

#Two second loading screen at the start of the program, I added this simply for effect
    #If the user presses enter or space it is skipped (like in a real game)
def loadingScreen():
    loadCount = 0
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                quit()
                raise SystemExit        #loadingScreen() is not included in the "while" structure; SystemExit also quits the program

        keys = key.get_pressed()

        screen.blit(load_screen, (0, 0))

        if keys[K_RETURN] or keys[K_SPACE]:
                running = False

        loadCount += 1 
        if loadCount >= 120:
                running = False

        display.flip()
        fps.tick(60)
        
    return None

loadingScreen()

#Main game loop
    #Each screen function returns the screen that needs to follow it after it is done

while mode != "exit":           #For every "evt.type == QUIT", each function returns "exit"
                                    #At which point this loop will end, the new high score will be written to and the game will end
    if mode == "Splash Screen":
        mode = splashScreen()

    elif mode == "Play":
        mode = main()

    elif mode == "Pause":
        mode = pauseScreen()

    elif mode == "Credits":
        mode = creditsMenu()

    elif mode == "Options":
        mode = optionsScreen()

    elif mode == "Options_Customize":
        mode = customizeScreen()

    elif mode == "After":
        mode = afterScreen()

#Writing the new high score to file if it is higher than the current high score
if highscore > oldHS:
    highFile = open("Untitled.txt", "w")
    highFile.write(str(highscore))

font.quit()
mixer.quit()
quit()
