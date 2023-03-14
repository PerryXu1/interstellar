#################################################################################################
# ██╗███╗░░██╗████████╗███████╗██████╗░░██████╗████████╗███████╗██╗░░░░░██╗░░░░░░█████╗░██████╗░#
# ██║████╗░██║╚══██╔══╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║░░░░░██║░░░░░██╔══██╗██╔══██╗#
# ██║██╔██╗██║░░░██║░░░█████╗░░██████╔╝╚█████╗░░░░██║░░░█████╗░░██║░░░░░██║░░░░░███████║██████╔╝#
# ██║██║╚████║░░░██║░░░██╔══╝░░██╔══██╗░╚═══██╗░░░██║░░░██╔══╝░░██║░░░░░██║░░░░░██╔══██║██╔══██╗#
# ██║██║░╚███║░░░██║░░░███████╗██║░░██║██████╔╝░░░██║░░░███████╗███████╗███████╗██║░░██║██║░░██║#
# ╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝#
#################################################################################################


#=============================================================================#
# Interstellar                                                                #
# Description: Game where you try to dodge obstacles as a spaceship           #
# Author: Perry Xu                                                            #
# Version: 1.0                                                                #
# Date: 23-01-2022                                                            #
#=============================================================================#


# Imports =====================================================================
from random import randint
import pygame
import time
from math import pi, factorial, cos, sin, dist, sqrt, atan, tan
from typing import Union
# import webbrowser

# Initialization ==============================================================
pygame.init()

# gameWindow Initialization ---------------------------------------------------
WIDTH = 1680
HEIGHT= 1080
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

# Colour Initialization -------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPACEBLUE = (24, 19, 41)
RED = (255, 0, 0)
LRED = (255, 50, 50)
BLUE = (0, 0, 255)
LBLUE = (50, 50, 255)
DGREY = (25, 25, 25)
LGREY = (100, 100, 100)

# Image Initialization ---------------------------------------------------
space = pygame.image.load("images/space.png")
space = pygame.transform.scale(space, (WIDTH, HEIGHT))
spaceBackground = pygame.image.load("images/spaceBackground.png")
spaceBackground = pygame.transform.scale(spaceBackground, (2*WIDTH, HEIGHT))
spaceAnimation = pygame.image.load("images/spaceAnimation.png")
spaceAnimation = pygame.transform.scale(spaceAnimation, (2*WIDTH, 2*HEIGHT))

ORIGINALBLACKHOLE = pygame.image.load("images/blackhole.png")
ORIGINALWHITEHOLE = pygame.image.load("images/whitehole.png")

titleImage = pygame.image.load("images/title.png")
titleImage = pygame.transform.scale(titleImage, (round(1018*WIDTH/1680), round(100*HEIGHT/1080)))

ORIGINALship = pygame.image.load("images/rocketshipOff.png")
ORIGINALlaser = pygame.image.load("images/laserBullet.png")
ORIGINALshield = pygame.image.load("images/shieldDisplay.png")

playButtonImage = pygame.image.load("images/play.png")
playButtonImage = pygame.transform.scale(playButtonImage, (round(339*WIDTH/1680), round(100*HEIGHT/1080)))

playButtonImages = [pygame.image.load(f"images/playButton/play{i}.png") for i in range(4)]
for i in range(4):
    playButtonImages[i] = pygame.transform.scale(playButtonImages[i], (round(339*WIDTH/1680), round(100*HEIGHT/1080)))

endlessText = pygame.image.load("images/endless.png")
endlessText = pygame.transform.scale(endlessText, (round(294*WIDTH/1680), round(48*HEIGHT/1080)))

endlessTextHover = pygame.image.load("images/endlessHover.png")
endlessTextHover = pygame.transform.scale(endlessTextHover, (round(294*WIDTH/1680), round(48*HEIGHT/1080)))

campaignText = pygame.image.load("images/campaign.png")
campaignText = pygame.transform.scale(campaignText, (round(336*WIDTH/1680), round(48*HEIGHT/1080)))

campaignTextHover = pygame.image.load("images/campaignHover.png")
campaignTextHover = pygame.transform.scale(campaignTextHover, (round(336*WIDTH/1680), round(48*HEIGHT/1080)))

exitText = pygame.image.load("images/exit.png")
exitText = pygame.transform.scale(exitText, (round(340*WIDTH/1680), round(100*HEIGHT/1080)))

exitTextHover = pygame.image.load("images/exitHover.png")
exitTextHover = pygame.transform.scale(exitTextHover, (round(340*WIDTH/1680), round(100*HEIGHT/1080)))


fireCast = [pygame.image.load(f"images/fireBlast/FireCast{n}.png") for n in range(28)]
for i in range(len(fireCast)):
    fireCast[i] = pygame.transform.scale(fireCast[i], (96+(100*i), 96+(100*i)))

# Font Initialization ---------------------------------------------------------
timeFont = pygame.font.Font("fonts/monogram.ttf", 80)
titleFont = pygame.font.Font("fonts/GravityBold8.ttf", 100)
modeFont = pygame.font.Font("fonts/GravityBold8.ttf", 48)
highscoreFont = pygame.font.Font("fonts/GravityBold8.ttf", 65)

# Sound Initialization --------------------------------------------------------
pygame.mixer.init()

