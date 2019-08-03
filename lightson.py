
# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

#import random shit i felt like using
import random
 
# Configure the count of pixels:
PIXEL_COUNT = 153
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


def adacolor(rgb,g=False,b=False):
    if g and b: 
        return Adafruit_WS2801.RGB_to_color(b,g,rgb)
    else:
        return Adafruit_WS2801.RGB_to_color(rgb[2],rgb[1],rgb[0])



def  lightsOn(color=(255,255,255)):
    pixels.set_pixels(adacolor(color)); 
    pixels.show(); 

def lightsOff():
    pixels.clear(); 
    pixels.show();

def shimmerRandom(): 
    for x in range(PIXEL_COUNT):
        pixels.set_pixel(x,adacolor(getRandomColor()))
    pixels.show();
    time.sleep(0.1);


def getRandomColor():
    return (
             random.randint(0,255), 
             random.randint(0,255), 
             random.randint(0,255)
        )

def showtime():
    for i in range(3):
        for x in range(PIXEL_COUNT):
            if((x % 3) == 0):
                pixels.set_pixel(x+i,adacolor((255,255,0)))

        pixels.show()
        pixels.clear() # according to my notes, 
        # it should clear after sleeping, but 
        # this is how I had it, and it WAS working, so... 
        # current implementation is : 
        # show->sleep->clear
        # YMMV
        time.sleep(0.05)

def shimmer(color):
    for x in range(PIXEL_COUNT):
        pixels.set_pixel(x,adacolor((0, random.randint(0,255),random.randint(0,255))))
    pixels.show()
    time.sleep(0.1)

SEAT_COUNT = 10
SEAT_WIDTH = PIXEL_COUNT // SEAT_COUNT

def lightSeat(seatNo, color):
    pixels.set_pixels(adacolor((255,255,255)))
    pixels.show()
    for x in range(SEAT_WIDTH):
        led = seatNo * SEAT_WIDTH + x;
        if(led >= 153):
            led = led - 153
        pixels.set_pixel(led, adacolor((255,0,0)))
    pixels.show()



if __name__ == "__main__": 
    i = 0;

    while i < 10 : 
        lightsOn(getRandomColor)
        time.sleep(1)
        i=i+1

    i = 0
    while i < 30 : 
        showtime()
        i=i+1
    i = 0
    while i < 30 : 
        shimmer(True)
        i=i+1
    


    for x in range(1,SEAT_COUNT+1):
        lightSeat(x,adacolor((255,255,255)))
        time.sleep(1)

    #while True: shimmer(True) ; 
    #while True: showtime() ; 
    
    #shimmerRandom()
    #lightsOn(getRandomColor()); 
