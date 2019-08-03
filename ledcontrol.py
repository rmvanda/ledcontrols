#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

#import random shit i felt like using
import random
import memcache 
import webcolors

# Configure the count of pixels:
PIXEL_COUNT = 153

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.set("c",0) # c is for clutch. 




#Bare basic functionality. Makes me think... 

class LEDs: 

    def __init__(self,pixels):
        self.pixels = pixels

    def color(self,rgb,g=False,b=False):
        if g is not False and b is not False:
            return Adafruit_WS2801.RGB_to_color(b,g,rgb)
        else:
            return Adafruit_WS2801.RGB_to_color(rgb[2],rgb[1],rgb[0])

    def update(self):
        self.pixels.show();
        return self

    def clear(self):
        self.pixels.clear()
        return self.update()

    def setAll(self,rgb):
        self.pixels.set_pixels(self.color(rgb))
        return self

    def setColor(self,pixel,rgb):
        self.pixels.set_pixel(pixel,self.color(rgb))

    def getColor(self,led=0):
        return self.color(pixels.get_pixel_rgb(led)); #TODO what's the return format? 

    def getRandColor(self,min=0,max=255):
        return [ 
                random.randint(min,max),
                random.randint(min,max),
                random.randint(min,max)
                ]
 
    def on(self,rgb): 
        return self.setAll(rgb).update()

    def off(self):
        return self.clear().update()

    def fadeStepColor(self,oldrgb, newrgb,timing=5,steps=100):
        delay = timing / steps 
        stepAmount = [0,0,0]
        currentrgb = list(oldrgb)
        for x in range(3):
            amnt = (newrgb[x] - oldrgb[x]) // steps
            stepAmount[x] = amnt
            currentrgb[x] = oldrgb[x] 

        for x in range(steps):
            for y in range(3):
                currentrgb[y]+= stepAmount[y]
            self.setAll(currentrgb).update()
            time.sleep(delay);

        return self

    def fadeIn(self,rgb,timing=10,steps=100):
        return self.clear().fadeStepColor([0,0,0],rgb)

    def fadeOut(self):
        return self.fadeStepColor(self.getColor(),[0,0,0])

    def forEach(self,method,delay,**kwargs):
        for led in range(self.pixels.count()): 
            method(led,kwargs)
            self.update()
            time.sleep(delay)


    def ringOn(self,rgb):
        self.forEach(lambda x,params : 
            self.setColor(x,params['rgb']), 
         0.01,
         rgb=rgb)

    def ringOff(self):
        pass
#here, dual and more ring animations for on and off seem more for the 
#Queue bit that I was originally including in the LEDController bit. 
#But, we can certainly include some other advanced things in here such as: 
    background_color = [0,255,255]; 
    last_lit_seat    = 0 
    def lightSection(self,rgb,seat,size=15):
    # actually this gets complicated to the point where we now need the ring cycling thing.. hmm 
        #cur = self.getColor()
        #redundant looking, but it's to reset... 
        
        for x in range(size):
            led = int(seat)*size + x
            if(led >= self.pixels.count()):
                led = led - self.pixels.count() # this should never happen at this point, but hey. 
            self.setColor(led,rgb)
        return self.update()


#python seems painfully inadequate for doing this in an OOP way but kwargs is at least one way it succeeds.. 

    def shimmer(self,**kwargs): #usage: shimmer(r=True,b=True,g=True) // rainbow shimmers!
        if(hasattr(kwargs,"r")):
            r = kwargs['r']
        if(hasattr(kwargs,"b")):
            b = kwargs['b']
        if(hasattr(kwargs,"g")):
            g = kwargs['g']

    def coinFlip(self):
        return random.randint(0,1)

    def getRandUnbiased(self):
        a = [
                random.randint(0,self.coinFlip() and 255),
                random.randint(0,self.coinFlip() and 255),
                random.randint(0,self.coinFlip() and 255)
        ]
        if 1 not in a or sum(a) < 88:
            return self.getRandUnbiased()
        else:
            return a

    def shimmerRandom(self):
        #beau = [0,0,0]
        #for x in range(len(beau)):
        #    beau[x] = random.randint(0,1)
        rgb = self.getRandUnbiased()
        while mc.get("c"):
            for x in range(self.pixels.count()):
                beau = [0,0,0]
                for y in range(3):
                    beau[y] = random.randint(0,rgb[y])
                self.setColor(x,beau)

            self.update()
            time.sleep(0.1)





    def showtime(self,rgb=[255,255,0]):
        for i in range(3):
            for x in (range(self.pixels.count())):
                if((x % 3) == 0):
                    self.setColor(x+i,rgb)

            self.update()
            time.sleep(0.05)
            self.clear()

   


class LEDController: 

    def __init__(self, pixel_count, port=0,device=0):
        self.pixel_count = pixel_count
        self.port        = port
        self.device      = device

        self.pixels = Adafruit_WS2801.WS2801Pixels(pixel_count,spi=SPI.SpiDev(port,device), gpio=GPIO)
    #   All Lists are [R,G,B] - the second one is populated with an _array_ of 
    #   Tuples because that way, if we have two objects animating that intersect, 
    #   We can add their colors together to get something of a combination effect. """
        LEDState = [ [0,0,0]  for x in range(self.pixel_count)]
        LEDQueue = [[[0,0,0]] for x in range(self.pixel_count)]

    #    A method for taking multiple, independent animations and combining them so that they 
    #    do not have to worry about eachother - but also so that if they intersect, their colors
    #    can be combined for the combination effect. 

    def renderMultipleCombined(): 
        self.pixels.clear()
        newState = [ [0,0,0] for x in range(self.pixel_count) ]
        oldState = self.LEDState

    # Here, we're going through all of the queued up colors and adding them together. 
        for colors in self.LEDQueue: 
            for color in colors:
                newState[syncsane][0] += color[0]
                newState[syncsane][1] += color[1]
                newState[syncsane][2] += color[2]
            syncsane +=1 # meh, this is OKAY

        # Here, we're
        syncsane = 0
        for state in self.LEDState: 
            if state == oldState[syncsane]:
                continue

            self.LEDState[syncsane] = self.LEDQueue[syncsane]; 
            self.pixels.set_pixel(syncsane, *state)

    # Ensure that any animations we want to render are registered into our queue

    def registerAnimation():
        pass

    # For when we don't care about combining them. 
    # Last animation rendered shows up on top 
    
    def renderAnimation(): 
        pass


def releaseClutch():
    mc.set("c",0)
    

def engageClutch():
    mc.set("c",1)

def clutch():
    return mc.get("c")

def doAnimation(animation,**params): 
    while clutch():
        animation(params)




class LEDAnimation: 

    def __init__(self,opts):
        self.color = opts.color
        self.width
        self.speed

        pass # hmm... 

    def getColor(x,y):
        pass


a = LEDs(pixels)