pygame.mixer.music.load("sounds/themeMusic/starman.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

accelerationSound = pygame.mixer.Sound("sounds/spaceshipSounds/engine.mp3")

asteroidExplosion = pygame.mixer.Sound("sounds/obstacleEffects/asteroidEffects/explode.wav")
asteroidExplosion.set_volume(0.15)

collectPowerUp = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/collect.wav")
collectPowerUp.set_volume(0.2)

laserSound = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/laser.wav")
laserSound.set_volume(0.2)

shieldInit = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/shieldPower.wav")
shieldInit.set_volume(0.2)

clearPowerUp = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/clear.wav")
clearPowerUp.set_volume(0.3)

superStarMusic = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/superStar.mp3")
superStarMusic.set_volume(0.3)

shieldDownSound = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/shieldDown.wav")
shieldDownSound.set_volume(0.3)

shieldHitSound = pygame.mixer.Sound("sounds/obstacleEffects/powerUpEffects/shieldHit.wav")
shieldHitSound.set_volume(0.1)

selectionSound = pygame.mixer.Sound("sounds/menuSounds/select.wav")
selectionSound.set_volume(0.3)

deathSound = pygame.mixer.Sound("sounds/spaceshipSounds/death.mp3")
deathSound.set_volume(1)

winSound = pygame.mixer.Sound("sounds/campaignSounds/win.wav")
winSound.set_volume(0.5)

# Game Variables Initialization -----------------------------------------------

# Booleans
menuScreen = True
inPlay = False
campaignMode = False
endlessMode = True
options = False
endScreen = False
isRunning = True
highScore = False
animation = False
fireBlast = False
specialLevel = False
newLevel = True
superNitro = False
infNitro = False
animDecelerate = False
animRotate = False

# Ints
titleEnd = (WIDTH/2-(round(1018*WIDTH/1680)/2)) - 3280
playButtonEnd = (WIDTH/2-(round(195*WIDTH/1680))) - 3280
scorePos = 10000 # set to 10000 at first for initialization
score = 0
highScore1 = 0
shipAngle = 0
shieldAngle = 0
shieldRotationStep = 12
referenceTime1 = 0
cooldown = 0
referenceTime3 = 0
playButtonStage = 0
animVel = 0
elapsed = 0
referenceTime0 = 0
shipX = WIDTH//2
shipY = HEIGHT//2
rotationStep = 10
bhAngle = 0
rotationStepBh = 20
timeInS = 0
stage = 0
blackHoleAngle = 0
backgroundPos = 0
exitRef = 0
collected = 0
maxCollected = 1
level = 1
referenceTime2 = 0
animationPos = 0
collectedScore = 0
hyperdriveIndex = 0

# Lists
asteroids = []
blackHoles = []
powerups = []
collectibles = []

# Keys
keys = pygame.key.get_pressed()

# Classes =====================================================================

# Spaceship class -------------------------------------------------------------
class Spaceship:
    """A user controlled collideable spaceship

    Attributes
        (health) -> int
            an integer that represent the health of the spaceship

        (init_health) -> int
            an integer that represents the initial health of the spaceship

        (acceleration) -> float
            a float that represents the acceleration of the spaceship

        (init_accel) -> float
            a float that represents the initial acceleration of the spaceship

        (spaceShip) -> pygame.Surface
            an image used for the display of the spaceship

        (spaceShipWidth) -> int
            an int that represents the width of the spaceship

        (spaceShipHeight) -> int
            an int that represents the height of the spaceship

        (xVel) -> int
            an int that represents the x-velocity of the spaceship

        (yVel) -> int
            an int that represents the y-velocity of the spaceship

        (xPos) -> int
            an int that represents the x-position of the spaceship

        (yPos) -> int
            an int that represents the y-position of the spaceship

        (x1) -> int
            the x-coordinate of the top left corner of the spaceship

        (x2) -> int
            the x-coordinate of the top right corner of the spaceship

        (x3) -> int
            the x-coordinate of the bottom right corner of the spaceship

        (x4) -> int
            the x-coordinate of the bottom left corner of the spaceship

        (y1) -> int
            the y-coordinate of the top left corner of the spaceship

        (y2) -> int
            the y-coordinate of the top right corner of the spaceship

        (y3) -> int
            the y-coordinate of the bottom right corner of the spaceship

        (y4) -> int
            the y-coordinate of the bottom left corner of the spaceship

        (xCenter) -> int
            the x-coordinate of the center of the spaceship

        (yCenter) -> int
            the y-coordinate of the center of the spaceship

        (ignitionAnim) -> list[pygame.Surface]
            list of ignition animation images for the spaceship

        (engineAnim) -> list[pygame.Surface]
            list of engine animation images for the spaceship

        (engineAnimStage) -> int
            index of the engine animation images

        (ignitionAnimStage) -> int
            index of the ignition animation images

        (nitroIgnitionAnimStage) -> int
            index of the nitro ignition animation images

        (nitroIgnitionAnim) -> list[pygame.Surface]
            list of nitro ignition animation images for the spaceship

        (nitroEngineAnim) -> list[pygame.Surface]
            list of nitro engine animation images for the spaceship

        (hyperdrive) -> list[pygame.Surface]
            list of hyperdrive engine animation images for the spaceship

        (nitro) -> float
            a float that represents the acceleration of the spaceship while using nitro

        (initNitro) -> float
            a float that represents the initial acceleration of the spaceship while using nitro

        (nitroAmount) -> float
            a float that represents the amount of nitro that the spaceship has

        (nitroAmountInit) -> float
            a float that represents the initial amount of nitro that the spaceship has

        (mass) -> float
            a integer that represents how much a black hole/white hole pulls/pushes on the spaceship

        (powerUpState) -> bool
            a boolean value that represents if the spaceship is in the powered up state

        (laser) -> bool
            a boolean value that represents if the spaceship is in the laser mode

        (shield) -> bool
            a boolean value that represents if the spaceship is in the shield mode

        (shieldhp) -> int
            an int that represents the hit points of the shield

        (superStar) -> bool
            a boolean value that represents if the spaceship is in the super star mode

        (antiGravity) -> bool
            a boolean value that represents if the spaceship is in the anti-gravity mode

        (fireCast) -> bool
            a boolean value that represents if the spaceship is in fire cast mode

        (shieldDisplay) -> pygame.Surface
            an image of the shield used for the shield power up

        (laserBullet) -> pygame.Surface
            an image of the laser used for the laser power up

        (laserX) -> int
            initial x-coordinate of the laser

        (laserY) -> int
            initial y-coordinate of the laser

        (lasers) -> list
            list of lasers
    """

    def __init__(self, health: int = 100, acceleration: float = 0.8, nitro: float = 1.2) -> None:
        self.health = health
        self.init_health = health
        self.acceleration = acceleration
        self.init_accel = acceleration

        self.spaceShipWidth = 60
        self.spaceShipHeight = 80

        self.spaceShip = pygame.image.load("images/rocketship.png")

        self.spaceShip = pygame.transform.scale(self.spaceShip, (self.spaceShipWidth, self.spaceShipHeight))

        self.xVel = 0
        self.yVel = 0

        self.xPos = WIDTH//2
        self.yPos = HEIGHT//2

        self.x1 = self.xPos
        self.y1 = self.yPos-30
        self.x2 = self.xPos + self.spaceShipWidth
        self.y2 = self.yPos-30
        self.x3 = self.xPos + self.spaceShipWidth
        self.y3 = self.yPos + self.spaceShipHeight-15
        self.x4 = self.xPos
        self.y4 = self.yPos + self.spaceShipHeight-15

        self.centerX = (self.x1 + self.x3)/2
        self.centerY = (self.y1 + self.y3)/2

        self.ignitionAnim = [pygame.image.load(f"images/boosterAnim/rocketship{n}.png") for n in range(1, 4)]
        self.engineAnim = [pygame.image.load(f"images/engineAnim/rocketship{n}.png") for n in range(4)]

        self.engineAnimStage = 0
        self.ignitionAnimStage = 0
        self.nitroIgnitionAnimStage = 0

        self.nitroIgnitionAnim = [pygame.image.load(f"images/boosterAnimNitro/rocketshipNitro{n}.png") for n in range(1, 4)]
        self.nitroEngineAnim = [pygame.image.load(f"images/engineAnimNitro/rocketship{n}.png") for n in range(4)]
        self.hyperdrive = [pygame.image.load(f"images/hyperdriveAnim/rocketshipHyperdrive{n}.png") for n in range(4)]

        self.nitro = nitro
        self.initNitro = self.nitro
        self.nitroAmount = 100
        self.nitroAmountInit = self.nitroAmount

        self.mass = self.init_health

        self.powerUpState = False
        self.laser = False
        self.shield = False
        self.superStar = False
        self.antiGravity = False
        self.fireCast = False

        self.shieldhp = 0

        self.shieldDisplay = pygame.image.load("images/shieldDisplay.png")
        self.shieldDisplay = pygame.transform.scale(self.shieldDisplay, (180, 180))

        self.laserBullet = pygame.image.load("images/laserBullet.png")
        self.laserBullet = pygame.transform.scale(self.laserBullet, (50, 50))

        self.laserX = (self.x1 + self.x4)/2
        self.laserY = (self.y1 + self.y4)/2

        self.lasers = []

    def drawSpaceShip(self) -> None:
        """ (None) -> None
            Draws the spaceship hitbox and blits the spaceship image at a position
        """
        global ORIGINALship
        self.spaceShipRect = pygame.draw.polygon(gameWindow, SPACEBLUE, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3), (self.x4, self.y4)), 1)
        gameWindow.blit(self.spaceShip, (self.xPos-(self.spaceShipWidth/2)-30, (self.yPos-(round(self.spaceShipHeight/2))-10)))

    # Rotation Methods --------------------------------------------------------

    def rotate(self, angle: float) -> Union[pygame.Surface, pygame.SurfaceType]:
        """ (angle) -> Union[Surface, SurfaceType]
            Rotates the spaceship image by angle degrees
        """
        # Get Rectangle
        ORIGINALrect = ORIGINALship.get_rect()

        # Rotation
        rotatedImage = pygame.transform.rotate(ORIGINALship, angle)

        # Copy Rectangle
        rotatedRect = ORIGINALrect.copy()

        # Get Center
        rotatedRect.center = rotatedImage.get_rect().center

        # Copy Image
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()

        return rotatedImage

    def rotateLaser(self, angle: float) -> Union[pygame.Surface, pygame.SurfaceType]:
        """ (angle) -> Union[Surface, SurfaceType]
            Rotates the laser image by angle degrees
        """
        # Get Rectangle
        ORIGINALrectLaser = ORIGINALlaser.get_rect()

        # Rotation
        rotatedImage = pygame.transform.rotate(ORIGINALlaser, angle)

        # Copy Rectangle
        rotatedRect = ORIGINALrectLaser.copy()

        # Get Center
        rotatedRect.center = rotatedImage.get_rect().center

        # Copy Image
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()

        return rotatedImage

    def rotateShield(self, angle: float) -> Union[pygame.Surface, pygame.SurfaceType]:
        """ (angle) -> Union[Surface, SurfaceType]
            Rotates the laser image by angle degrees
        """
        # Get Rectangle
        ORIGINALrect = ORIGINALshield.get_rect()

        # Rotation
        rotatedImage = pygame.transform.rotate(ORIGINALshield, angle)

        # Copy Rectangle
        rotatedRect = ORIGINALrect.copy()

        # Get Center
        rotatedRect.center = rotatedImage.get_rect().center

        # Copy Image
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()

        return rotatedImage

    def rotateHitbox(self, theta: float) -> None:
        """ (theta) -> None
            Rotates the hitbox of the spaceship theta degrees
        """

        # Rotates top left point
        self.x1, self.y1 = rotateRect(self.x1, self.y1, theta * (pi / 18), self.xPos + (self.spaceShipWidth / 2), self.yPos + (self.spaceShipHeight / 2))

        # Rotates top right point
        self.x2, self.y2 = rotateRect(self.x2, self.y2, theta * (pi / 18), self.xPos + (self.spaceShipWidth / 2), self.yPos + (self.spaceShipHeight / 2))

        # Rotates bottom right point
        self.x3, self.y3 = rotateRect(self.x3, self.y3, theta * (pi / 18), self.xPos + (self.spaceShipWidth / 2), self.yPos + (self.spaceShipHeight / 2))

        # Rotates bottom left point
        self.x4, self.y4 = rotateRect(self.x4, self.y4, theta * (pi / 18), self.xPos + (self.spaceShipWidth / 2), self.yPos + (self.spaceShipHeight / 2))

# -----------------------------------------------------------------------------

    def move(self) -> None:
        """ (None) -> None
            Changes the spaceship position fields according to the velocity of the spaceship
        """
        # Position Movement
        self.xPos -= self.xVel
        self.yPos -= self.yVel

        # Point Movement
        self.x1 -= self.xVel
        self.y1 -= self.yVel
        self.x2 -= self.xVel
        self.y2 -= self.yVel
        self.x3 -= self.xVel
        self.y3 -= self.yVel
        self.x4 -= self.xVel
        self.y4 -= self.yVel

        # Laser Movement
        self.laserX -= self.xVel
        self.laserY -= self.yVel

        # Center Movement
        self.centerX -= self.xVel
        self.centerY -= self.yVel


    def accelerate(self, angle: float) -> None:
        """ (angle) -> None
            Changes the velocity of the spaceship according to the acceleration field and the angle of the ship
        """
        self.xVel += self.acceleration * -cos(((angle+90)*(pi/180)))
        self.yVel += self.acceleration * sin(((angle+90)*(pi/180)))

    def useNitro(self) -> None:
        """ (None) -> None
            Activates nitro if the nitro amount is greater than zero
        """
        if self.nitroAmount > 0:

            # Nitro acceleration
            self.nitroAmount -= 1
            self.acceleration = self.nitro
            return True
        else:

            # No Nitro
            self.acceleration = self.init_accel
            return False

# Obstacle class --------------------------------------------------------------
class Obstacle:
    """ Class with fields that all obstacles have

    All obstacles inherit from Obstacle

    Attributes:
        (radius) -> float
            the radius of the obstacle
        (x) -> int
            the x-position of the obstacle
        (y) -> int
            the y-position of the obstacle
        (xVel) -> int
            the x velocity of the obstacle
        (yVel) -> int
            the y velocity of the obstacle
    """

    def __init__(self, radius: float, xVel: float, yVel: float, x: int, y: int) -> None:
        self.radius = radius

        self.x = x
        self.y = y

        self.xVel = xVel
        self.yVel = yVel

# Asteroid class --------------------------------------------------------------
class Asteroid(Obstacle):
    """Asteroids that deal damage to the spaceship when they collide with the spaceship

    Attributes:
        (asteroid) -> pygame.Surface
            image used for the display of the asteroid

        (explosion) -> list[pygame.Surface]
            images used for the explosion of the asteroid

        (explosionAnimStage) -> int
            index of the explosion
    """

    def __init__(self, radius: float, xVel: float, yVel: float, x: int, y:int) -> None:
        super().__init__(radius, xVel, yVel, x, y)
        self.asteroid = pygame.image.load("images/asteroid.png")
        self.asteroid = pygame.transform.scale(self.asteroid, (self.radius, self.radius))
        self.explosion = [pygame.image.load("images/explosions/explosion1.png"), pygame.image.load("images/explosions/explosion2.png"),
                          pygame.image.load("images/explosions/explosion3.png"), pygame.image.load("images/explosions/explosion4.png"),
                          pygame.image.load("images/explosions/explosion5.png"), pygame.image.load("images/explosions/explosion6.png"),
                          pygame.image.load("images/explosions/explosion7.png"), pygame.image.load("images/explosions/explosion8.png")]
        self.explosionAnimStage = 0

    def draw(self) -> None:
        """ (None) -> None
            Draws the asteroid hitbox and blits the asteroid image at a position
        """
        # Hitbox of asteroid
        self.hb = pygame.draw.circle(gameWindow, SPACEBLUE, (self.x+(round(self.radius/2)), self.y+(round(self.radius/2))), round(self.radius/2), 1)

        # Asteroid Display Blitting
        gameWindow.blit(self.asteroid, (self.x, self.y))

