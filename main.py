# Bibliotheken laden
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from collections import deque
import machine
import network
import sys
import time
import usocket as socket
import ustruct as struct
import random
import math
import helper
from WIFI_CONFIG import SSID, PASSWORD
from ota import OTAUpdater

firmware_url = "https://github.com/MacGoever/yalc/refs/heads/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py", "helper.py")
ota_updater.download_and_install_update_if_available()


helper.getTime()



cookooDone = False
tempint = 0



currentDisplay = [ [(0,0,0)]*7 for i in range(19)]
plannedDisplay = [ [(0,0,0)]*7 for i in range(19)]

color = (0,0,200)
bgcolor = (0,0,0)
red = (255,0,0)
green = (0,255,0)


upperDot = green
lowerDot = red
dotDelay = 1000
dotCount = 0




# Neopixel WS2812
pin_np = 0

leds = 74

delay_normal = 10





# Initialisierung WS2812/NeoPixel
np = NeoPixel(Pin(pin_np, Pin.OUT), leds)
np.fill((255,0,0))
np.write()
sleep_ms(500)

np.fill((0,255,0))
np.write()
sleep_ms(500)

np.fill((0,0,255))
np.write()
sleep_ms(500)

np.fill((0,0,0))
np.write()

def getPixel(x,y):
    ledIndex = helper.pixelmap[x][y]
    return np[ledIndex]

def setPixel (x,y,color):
    npIndex = helper.pixelmap[x][y]
    if npIndex != -1:
        np[npIndex] = color

def fadeTo(fromMatrix, toMatrix, step):
    outMatrix = [ [(0,0,0)]*7 for i in range(19)]
    for x in range(0,19):
        outTupel = [0,0,0]
        for y in range(0,7):
            fromTupel = fromMatrix[x][y]
            toTupel = toMatrix[x][y]
            for colorRGB in range(0,3):
                if ((fromTupel[colorRGB] + step) < toTupel[colorRGB]):
                    outTupel[colorRGB] = fromTupel[colorRGB] + step
                elif ((fromTupel[colorRGB] - step) > toTupel[colorRGB]):
                    outTupel[colorRGB] = fromTupel[colorRGB] - step
                else:
                    outTupel[colorRGB] = toTupel[colorRGB]
            outMatrix[x][y] = tuple(outTupel)
    
    return outMatrix



def doAnimation (step):
    for i in range (0,19):
        colorFactor =  step
        #print(colorFactor)
        #colorFactor = math.sin(1/3*i+2*math.pi*step)+1
        for j in range (0,7):
            color = getColor(i,j)
            newColor = (int(color[0] * colorFactor), int(color[1] * colorFactor), int(color[2] * colorFactor))
            setPixel(i,j,newColor)






def cookoo2():
    time = machine.RTC().datetime()
    hours = time[4] % 10
    hoursPoTen = time[4] // 10
    minutes = time[5] % 10
    minutesPoTen = time[5] // 10
    
    colors=[(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(0,255,255),(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(0,255,255)]
    
    for k in range(20):
        cookoo2Color = colors[k]
        plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 0 ,hoursPoTen, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 3) % 20]
        plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 1 ,hours, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 7) % 20]
        plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 2 ,minutesPoTen, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 11) % 20]
        plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 3 ,minutes, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 15) % 20]
        plannedDisplay = helper.setColonInMatrix(plannedDisplay, cookoo2Color, cookoo2Color)
            
        for j in range(255 / 20):       
            currentDisplay = fadeTo(currentDisplay, plannedDisplay, 20)
                     
            for x in range(0,19):
                for y in range(0,7):
                    setPixel(x,y,currentDisplay[x][y])

            np.write()
            
            sleep_ms(delay_normal)

                
    

def cookoo1():

    for i in range (0,2):
        for i in range (0,19):
            for j in range (0,7):
                setPixel (i, j, (0,0,255))
                np.write()
                sleep_ms(10)       

        for i in range (0,19):
            for j in range (0,7):
                setPixel (i, j, (0,255,0))
                np.write()
                sleep_ms(10)  

        for i in range (0,19):
            for j in range (0,7):
                setPixel (i, j, (255,0,0))
                np.write()
                sleep_ms(10)  

#cookoos = [cookoo1,cookoo2]
cookoos = [cookoo1]


def doCookoo():
    cookoos.append(cookoos.pop(0))
    cookoos[0]()


while True:
    #set time
    time = machine.RTC().datetime()
    hours = time[4] % 10
    hoursPoTen = time[4] // 10
    minutes = time[5] % 10
    minutesPoTen = time[5] // 10
    
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 0 ,hoursPoTen, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 1 ,hours, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 2 ,minutesPoTen, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 3 ,minutes, color, bgcolor)
    plannedDisplay = helper.setColonInMatrix(plannedDisplay, upperDot , lowerDot)
       
    dotCount = dotCount + delay_normal
    if dotCount >= dotDelay:
        tempDot = lowerDot
        lowerDot = upperDot
        upperDot = tempDot
        dotCount = 0

    currentDisplay = fadeTo(currentDisplay, plannedDisplay, 20)
 
    if (time[5] == 0 or time[5] == 15 or time[5] == 30 or time[5] == 45 ):
    #if (time[5] != tempint):
        if not cookooDone:
            doCookoo()
            cookooDone = True
            #tempint = time[5]
    else:
        cookooDone = False
            
            
    for x in range(0,19):
        for y in range(0,7):
            setPixel(x,y,currentDisplay[x][y])

    np.write()
    
    sleep_ms(delay_normal)