# BlackHole class -------------------------------------------------------------
class BlackHole(Obstacle):
    """Large obstacle with an attractive force towards it
    Going too close to it will end the game

    Attributes:
        (display) -> pygame.Surface
            display of the blackhole

        (mass) -> float
            an int that represents the attractiveness of the black hole

        (xCenter) -> float
            a float representing the x coordinate of the center of the black hole

        (yCenter) -> float
            a float representing the y coordinate of the center of the black hole

        (scale) -> bool
            a boolean value that tells the black hole when to scale

    """
    def __init__(self, radius: float, xVel: float, yVel: float, x: int, y: int, mass: float) -> None:
        super().__init__(radius, xVel, yVel, x, y)
        self.display = pygame.image.load("images/blackhole.png")
        self.mass = mass
        self.xCenter = self.x+self.radius
        self.yCenter = self.y+self.radius
        self.scale = True

    def gravity(self, xPos: int, yPos: int, mass: float, xVel: float, yVel: float) -> tuple[float, float]:
        """ (xPos, yPos, mass, xVel, yVel) -> tuple
            Accelerates the spaceship towards a point with an acceleration depending on mass and distance

            Acceleration is twice as strong when the spaceship has the super star power up active

            Acceleration calculation is proportional to the product of the masses and
            inversely proportional to the distance squared
        """

        # Distance Calculation
        distance = round(dist((self.xCenter, self.yCenter),
                              (xPos, yPos)), 1)

        # Force Calculation
        if not spaceship.superStar:
            force = 10*((mass * self.mass) / distance ** 2)
        else:
            # Super Star Gravity Effect
            force = 20*((mass * self.mass) / distance ** 2)

        # Angle Calculation
        if xPos - self.xCenter != 0:
            angle = -atan(((yPos - self.yCenter) / (xPos - self.xCenter)))
        else:
            # Angle Calculation for Zero Division Error
            angle = -atan((yPos - self.yCenter) / 1)

        # Acceleration Calculation
        if not spaceship.antiGravity:

            # Quadrant I
            if xPos > self.xCenter and yPos < self.yCenter:
                xVel += (force*cos(angle)) / mass
                yVel -= (force*sin(angle)) / mass

            # Quadrant II
            elif xPos <= self.xCenter and yPos <= self.yCenter:
                xVel -= (force*cos(angle)) / mass
                yVel += (force*sin(angle)) / mass

            # Quadrant III
            elif xPos < self.xCenter and yPos > self.yCenter:
                xVel -= (force*cos(angle)) / mass
                yVel += (force*sin(angle)) / mass

            # Quadrant IV
            elif xPos >= self.xCenter and yPos >= self.yCenter:
                xVel += (force*cos(angle)) / mass
                yVel -= (force*sin(angle)) / mass

        return xVel, yVel

    def move(self) -> None:
        """ (None) -> None
            Moves the blackhole depending on the velocity and blits the black hole
        """
        # Black Hole Display Blitting
        gameWindow.blit(self.display, (self.x, self.y))
        
        # Center Movement
        self.xCenter += self.xVel
        self.yCenter += self.yVel

        # x and y movement
        self.x += self.xVel
        self.y += self.yVel


    def rotate(self, angle: float) -> Union[pygame.Surface, pygame.SurfaceType]:
        """ (angle) -> Union[pygame.Surface, pygame.SurfaceType]
            Rotates the black hole image by angle degrees
        """
        global ORIGINALBLACKHOLE

        # Scale
        ORIGINALBLACKHOLE = pygame.transform.scale(ORIGINALBLACKHOLE, (2*self.radius, 2*self.radius))

        # Get Rectangle
        ORIGINALrect = ORIGINALBLACKHOLE.get_rect()

        # Rotation
        rotatedImage = pygame.transform.rotate(ORIGINALBLACKHOLE, angle)

        # Scaling Rotated Image
        if self.scale:
            rotatedImage = pygame.transform.scale(rotatedImage, (2*self.radius, 2*self.radius))
            self.scale = False

        # Copy Rectangle
        rotatedRect = ORIGINALrect.copy()

        # Getting Rectangle Center
        rotatedRect.center = rotatedImage.get_rect().center

        # Copy Image
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()

        return rotatedImage

# WhiteHole class -------------------------------------------------------------
class WhiteHole(BlackHole):
    """Large obstacle with a repulsive force away from it
    Going too close to it will end the game

    Attributes:
        (display) -> pygame.Surface
            display of the white hole

        (mass) -> float
            an int that represents the attractiveness of the  hole

        (xCenter) -> float
            a float representing the x coordinate of the center of the white hole

        (yCenter) -> float
            a float representing the y coordinate of the center of the white hole

        (scale) -> bool
            a boolean value that tells the white hole when to scale


    """
    def __init__(self, radius: float, xVel: float, yVel: float, x: int, y:int, mass: float):
        super().__init__(radius, xVel, yVel, x, y, mass)
        self.display = pygame.image.load("images/whitehole.png")

        self.xCenter = self.x+self.radius
        self.yCenter = self.y+self.radius

        self.scale = True

    def rotate(self, angle: float) -> None:
        """ (angle) -> Union[pygame.Surface, pygame.SurfaceType]
            Rotates the white hole image by angle degrees
        """
        global ORIGINALWHITEHOLE
        # Scale
        ORIGINALWHITEHOLE = pygame.transform.scale(ORIGINALWHITEHOLE, (2*self.radius, 2*self.radius))

        # Get Rectangle
        ORIGINALrect = ORIGINALWHITEHOLE.get_rect()

        # Rotation
        rotatedImage = pygame.transform.rotate(ORIGINALWHITEHOLE, angle)

        # Scaling Rotated Image
        if self.scale:
            rotatedImage = pygame.transform.scale(rotatedImage, (2*self.radius, 2*self.radius))
            self.scale = False

        # Copy Rectangle
        rotatedRect = ORIGINALrect.copy()

        # Getting Rectangle Center
        rotatedRect.center = rotatedImage.get_rect().center

        # Copy Image
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()

        return rotatedImage

# PowerUp class ---------------------------------------------------------------
class PowerUp(Obstacle):
    """Powerups that the spaceship can collect for certain benefits

    Atributes
        (powerUps) -> list[pygame.Surface]
            list of power up displays

        (powerup) -> int
            int that represents the type of power up

        (radius) -> int
            an int that represents the radius of the hitbox of the power up

        (powerupHitbox) -> pygame.Circle
            the hitbox of the power up

    """

    def __init__(self, xVel: float, yVel: float, x: int, y:int, powerup: int) -> None:
        super().__init__(self, xVel, yVel, x, y)

        self.powerUps = [pygame.image.load("images/powerUps/96x96/antiGravity.png"),
                         pygame.image.load("images/powerUps/96x96/clear.png"),
                         pygame.image.load("images/powerUps/96x96/health.png"),
                         pygame.image.load("images/powerUps/96x96/laser.png"),
                         pygame.image.load("images/powerUps/96x96/nitro.png"),
                         pygame.image.load("images/powerUps/96x96/shield.png"),
                         pygame.image.load("images/powerUps/96x96/superStar.png")]

        self.powerup = powerup
        self.radius = 44
        self.powerupHitbox = pygame.draw.circle(gameWindow, SPACEBLUE,
                                        (self.x+round(self.radius), self.y+round(self.radius)), round(self.radius), 0)

    def move(self):
        """ (None) -> None
            Moves the power up depending on the velocity and blits the powerup image
        """

        # Blitting power up image
        gameWindow.blit(self.powerUps[self.powerup], (self.x, self.y))

        # Move x and y
        self.x += self.xVel
        self.y += self.yVel

class Collectible(Obstacle):
    """ Objects that the spaceship collects

    Attributes
        (radius) -> int
            an int that represents the radius of the hitbox of the collectible

        (hitbox) -> pygame.Circle
            the hitbox of the collectible

        (display) -> pygame.Surface
            the display of the collectible
    """
    def __init__(self, x: int, y: int, xVel: float, yVel: float) -> None:
        super().__init__(self, xVel, yVel, x, y)
        self.radius = 38

        self.hitbox = pygame.draw.circle(gameWindow, SPACEBLUE, (self.x, self.y), self.radius)

        self.display = pygame.image.load("images/hyperDriveFuel.png")
        self.display = pygame.transform.scale(self.display, (round(63*WIDTH/1680), round(78*HEIGHT/1080)))

    def move(self):
        """ (None) -> None
            Moves the collectible depending on the velocity and blits the collectible image
        """

        # Blit display
        gameWindow.blit(self.display, (self.x-(round(63*WIDTH/1680)/2), self.y-(round(78*HEIGHT/1080)/2)))

        # Move x and y
        self.x += self.xVel
        self.y += self.yVel

# Functions ====================================================================

def exp(x: Union[complex, float])-> Union[complex, float]:
    """ (x) -> Union[complex, float]
        Returns e^x
        Used for rotation
    """
    return sum([
        x**n/factorial(n) for n in range(100)
    ])


def rotateRect(x: float, y: float, theta: float, xAxis: float, yAxis: float) -> float:
    """ (x, y, theta. xAxis, yAxis) -> float
    Rotates a point around another point theta radians
    """
    # Writes point as complex number relative to rotation point
    point = complex(x-xAxis, y-yAxis)

    # Rotates point
    expInput = exp(complex(0, 1) * theta)
    point *= expInput

    # Gets x and y
    rotatedX = point.real
    rotatedY = point.imag

    return rotatedX+xAxis, rotatedY+yAxis


def moveAsteroidInit() -> None:
    """ (None) -> None
        Initializes the asteroids and their velocities
    """
    for i in range(len(asteroids)):

        # Velocity Limit
        if asteroids[i].xVel < 20 or asteroids[i].yVel < 20:

            # Movement
            asteroids[i].x += asteroids[i].xVel
            asteroids[i].y += asteroids[i].yVel
        else:

            # Velocity Limiting
            if asteroids[i].xVel > 20:
                asteroids[i].xVel = 20
            elif asteroids[i].xVel < -20:
                asteroids[i].xVel = -20
            elif asteroids[i].yVel > 20:
                asteroids[i].yVel = 20
            elif asteroids[i].yVel < -20:
                asteroids[i].yVel = -20

        # Velocity Setting
        if (asteroids[i].y == 0) and (asteroids[i].x != 0 or asteroids[i].x != WIDTH):
            asteroids[i].xVel = randint(5, 20)
        elif (asteroids[i].y == HEIGHT) and (asteroids[i].x != 0 or asteroids[i].x != WIDTH):
            asteroids[i].xVel = randint(-20, -5)
        elif (asteroids[i].y != 0 or asteroids[i].y != HEIGHT) and (asteroids[i].x == 0):
            asteroids[i].yVel = randint(5, 20)
        elif (asteroids[i].y != 0 or asteroids[i].y != HEIGHT) and (asteroids[i].x == WIDTH):
            asteroids[i].yVel = randint(-20, -5)


def objectGravity() -> None:
    """ (None) -> None
        Applies the gravity from black/white holes to the spaceship
    """
    for i in range(len(blackHoles)):
        spaceship.xVel, spaceship.yVel = blackHoles[i].gravity(spaceship.xPos+(spaceship.spaceShipWidth/2), spaceship.yPos, spaceship.mass, spaceship.xVel, spaceship.yVel)
        # Too buggy
        # for j in range(len(asteroids)):
        #      asteroids[j].xVel, asteroids[j].yVel = blackHoles[i].gravity(asteroids[j].x, asteroids[j].y, asteroids[j].radius*100, asteroids[j].xVel, asteroids[j].yVel)


# Adding functions ------------------------------------------------------------


def addAsteroids(amount: int) -> None:
    """ (amount) -> None
        Appends asteroids to a list for storage
    """
    for i in range(amount):

        # Pick Random Side
        side = randint(0, 4)

        #|-----------------|
        #|        0        |
        #| 3             1 |
        #|        2        |
        #|-----------------|

        # Generates based on side
        if side == 0:
            asteroids.append(Asteroid(randint(40, 60),randint(5, 20), randint(5, 20), randint(randint(40, 80), WIDTH - randint(40, 80)), 0))

        elif side == 1:
            asteroids.append(Asteroid(randint(40, 60), -randint(5, 20), -randint(5, 20), WIDTH, randint(randint(40, 80), HEIGHT - randint(40, 80))))

        elif side == 2:
            asteroids.append(Asteroid(randint(40, 60), -randint(5, 20), -randint(5, 20), randint(randint(40, 80), WIDTH - randint(40, 80)), HEIGHT))

        else:
            asteroids.append(Asteroid(randint(40, 60), randint(5, 20), randint(5, 20), 0, randint(randint(40, 80), HEIGHT - randint(40, 80))))


def addBlackHoles(amount: int) -> None:
    """ (amount) -> None
        Appends black holes to a list for storage
    """
    for i in range(amount):

        # Pick Random Side
        side = randint(0, 4)

        #|-----------------|
        #|        0        |
        #| 3             1 |
        #|        2        |
        #|-----------------|

        # Generates based on side
        # Amount of black/white holes restricted to 1
        if side == 0 and len(blackHoles) == 0:
            blackHoles.append(BlackHole(randint(150, 200),randint(2, 5), randint(2, 5), randint(0, WIDTH), -250, randint(5000, 8000)))

        elif side == 1 and len(blackHoles) == 0:
            blackHoles.append(BlackHole(randint(150, 200), -randint(2, 5), -randint(2, 5), WIDTH+250, randint(0, HEIGHT), randint(5000, 8000)))

        elif side == 2 and len(blackHoles) == 0:
            blackHoles.append(BlackHole(randint(150, 200), -randint(2, 5), -randint(2, 5), randint(0, WIDTH), HEIGHT+250, randint(5000, 8000)))

        elif side == 3 and len(blackHoles) == 0:
            blackHoles.append(BlackHole(randint(150, 200), randint(2, 5), randint(2, 5), -250   , randint(0, HEIGHT), randint(5000, 8000)))


def addWhiteHoles(amount: int) -> None:
    """ (amount) -> None
        Appends white holes to a list for storage
    """
    for i in range(amount):

        # Picks Random Side
        side = randint(0, 4)

        #|-----------------|
        #|        0        |
        #| 3             1 |
        #|        2        |
        #|-----------------|

        # Generated based on side
        # Amount of black/white holes restricted to 1
        if side == 0 and len(blackHoles) == 0:
            blackHoles.append(WhiteHole(randint(150, 200),randint(2, 5), randint(2, 5), randint(0, WIDTH), -160, -randint(5000, 8000)))

        elif side == 1 and len(blackHoles) == 0:
            blackHoles.append(WhiteHole(randint(150, 200), -randint(2, 5), -randint(2, 5), WIDTH+160, randint(0, HEIGHT), -randint(5000, 8000)))

        elif side == 2 and len(blackHoles) == 0:
            blackHoles.append(WhiteHole(randint(150, 200), -randint(2, 5), -randint(2, 5), randint(0, WIDTH), HEIGHT+160, -randint(5000, 8000)))

        elif side == 3 and len(blackHoles) == 0:
            blackHoles.append(WhiteHole(randint(150, 200), randint(2, 5), randint(2, 5), -160, randint(0, HEIGHT), -randint(5000, 8000)))


def addPowerUp(amount: int) -> None:
    """ (amount) -> None
        Appends power ups to a list for storage
    """
    for i in range(amount):

        # Picks Random Side
        side = randint(0, 4)

        #|-----------------|
        #|        0        |
        #| 3             1 |
        #|        2        |
        #|-----------------|

        # Generates based on side
        # Amount of power ups restricted to 1
        if side == 0 and len(powerups) == 0:
            powerups.append(PowerUp(randint(2, 8), randint(2, 8), randint(randint(40, 80), WIDTH - randint(40, 80)), 0, randint(0, 6)))

        elif side == 1 and len(powerups) == 0:
            powerups.append(PowerUp(-randint(2, 8), -randint(2, 8), WIDTH, randint(randint(40, 80), HEIGHT - randint(40, 80)), randint(0, 6)))

        elif side == 2 and len(powerups) == 0:
            powerups.append(PowerUp(-randint(2, 8), -randint(2, 8), randint(randint(40, 80), WIDTH - randint(40, 80)), HEIGHT, randint(0, 6)))

        elif side == 3 and len(powerups) == 0:
            powerups.append(PowerUp(randint(2, 8), randint(2, 8), 0, randint(randint(40, 80), HEIGHT - randint(40, 80)), randint(0, 6)))


def addCollectible(amount: int) -> None:
    """ (amount) -> None
        Appends collectibles to a list for storage
    """
    for i in range(amount):

        # Picks random side
        side = randint(0, 4)

        #|-----------------|
        #|        0        |
        #| 3             1 |
        #|        2        |
        #|-----------------|

    # Generates based on side
    # Amount of collectibles restricted to 3
    if side == 0 and len(collectibles) < 3:
        collectibles.append(Collectible(randint(randint(40, 80), WIDTH - randint(40, 80)), 0, randint(2, 8), randint(2, 8)))

    elif side == 1 and len(collectibles) < 3:
        collectibles.append(Collectible(WIDTH, randint(randint(40, 80), HEIGHT - randint(40, 80)), -randint(2, 8), -randint(2, 8)))

    elif side == 2 and len(collectibles) < 3:
        collectibles.append(Collectible(randint(randint(40, 80), WIDTH - randint(40, 80)), HEIGHT, -randint(2, 8), -randint(2, 8)))

    elif side == 3 and len(collectibles) < 3:
        collectibles.append(Collectible(0, randint(randint(40, 80), HEIGHT - randint(40, 80)), randint(2, 8), randint(2, 8)))


# Collision functions ---------------------------------------------------------


def collideAsteroid() -> None:
    """ (None) -> None
        Checks for collision between the asteroids and the spaceship and removes the asteroid if it does collide
    """
    for i in range(360):
        for j in range(len(asteroids)):

            # Checks for collision
            if spaceship.spaceShipRect.collidepoint(asteroids[j].x + (asteroids[j].radius/2)*cos(i*pi/180),
                                                    asteroids[j].y + (asteroids[j].radius/2)*sin(i*pi/180)) \
                    and spaceship.shieldhp == 0: # Checks that there isn't a shield

                # Checks that there isn't super star
                if not spaceship.superStar:

                    # Damage calculation
                    spaceship.health -= abs(sqrt(asteroids[j].xVel**2 + asteroids[j].yVel**2))

                # Asteroid Collision Animation
                for i in range(39):
                    asteroids[j].explosionAnimStage += 1
                    asteroids[j].asteroid = asteroids[j].explosion[asteroids[j].explosionAnimStage//5]
                    gameWindow.blit(asteroids[j].asteroid, (asteroids[j].x, asteroids[j].y))

                # Asteroid Explosion Sound
                asteroidExplosion.play()

                # Asteroid removal
                asteroids.pop(j)
                break


def laserCollideAsteroid() -> None:
    """ (None) -> None
        Checks for collision between the asteroids and lasers and removes the asteroid and lasers if they do collide
    """
    for k in range(len(spaceship.lasers)):
        for j in range(len(asteroids)):

            # Checks for collision
            if dist((spaceship.lasers[k][0], spaceship.lasers[k][1]), (asteroids[j].x, asteroids[j].y)) <= asteroids[j].radius:

                # Asteroid Collision Animation
                for i in range(39):
                    asteroids[j].explosionAnimStage += 1
                    asteroids[j].asteroid = asteroids[j].explosion[asteroids[j].explosionAnimStage//5]
                    gameWindow.blit(asteroids[j].asteroid, (asteroids[j].x, asteroids[j].y))

                # Asteroid Explosion Sound
                asteroidExplosion.play()

                # Asteroid removal
                asteroids.pop(j)

                # Laser removal
                spaceship.lasers.pop(k)
                return None


def asteroidCollideAsteroid() -> None:
    """ (None) -> None
    Checks for collision between the asteroids and alters the momentum of the asteroids if they collide
    """
    for i in range(len(asteroids)):
        for j in range(len(asteroids)):
            if i != j:
                # Checks for collision
                if dist((asteroids[i].x, asteroids[i].y), (asteroids[j].x, asteroids[j].y)) <= (asteroids[i].radius/2) + (asteroids[j].radius/2):

                    # Gives random velocities based on quadrant
                    if asteroids[i].x > asteroids[j].x and asteroids[i].y > asteroids[j].y:
                        if asteroids[i].yVel >= 0:
                            asteroids[i].yVel = randint(-20, -5)
                        else:
                            asteroids[i].yVel = randint(5, 20)
                    elif asteroids[i].x > asteroids[j].x and asteroids[i].y < asteroids[j].y:
                        if asteroids[i].xVel >= 0:
                            asteroids[i].xVel = randint(-20, -5)
                        else:
                            asteroids[i].xVel = randint(5, 20)
                    elif asteroids[i].x < asteroids[j].x and asteroids[i].y < asteroids[j].y:
                        if asteroids[i].yVel >= 0:
                            asteroids[i].yVel = randint(5, 20)
                        else:
                            asteroids[i].yVel = randint(-20, -5)
                    else:
                        if asteroids[i].xVel >= 0:
                            asteroids[i].xVel = randint(5, 20)
                        else:
                            asteroids[i].xVel = randint(-20, -5)


def getPowerUp() -> None:
    """ (None) -> None
        Checks for power up collision and if there is collision, a powerup effect is applied for a certain amount of time
    """
    global referenceTime0, cooldown, stage
    for i in range(360):
        for j in range(len(powerups)):

            # Checks for collision
            if spaceship.spaceShipRect.collidepoint(powerups[j].x + powerups[j].radius*cos(i*pi/180),
                                                    powerups[j].y + powerups[j].radius*sin(i*pi/180)) \
                    and not spaceship.powerUpState: # Checks if the spaceship already has a power up effect

                # Getting time for power up effect times
                referenceTime0 = time.time()

                # Collect Power Up Sound
                collectPowerUp.play()

                # Anti-Gravity Power Up
                if powerups[j].powerup == 0:

                    # Anti-gravity effect
                    spaceship.antiGravity = True

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 12

                # Clear Power Up
                elif powerups[j].powerup == 1:

                    # Clear Sound
                    clearPowerUp.play()

                    # Animation Stage
                    stage = 0

                    # Fire Animation
                    spaceship.fireCast = True

                    # Clear Asteroids
                    asteroids.clear()

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 0.5

                # Health Power Up
                elif powerups[j].powerup == 2:

                    # Add health
                    if spaceship.health + (spaceship.init_health/3) <= spaceship.init_health:
                        spaceship.health += (spaceship.init_health/3)
                    else:
                        spaceship.health = spaceship.init_health

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 0.5

                # Laser Power Up
                elif powerups[j].powerup == 3:

                    # Laser effect
                    spaceship.laser = True

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 12

                # Nitro Power Up
                elif powerups[j].powerup == 4:

                    # Add Nitro
                    if spaceship.nitroAmount + (spaceship.nitroAmountInit/3) <= spaceship.nitroAmountInit:
                        spaceship.nitroAmount += (spaceship.nitroAmountInit/3)
                    else:
                        spaceship.nitroAmount = spaceship.nitroAmountInit

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 0.5

                # Shield Power Up
                elif powerups[j].powerup == 5:

                    # Shield Powering Up Sound
                    shieldInit.play()

                    # Shield effect
                    spaceship.shield = True

                    # Initializing Shield hitpoints
                    spaceship.shieldhp = 3

                    # Power Up States
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 25

                # Super Star Power Up
                elif powerups[j].powerup == 6:

                    # Super Star Music
                    superStarMusic.play()

                    # Super star effect
                    spaceship.superStar = True

                    # Power Up State
                    spaceship.powerUpState = True

                    # Duration of power up
                    cooldown = 6

                # Power Up Removal
                powerups.pop(j)

        # Power Up Duration End
        if time.time() - referenceTime0 > cooldown and spaceship.powerUpState:

            # Re-initialization of effects and properties
            spaceship.mass = spaceship.init_health
            spaceship.powerUpState = False
            spaceship.laser = False
            spaceship.shield = False
            spaceship.superStar = False
            spaceship.fireCast = False
            spaceship.antiGravity = False

            # Stop super star music
            superStarMusic.stop()

        # Shield Down
        elif spaceship.shieldhp == 0 and spaceship.shield:

            # Shield Down Sound
            shieldDownSound.play()

            # Re-initialization of effects and properties
            spaceship.mass = spaceship.init_health
            spaceship.powerUpState = False
            spaceship.laser = False
            spaceship.shield = False
            spaceship.superStar = False
            spaceship.fireCast = False
            spaceship.antiGravity = False

            # Stop super star music
            superStarMusic.stop()


def getCollectible() -> None:
    """ (None) -> None
        Checks for collectible collision and if there is collision, the collected amount is incremented by 1
    """
    global collected
    for i in range(360):
        for j in range(len(collectibles)):

            # Check for colision
            if spaceship.spaceShipRect.collidepoint(collectibles[j].x + collectibles[j].radius*cos(i*pi/180),
                                                    collectibles[j].y + collectibles[j].radius*sin(i*pi/180)):
                # Collected Collectible Power Up
                collectPowerUp.play()

                # Collected Incremented
                collected += 1

                # Collectible Removal
                collectibles.pop(j)

                break


# Display functions -----------------------------------------------------------


def displayHealth() -> None:
    """ (None) -> None
        Draws the health bar
    """
    # Draw Border
    pygame.draw.rect(gameWindow, BLACK, (50, 50, 500, 50), 10)

    # Draw Background
    pygame.draw.rect(gameWindow, DGREY, (55, 55, 490, 40), 0)

    # Draw Health Bar
    pygame.draw.rect(gameWindow, RED, (55, 55, 490*(spaceship.health/spaceship.init_health), 40), 0)

    # Draw Reflection
    pygame.draw.rect(gameWindow, LRED, (65, 60, 480*(spaceship.health/spaceship.init_health)-10, 6), 0)


def displayNitro() -> None:
    """ (None) -> None
        Draws the health bar
    """
    # Draw Border
    pygame.draw.rect(gameWindow, BLACK, (50, 120, 500, 50), 10)

    # Draw Background
    pygame.draw.rect(gameWindow, DGREY, (55, 125, 490, 40), 0)

    # Draw Health Bar
    pygame.draw.rect(gameWindow, BLUE, (55, 125, 490*(spaceship.nitroAmount/spaceship.nitroAmountInit), 40), 0)

    # Draw Reflection
    pygame.draw.rect(gameWindow, LBLUE, (65, 130, 480*(spaceship.nitroAmount/spaceship.nitroAmountInit)-10, 6), 0)


def displayTime(timeInS: float, x: int, y: int) -> None:
    """ (timeInS, x, y) -> None
        Renders and blits the time on the screen
    """
    # Get rounded time
    strTime = round(timeInS, 1)

    # render time
    stopwatch = timeFont.render(f"{strTime}s", 1, WHITE)

    # Blit time
    gameWindow.blit(stopwatch, (x, y))


def displayCollected(collected: int, maximum: int, x: int, y: int) -> None:
    """ (collected, maximum, x, y) -> None
        Displays the collected score
    """
    # Render collected score
    collectedScore = timeFont.render(f"{collected}/{maximum}", 1, WHITE)

    # Blit collected score
    gameWindow.blit(collectedScore, (x, y))


def scaleX(x: float) -> int:
    """ (x) -> int
        Returns rounded version of a x-coordinate scaled to the width
    """
    return round(x*WIDTH/1680)


def scaleY(y: float) -> int:
    """ (y) -> int
        Returns rounded version of a y-coordinate scaled to the height
    """
    return round(y*HEIGHT/1080)


# Menu functions --------------------------------------------------------------


def renderMenu() -> None:
    """ (None) -> None
        Renders the menu
    """
    global playButtonStage, inPlay, menuScreen, campaignMode, endlessMode, referenceTime3, options
    # Get position and pressed
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    # Type Button Rectangle
    typeButton = pygame.Rect((scaleX(645), scaleY(690), scaleX(375), scaleY(140)))

    # Play Button Rectangle
    playButton = pygame.draw.rect(gameWindow, WHITE, (scaleX(645), scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

    # Buffer Rectangle
    buffer = pygame.Rect((scaleX(645), scaleY(690), scaleX(375), scaleY(20)))

    # If hover over play button
    if playButton.collidepoint(pos):

        # Button Darkens
        playButton = pygame.draw.rect(gameWindow, LGREY, (scaleX(645), scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

        # Blit Play Text and Animation
        gameWindow.blit(playButtonImages[playButtonStage//20], (scaleX(664), scaleY(570)))
        playButtonStage = (playButtonStage + 1) % 80

        # Show Type Button
        options = True

    # If hovering over type button
    elif options and typeButton.collidepoint(pos):
        options = True

    else:
        # Normal Play Button
        playButton = pygame.draw.rect(gameWindow, WHITE, (scaleX(645), scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

        # Blit Play Text Image
        gameWindow.blit(playButtonImage, (scaleX(664), scaleY(570)))

        # Hide Type Button
        options = False

    if options:
        # draw type button
        typeButton = pygame.draw.rect(gameWindow, WHITE, (scaleX(645), scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

        # If hover over type button
        if typeButton.collidepoint(pos):

            # Button Darkens
            pygame.draw.rect(gameWindow, LGREY, (scaleX(645), scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

            # Freezes Animation
            gameWindow.blit(playButtonImages[playButtonStage//20], (scaleX(664), scaleY(570)))
        else:
            # Normal Type Button
            pygame.draw.rect(gameWindow, WHITE, (scaleX(645), scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

        # If hover over buffer
        if buffer.collidepoint(pos):

            # Freezes animation
            gameWindow.blit(playButtonImages[playButtonStage//20], (scaleX(664), scaleY(570)))

        # If type button pressed and campaign mode
        if typeButton.collidepoint(pos) and pressed and campaignMode and time.time() - referenceTime3 >= 0.3:

            # Select Button Sound
            selectionSound.play()

            # Switches Modes
            campaignMode = False
            endlessMode = True

            # Get time
            referenceTime3 = time.time()

        # If type button pressed and endless mode
        elif typeButton.collidepoint(pos) and pressed and endlessMode and time.time() - referenceTime3 >= 0.3:

            # Select Button Sound
            selectionSound.play()

            # Switches Modes
            campaignMode = True
            endlessMode = False

            # Get time
            referenceTime3 = time.time()

        # Blit "Endless" / "Campaign" with Hover / No Hover

        if campaignMode and typeButton.collidepoint(pos):
            gameWindow.blit(campaignTextHover, ((WIDTH/2) - scaleX(175), HEIGHT / 2 + scaleY(204)))

        elif campaignMode and not typeButton.collidepoint(pos):
            gameWindow.blit(campaignText, ((WIDTH/2) - scaleX(175), HEIGHT / 2 + scaleY(204)))

        if endlessMode and typeButton.collidepoint(pos):
            gameWindow.blit(endlessTextHover, ((WIDTH/2) - scaleX(153), HEIGHT/2 + scaleY(204)))

        elif endlessMode and not typeButton.collidepoint(pos):
            gameWindow.blit(endlessText, ((WIDTH/2) - scaleX(153), HEIGHT/2 + scaleY(204)))

    # Play Button Collision
    if playButton.collidepoint(pos) and pressed:

        # Rick Roll
        # webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        # Button Selection Sound
        selectionSound.play()

        # Menu Switched Off
        menuScreen = False

        # In Play Switched On
        inPlay = True

    # Blit Title Image
    gameWindow.blit(titleImage, (round(WIDTH/2-scaleX(1080)/2), 100))


def renderEnd() -> None:
    """ (None) -> None
        Renders the endscreen
    """
    global playButtonStage, inPlay, menuScreen, campaignMode, endlessMode, referenceTime3, options, titleEnd, playButtonEnd, \
        endScreen, reset, scorePos, score, isRunning, collected, collectedScore

    # Get Position and Pressed
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    # Type Button Rectangle
    typeButton = pygame.Rect((playButtonEnd, scaleY(690), scaleX(375), scaleY(140)))

    # Play Button Rectangle
    playButton = pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

    # Buffer Rectangle
    buffer = pygame.Rect((scaleX(645), scaleY(690), scaleX(375), scaleX(20)))

    # Game Over Text
    gameOver = titleFont.render("Game Over", 1, WHITE)

    # Score Display Text
    scoreDisplay = modeFont.render(f"{score}", 1, WHITE)

    # Level Display Text
    levelDisplay = titleFont.render(f"Level {level}", 1, WHITE)

    # Collected Display Text
    collectedDisplay = modeFont.render(f"{collectedScore}/{maxCollected}", 1, WHITE)

    # High Score Display Text
    highscoreDisplay = highscoreFont.render("High Score", 1, WHITE)

    # Quit Button Rectangle
    quitButton = pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(850), scaleX(375), scaleY(140)), scaleX(15))

    # If hover over play button
    if playButton.collidepoint(pos):

        # Button Darkens
        playButton = pygame.draw.rect(gameWindow, LGREY, (playButtonEnd, scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

        # Blit Play Text and Animation
        gameWindow.blit(playButtonImages[playButtonStage//20], (playButtonEnd + scaleX(19), scaleY(570)))
        playButtonStage = (playButtonStage + 1) % 80

        # Show Type Button
        options = True

    # If hovering over type button
    elif options and typeButton.collidepoint(pos):
        options = True

    else:
        # Normal Play Button
        playButton = pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(550), scaleX(375), scaleY(140)), scaleX(15))

        # Blit Play Text Image
        gameWindow.blit(playButtonImage, (playButtonEnd + scaleX(19), scaleY(570)))
        options = False

    # If hovering over quit button
    if quitButton.collidepoint(pos):

        # Quit Button Rectangle
        quitButton = pygame.draw.rect(gameWindow, LGREY, (playButtonEnd, scaleY(850), scaleX(375), scaleY(140)), scaleX(15))

        # Text Darkens
        gameWindow.blit(exitTextHover, (playButtonEnd + scaleX(19), scaleY(870)))

    else:
        # Normal Quit Button
        quitButton = pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(850), scaleX(375), scaleY(140)), scaleX(15))

        # Blit Exit Text Image
        gameWindow.blit(exitText, (playButtonEnd + scaleX(19), scaleY(870)))


    # Quit Button Pressed
    if quitButton.collidepoint(pos) and pressed:

        # All loops switched off
        isRunning = False
        menuScreen = False
        inPlay = False
        endScreen = False

    # Options Button
    if options:

        # Draw Type Button
        typeButton = pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

        # If hover over type button
        if typeButton.collidepoint(pos):

            # Button Darkens
            pygame.draw.rect(gameWindow, LGREY, (playButtonEnd, scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

            # Freezes Animation
            gameWindow.blit(playButtonImages[playButtonStage//20], (playButtonEnd + scaleX(19), scaleY(570)))
        else:
            # Normal Type Button
            pygame.draw.rect(gameWindow, WHITE, (playButtonEnd, scaleY(710), scaleX(375), scaleY(120)), scaleX(15))

        # If type button pressed and campaign mode
        if typeButton.collidepoint(pos) and pressed and campaignMode and time.time() - referenceTime3 >= 0.3:

            # Button Selection Sound
            selectionSound.play()

            # Switch Modes
            campaignMode = False
            endlessMode = True

            # Get Time
            referenceTime3 = time.time()

        # If type button pressed and endless mode
        elif typeButton.collidepoint(pos) and pressed and endlessMode and time.time() - referenceTime3 >= 0.3:

            # Button Selection Sound
            selectionSound.play()

            # Switch Modes
            campaignMode = True
            endlessMode = False

            # Get Time
            referenceTime3 = time.time()

        # If hover over type button
        if buffer.collidepoint(pos):
            # Freeze animation
            gameWindow.blit(playButtonImages[playButtonStage//20], (playButtonEnd + scaleX(19), scaleY(570)))

        # Blit "Campaign"/ "Endless" with Hover/ No Hover

        if campaignMode and typeButton.collidepoint(pos):
            gameWindow.blit(campaignTextHover, (playButtonEnd + scaleX(19), HEIGHT / 2 + scaleY(204)))

        elif campaignMode and not typeButton.collidepoint(pos):
            gameWindow.blit(campaignText, (playButtonEnd + scaleX(19), HEIGHT / 2 + scaleY(204)))

        if endlessMode and typeButton.collidepoint(pos):
            gameWindow.blit(endlessTextHover, (playButtonEnd + scaleX(40), HEIGHT/2 + scaleY(204)))

        elif endlessMode and not typeButton.collidepoint(pos):
            gameWindow.blit(endlessText, (playButtonEnd + scaleX(40), HEIGHT/2 + scaleY(204)))

    # Play Button Clicked
    if playButton.collidepoint(pos) and pressed:

        # Button Selection Sound
        selectionSound.play()

        # re-initialization
        reInit()

        # In Play switched on
        # Menu and end screen switched off
        menuScreen = False
        endScreen = False
        inPlay = True

    # Blit Title
    gameWindow.blit(titleImage, (titleEnd, 100))

    # get "game over" width and height
    gameOverWidth, gameOverHeight = titleFont.size("Game Over")

    if not campaignMode:
        # High Score
        highscoreWidth, highscoreHeight = highscoreFont.size("High Score")

        # Blit score and "game over"
        if scorePos < WIDTH + gameOverWidth:
            gameWindow.blit(gameOver, (scorePos - round(gameOverWidth/2), 100))
            gameWindow.blit(scoreDisplay, (scorePos-round(scoreWidth/2), 664))

            # Blit Highscore
            if highScore:
                gameWindow.blit(highscoreDisplay, (scorePos - round(highscoreWidth/2), 400))

            # Score text movement
            scorePos += 2

    else:
        # Blit Level and collected score
        titleWidth, titleHeight = titleFont.size(f"Level {level}")
        collectedWidth, collectedHeight = modeFont.size(f"{collectedScore}/{maxCollected}")

        # Move score and level display
        if scorePos < WIDTH + titleWidth:
            gameWindow.blit(levelDisplay, (scorePos - round(titleWidth/2), 100))
            gameWindow.blit(collectedDisplay, (scorePos - round(collectedWidth/2), 664))
            scorePos += 2

    # Limit title image position
    if titleEnd >= round(WIDTH/2-scaleX(1018)/2):
        titleEnd += 0
        titleEnd = round(WIDTH/2-scaleX(1018)/2)
    else:
        # Move title position
        titleEnd += 2

    # Limit play button image position
    if playButtonEnd >= round(WIDTH/2 - scaleX(195)):
        playButtonEnd += 0
        playButtonEnd = round(WIDTH/2 - scaleX(195))
    else:
        # Move play button position
        playButtonEnd += 2


# Endgame and re-initialization functions --------------------------------------


def exitGame() -> None:
    """ (None) -> bool
        Returns True if the game is exited or escape is pressed
    """
    # If quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    # If escape key pressed
    if keys[pygame.K_ESCAPE]:
        return True


def gameOver(*, end=False) -> None:
    """ (None) -> None
        Stops sounds, plays death sound and goes to the end screen
    """
    global menuScreen, inPlay, endScreen, accelerationSound, superStarMusic, shieldInit, shieldDownSound, shieldHitSound, \
        asteroidExplosion, collectPowerUp, laserSound, clearPowerUp, selectionSound, deathSound, collected, collectedScore, isRunning \
        , animation

    # Death Sound
    deathSound.play()

    # Stop Other Sounds
    accelerationSound.stop()
    superStarMusic.stop()
    shieldHitSound.stop()
    shieldDownSound.stop()
    shieldInit.stop()
    asteroidExplosion.stop()
    collectPowerUp.stop()
    laserSound.stop()
    clearPowerUp.stop()
    selectionSound.stop()
    winSound.stop()

    # Stop Music
    pygame.mixer.music.stop()

    # Re-initialize collected and stop animation
    if campaignMode:
        collectedScore = collected
        collected = 0
        animation = False

    # Menu and inPlay switched off
    menuScreen = False
    inPlay = False

    # If not in endscreen, go to endscreen
    # If in endscreen, exit game
    if end:
        isRunning = False
        endScreen = False
    else:
        endScreen = True


def reInit() -> None:
    """ (None) -> None
        Reinitializes some fields and variables
    """
    global HEIGHT, rotationStep, rotationStepBh, timeInS, stage, fireBlast, blackHoleAngle, \
        referenceTime0, elapsed, asteroids, blackHoles, powerups, WIDTH, playButtonEnd, titleEnd, shipAngle, scorePos, highScore, newLevel

    # Re-initialization of game variables
    spaceship.xPos = WIDTH//2
    spaceship.yPos = HEIGHT//2
    spaceship.yVel = 0
    spaceship.xVel = 0
    rotationStep = 10
    shipAngle = 0
    bhAngle = 0
    rotationStepBh = 20
    timeInS = 0
    stage = 0
    fireBlast = False
    blackHoleAngle = 0
    elapsed = 0
    referenceTime0 = 0
    spaceship.shieldhp = 0
    spaceship.x1 = spaceship.xPos
    spaceship.y1 = spaceship.yPos-30
    spaceship.x2 = spaceship.xPos + spaceship.spaceShipWidth
    spaceship.y2 = spaceship.yPos-30
    spaceship.x3 = spaceship.xPos + spaceship.spaceShipWidth
    spaceship.y3 = spaceship.yPos + spaceship.spaceShipHeight-15
    spaceship.x4 = spaceship.xPos
    spaceship.y4 = spaceship.yPos + spaceship.spaceShipHeight-15
    spaceship.spaceShipRect = pygame.draw.polygon(gameWindow, SPACEBLUE, ((spaceship.x1, spaceship.y1),
                                                                          (spaceship.x2, spaceship.y2), (spaceship.x3, spaceship.y3), (spaceship.x4, spaceship.y4)), 1)
    spaceship.mass = spaceship.init_health
    spaceship.powerUpState = False
    spaceship.laser = False
    spaceship.shield = False
    spaceship.superStar = False
    spaceship.fireCast = False
    spaceship.antiGravity = False
    titleEnd = (WIDTH/2-(round(1018*WIDTH/1680)/2)) - 3280
    playButtonEnd = (WIDTH/2-(round(195*WIDTH/1680))) - 3280
    scorePos = 10000
    asteroids.clear()
    blackHoles.clear()
    powerups.clear()
    spaceship.lasers.clear()
    spaceship.health = spaceship.init_health
    spaceship.nitroAmount = spaceship.nitroAmountInit
    spaceship.centerX = (spaceship.x1 + spaceship.x3)/2
    spaceship.centerY = (spaceship.y1 + spaceship.y3)/2
    spaceship.laserX = (spaceship.x1 + spaceship.x4)/2
    spaceship.laserY = (spaceship.y1 + spaceship.y4)/2
    highScore = False
    pygame.mixer.music.load("sounds/themeMusic/starman.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)
    newLevel = True
    spaceship.acceleration = spaceship.init_accel
    spaceship.nitro = spaceship.initNitro


# Campaign functions ----------------------------------------------------------


def nextLevel() -> None:
    """ (None) -> None
    Goes to the next level and changes the max amount of collectibles needed
    """
    global maxCollected, collected, level, collectedScore, specialLevel, superNitro, infNitro

    # Increments the level and maxCollected by 1
    maxCollected += 1
    level = maxCollected

    # Gets score
    collectedScore = collected

    # Re-initializes collected
    collected = 0

    # Special Level
    if level % 4 == 0 and level >= 4:
        specialLevel = True
    else:
        specialLevel = False

    # Special Levels Powers Switched Off
    spaceship.laser = False
    superNitro = False
    infNitro = False


def nextLevelAnim() -> None:
    """ (None) -> None
        Performs the animation for the next level transition
    """
    global ORIGINALship, backgroundPos, animationPos, animVel, animDecelerate, animation, inPlay, animRotate, hyperdriveIndex

    # Event clearing and getting keys
    pygame.event.clear()
    keys = pygame.key.get_pressed()

    # Stop Sounds
    accelerationSound.stop()
    superStarMusic.stop()
    shieldHitSound.stop()
    shieldDownSound.stop()
    shieldInit.stop()
    asteroidExplosion.stop()
    collectPowerUp.stop()
    laserSound.stop()
    clearPowerUp.stop()
    selectionSound.stop()

    # Stop Music
    pygame.mixer.music.stop()

    # Blit background
    gameWindow.blit(spaceAnimation, (backgroundPos, animationPos))

    # Draw Spaceship
    spaceship.drawSpaceShip()

    # Move Spaceship
    spaceship.move()

    # Reset Position
    spaceship.xPos, spaceship.yPos = WIDTH/2, HEIGHT/2

    # Clear obstables and lasers
    blackHoles.clear()
    asteroids.clear()
    spaceship.lasers.clear()

    # Move background
    animationPos = (animationPos % - HEIGHT) + animVel*cos(shipAngle*pi/180)
    backgroundPos = (backgroundPos % - WIDTH) + animVel*sin(shipAngle*pi/180)

    # Hyperdrive effect
    if animVel >= 250:
        animDecelerate = True

    # Acceleration / Decceleration
    if animDecelerate:
        animVel -= 6
    else:
        animVel += 4

    # Next Level
    if animVel <= 0:
        animDecel = False
        animation = False
        inPlay = True
        reInit()

    # Rotation Spaceship
    spaceship.spaceShip = spaceship.rotate(shipAngle)

    # Hyperdrive animation
    ORIGINALship = spaceship.hyperdrive[hyperdriveIndex//4]
    hyperdriveIndex = (hyperdriveIndex + 1) % 16

    # Display Update
    pygame.display.update()

# Image Copies for rotation

# Spaceship class instance
spaceship = Spaceship()

# Original laser scaling
ORIGINALlaser = pygame.transform.scale(spaceship.laserBullet, (50, 50))

# Copy images
spaceship.spaceShip = ORIGINALship.copy()
spaceship.laserBullet = ORIGINALlaser.copy()
spaceship.shieldDisplay = ORIGINALshield.copy()

#=============================================================================#
#                                                                             #
#                               Program Loop                                  #
#                                                                             #
#=============================================================================#
while isRunning:

    #=============================================================================#
    #                                                                             #
    #                                Menu Loop                                    #
    #                                                                             #
    #=============================================================================#
    while menuScreen:
        # Event clearing and initializing keys
        pygame.event.clear()
        keys = pygame.key.get_pressed()

        # Background blitted
        gameWindow.blit(spaceBackground, (backgroundPos, 0))
        backgroundPos = (backgroundPos % - WIDTH) - 1

        # Menu Rendered
        renderMenu()

        # Exit
        if exitGame() and time.time() - exitRef >= 0.5:
            isRunning = False
            menuScreen = False
            inPlay = False
            endScreen = False

            exitRef = time.time()
        pygame.display.update()

    # Clock initialized
    clock = pygame.time.Clock()

    FPS = 30

    #=============================================================================#
    #                                                                             #
    #                                Game Loop                                    #
    #                                                                             #
    #=============================================================================#

    while inPlay:

        # Exit
        if exitGame() and time.time() - exitRef >= 0.5:
            gameOver()
            exitRef = time.time()

        # Time ticking
        clockTime = clock.tick(FPS)

        # Background blitting
        gameWindow.blit(spaceBackground, (backgroundPos, 0))
        backgroundPos = (backgroundPos % - WIDTH) - 1
        keys = pygame.key.get_pressed()
        pygame.event.clear()

        # Display
        displayHealth()
        displayNitro()

        # Shield collision and handling ---------------------------------------
        if spaceship.shield:

            # Shield blitting and rotation
            gameWindow.blit(spaceship.shieldDisplay, (spaceship.xPos-spaceship.spaceShipWidth-30,
                                                      spaceship.yPos-spaceship.spaceShipHeight-10))
            spaceship.shieldDisplay = spaceship.rotateShield(shieldAngle)
            shieldAngle += shieldRotationStep

            # Shield collision and handling
            for i in range(len(asteroids)):
                if dist((asteroids[i].x, asteroids[i].y), (spaceship.xPos+40, spaceship.yPos+40)) <= 90 + asteroids[i].radius:
                    spaceship.shieldhp -= 1

                    # Asteroid animation
                    for j in range(39):
                        asteroids[i].explosionAnimStage += 1
                        asteroids[i].asteroid = asteroids[i].explosion[asteroids[i].explosionAnimStage//5]
                        gameWindow.blit(asteroids[i].asteroid, (asteroids[i].x, asteroids[i].y))

                    # Sound
                    shieldHitSound.play()
                    asteroidExplosion.play()
                    asteroids.pop(i)
                    break

        # Clear powerup -------------------------------------------------------
        if spaceship.fireCast:
            fireBlast = True


        if fireBlast:
            # Clear powerup animation
            if stage < 28:
                gameWindow.blit(fireCast[stage], (spaceship.xPos-(stage*50), spaceship.yPos-(stage*50)))
                stage += 1
            else:
                fireBlast = False

        # Spaceship drawing and movement --------------------------------------
        spaceship.drawSpaceShip()
        spaceship.move()

        # Powerup collision ---------------------------------------------------
        getPowerUp()

        # Time
        timeTick = clockTime/1000
        if endlessMode:
            displayTime(timeInS, 1400, 66)
            timeInS += timeTick

        elif campaignMode:
            displayCollected(collected, maxCollected, 1400, 66)


        # Movement ------------------------------------------------------------
        if keys[pygame.K_w]:
            spaceship.accelerate(shipAngle)
            spaceship.spaceShip = spaceship.rotate(shipAngle)
            shipAngle -= 0
            accelerationSound.set_volume(0.1)

            # Booster Animation
            if spaceship.ignitionAnimStage < 2:
                spaceship.ignitionAnimStage += 1
                ORIGINALship = spaceship.ignitionAnim[spaceship.ignitionAnimStage]
            elif spaceship.ignitionAnimStage == 2:
                # Engine Animation
                ORIGINALship = spaceship.engineAnim[spaceship.engineAnimStage//4]
                spaceship.engineAnimStage = (spaceship.engineAnimStage + 1) % 16

            # Rotation Controls
            if keys[pygame.K_d]:
                shipAngle -= rotationStep
                spaceship.rotateHitbox(1)
            elif keys[pygame.K_a]:
                shipAngle += rotationStep
                spaceship.rotateHitbox(-1)

            # Nitro -----------------------------------------------------------
            if keys[pygame.K_SPACE] and spaceship.nitroAmount != 0:
                spaceship.useNitro()
                accelerationSound.set_volume(0.2)

                # Nitro Booster Animation
                if spaceship.nitroIgnitionAnimStage < 2:
                    spaceship.nitroIgnitionAnimStage += 1
                    ORIGINALship = spaceship.nitroIgnitionAnim[spaceship.nitroIgnitionAnimStage]
                elif spaceship.nitroIgnitionAnimStage == 2:
                    # Engine Animation
                    ORIGINALship = spaceship.nitroEngineAnim[spaceship.engineAnimStage // 4]
                    spaceship.engineAnimStage = (spaceship.engineAnimStage + 1) % 16

                spaceship.ignitionAnimStage = 0

            # Play Engine Sound
            if not pygame.mixer.get_busy():
                accelerationSound.play()

            elif not keys[pygame.K_SPACE] or spaceship.nitroAmount == 0:

                # Booster Animation
                if spaceship.ignitionAnimStage < 2:
                    spaceship.ignitionAnimStage += 1
                    ORIGINALship = spaceship.ignitionAnim[spaceship.ignitionAnimStage]
                if spaceship.ignitionAnimStage == 3:
                    # Engine Animation
                    ORIGINALship = pygame.image.load("images/rocketship.png")
                spaceship.acceleration = spaceship.init_accel

        # No movement ---------------------------------------------------------
        if not keys[pygame.K_w]:
            accelerationSound.stop()
            spaceship.ignitionAnimStage = 0
            ORIGINALship = pygame.image.load("images/rocketshipOff.png")
            spaceship.spaceShip = spaceship.rotate(shipAngle)
            # No movement rotation
            if keys[pygame.K_d]:
                shipAngle -= rotationStep
                spaceship.spaceShip = spaceship.rotate(shipAngle)
                spaceship.rotateHitbox(1)
            elif keys[pygame.K_a]:
                shipAngle += rotationStep
                spaceship.spaceShip = spaceship.rotate(shipAngle)
                spaceship.rotateHitbox(-1)

        # Shoot lasers --------------------------------------------------------
        if keys[pygame.K_r] and spaceship.laser and time.time() - referenceTime1 >= 0.2:
            laserSound.play()
            # Append Laser Pseudo-Object
            spaceship.lasers.append([
                                    spaceship.laserX + (80 * -cos((shipAngle-90)*pi/180)), # Initial x-position
                                     spaceship.laserY + (80 * sin((shipAngle-90)*pi/180)),  # Initial y-position
                                     shipAngle, # Angle
                                     True, # Initial rotation control boolean
                                     pygame.image.load("images/laserBullet.png") # Display image
                                     ])
            referenceTime1 = time.time()

        # Obstacle appending --------------------------------------------------
        if time.time() - elapsed >= 1:

            # Appending asteroids
            if randint(1, 4) == 1:
                addAsteroids(3)
                elapsed = time.time()

            # Appending blackHoles
            if randint(1, 50) == 1:
                if randint(1, 2) == 1:
                    addBlackHoles(1)
                else:
                    addWhiteHoles(1)
            # Appending power ups
            if randint(1, 8) == 1 and not specialLevel:
                addPowerUp(1)

            # Appending collectibles
            if campaignMode:
                if randint(0, 6) == 0:
                    addCollectible(2)

        # Campaign Mode -------------------------------------------------------
        if campaignMode:
            # Collectible colllision
            getCollectible()

            # Collectible cap
            if collected > maxCollected:
                collected = maxCollected

            # Collectibles clearing
            if maxCollected == collected and inPlay:
                referenceTime2 += timeTick
                collectibles.clear()

            # Level Win
            if referenceTime2 >= 0.5:
                winSound.play()
                referenceTime2 = 0
                inPlay = False
                animation = True
                nextLevel()

            # Special Level Power
            if specialLevel and newLevel:
                levelPower = randint(0, 2)
                if levelPower == 0:
                    spaceship.laser = True
                elif levelPower == 1:
                    spaceship.nitro = 2*spaceship.initNitro
                    superNitro = True
                elif levelPower == 2:
                    infNitro = True
                newLevel = False

        # Black Holes / White Holes
        for j in range(len(blackHoles)):
            if dist((spaceship.centerX, spaceship.centerY), (blackHoles[j].xCenter, blackHoles[j].yCenter)) \
                    <=(23/36)*blackHoles[j].radius + 60 and not spaceship.antiGravity:
                gameOver()

            # Black Hole/White Hole Rotation
            blackHoles[j].display = blackHoles[j].rotate(blackHoleAngle)
            blackHoleAngle += 20

        # Asteroid Drawing and Moving
        for asteroid in range(len(asteroids)):
            asteroids[asteroid].draw()

        # Black Hole Drawing and Moving
        for blackHole in range(len(blackHoles)):
            blackHoles[blackHole].move()

        # Power Up Drawing and Moving
        for powerup in range(len(powerups)):
            powerups[powerup].move()

        # Collectible Drawing and Moving
        if campaignMode:
            for collectible in range(len(collectibles)):
                collectibles[collectible].move()

        # Border Deletion -----------------------------------------------------

        # Asteroid Deletion From Border
        for i in range(len(asteroids)):
            if -160 >= asteroids[i].x - asteroids[i].radius or WIDTH+160 <= asteroids[i].x + asteroids[i].radius:
                asteroids.pop(i)
                break
            if -160 >= asteroids[i].y - asteroids[i].radius or HEIGHT+160 <= asteroids[i].y + asteroids[i].radius:
                asteroids.pop(i)
                break

        # Black Hole / White Hole Deletion From Border
        for i in range(len(blackHoles)):
            if -800 >= blackHoles[i].x - blackHoles[i].radius or WIDTH+800 <= blackHoles[i].x + blackHoles[i].radius:
                blackHoles.pop(i)
                break
            if -800 >= blackHoles[i].y - blackHoles[i].radius or HEIGHT+800 <= blackHoles[i].y + blackHoles[i].radius:
                blackHoles.pop(i)
                break

        # Power Up Deletion From Border
        for i in range(len(powerups)):
            if -240 >= powerups[i].x - powerups[i].radius or WIDTH+240 <= powerups[i].x + powerups[i].radius:
                powerups.pop(i)
                break
            if -240 >= powerups[i].y - powerups[i].radius or HEIGHT+240 <= powerups[i].y + powerups[i].radius:
                powerups.pop(i)
                break

        # Collectible Deletion From Border
        for collectible in range(len(collectibles)):
            if -240 >= collectibles[collectible].x or WIDTH+240 <= collectibles[collectible].x:
                collectibles.pop(collectible)
                break
            if -240 >= collectibles[collectible].y or HEIGHT+240 <= collectibles[collectible].y:
                collectibles.pop(collectible)
                break

        # Game Over From Border
        if -200 >= spaceship.xPos or WIDTH+200 <= spaceship.xPos:
            gameOver()
        if -200 >= spaceship.yPos or WIDTH+200 <= spaceship.yPos:
            gameOver()
        for i in range(len(blackHoles)):
            blackHoles[i].move()

        # Gravity and Asteroid Behaviour --------------------------------------

        # Gravity
        objectGravity()

        # Asteroid Movement Initialization
        moveAsteroidInit()

        # Asteroid Spaceship Collision
        collideAsteroid()

        # Asteroid Asteroid Collision
        asteroidCollideAsteroid()

        # Power Up Display ----------------------------------------------------

        # Laser
        if spaceship.laser:

            # Laser Collision
            if len(spaceship.lasers) > 0:
                laserCollideAsteroid()

            # Asteroid Icon Blitting
            gameWindow.blit(pygame.image.load("images/powerUps/96x96/laserIcon.png"), (600, 50))

        # Shield
        elif spaceship.shield:

            # Shield Icon Blitting
            gameWindow.blit(pygame.image.load("images/powerUps/96x96/shieldIcon.png"), (600, 50))

            # Shield Hitpoints Blitting
            for i in range(spaceship.shieldhp):
                gameWindow.blit(pygame.image.load("images/powerUps/96x96/shieldDisplay.png"), (1030+(i*100), 66))

        # Super Star
        elif spaceship.superStar:

            # Super Star Icon Blitting
            gameWindow.blit(pygame.image.load("images/powerUps/96x96/superStarIcon.png"), (600, 50))

        # Anti-Gravity
        elif spaceship.antiGravity:

            # Anti-Gravity Icon Blitting
            gameWindow.blit(pygame.image.load("images/powerUps/96x96/antiGravityIcon.png"), (600, 50))

        # Campaign Special Level Handling
        if campaignMode:

            # Super Nitro
            if superNitro:

                # Super Nitro Icon Blitting
                gameWindow.blit(pygame.image.load("images/powerUps/96x96/ultraNitroIcon.png"), (600, 50))

            # Infinite Nitro
            elif infNitro:

                # Infinite Nitro Icon Blitting
                gameWindow.blit(pygame.image.load("images/powerUps/96x96/infNitroIcon.png"), (600, 50))

                # Infinite Nitro Handling
                if spaceship.nitroAmount < 100:
                    spaceship.nitroAmount = 100

        # Laser Rotation and Movement
        for i in range(len(spaceship.lasers)):

            # Checking For Initial Rotation Boolean
            if spaceship.lasers[i][3]:

                # Laser Rotation
                spaceship.lasers[i][4] = spaceship.rotateLaser(spaceship.lasers[i][2]+90)
                spaceship.lasers[i][3] = False

            # Laser Blitting
            gameWindow.blit(spaceship.lasers[i][4], (spaceship.lasers[i][0], spaceship.lasers[i][1]))

            # Laser Movement
            spaceship.lasers[i][0] += (80 * -cos((spaceship.lasers[i][2]-90)*pi/180))
            spaceship.lasers[i][1] += (80 * sin((spaceship.lasers[i][2]-90)*pi/180))

            # Laser Image
            ORIGINALlaser = spaceship.laserBullet

        # Spaceship Death
        if spaceship.health <= 0:
            gameOver()

        # Pygame Display Update
        pygame.display.update()

    #=========================================================================#
    #                                                                         #
    #                             Animation Loop                              #
    #                                                                         #
    #=========================================================================#

    while animation:

        # Keys Initialization
        keys = pygame.key.get_pressed()

        # Exit Handling
        if exitGame() and time.time() - exitRef >= 0.5:
            gameOver()
            exitRef = time.time()

        # Clock Tick
        clockTime = clock.tick(FPS)

        # Spaceship Movement
        spaceship.move()

        # Animation to Next Level
        nextLevelAnim()

    #=========================================================================#
    #                                                                         #
    #                             End Screen Loop                             #
    #                                                                         #
    #=========================================================================#

    while endScreen:

        # Pygame Event Clearing
        pygame.event.clear()

        # Keys Initialization
        keys = pygame.key.get_pressed()

        # Moving Background
        gameWindow.blit(spaceBackground, (backgroundPos, 0))
        backgroundPos = (backgroundPos % - WIDTH) + 1

        # Score Blitting Initialization
        if scorePos == 10000:

            # Score Rounding
            score = round(timeInS, 1)

            # High Score
            if score > highScore1:
                highScore = True
                highScore1 = score

            # Score Centering
            scoreWidth, scoreHeight = modeFont.size(f"{score}")
            scorePos = (WIDTH/2-scaleX(scoreWidth)/2) - scaleX(1600)

        # Endscreen Rendering
        renderEnd()

        # Game Exitting
        if exitGame() and time.time() - exitRef >= 0.5:
            gameOver(end=True)
            exitRef = time.time()

        # Pygame Display Update
        pygame.display.update()

# Pygame Quitting
pygame.quit()