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


color = (0,0,200)
bgcolor = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

# display test
pin_np = 0
leds = 74
delay_normal = 10

np = NeoPixel(Pin(pin_np, Pin.OUT), leds)
np.fill(red)
np.write()
sleep_ms(500)

np.fill(green)
np.write()
sleep_ms(500)

np.fill(blue)
np.write()
sleep_ms(500)

np.fill(bgcolor)
np.write()

#get time and Wifi
helper.getWifi()

firmware_url = "https://github.com/MacGoever/yalc/refs/heads/main/"
ota_updater = OTAUpdater(firmware_url, "main.py", "helper.py")
ota_updater.download_and_install_update_if_available()

cookooDone = False
tempint = 0

currentDisplay = [ [(0,0,0)]*7 for i in range(19)]
plannedDisplay = [ [(0,0,0)]*7 for i in range(19)]


upperDot = green
lowerDot = red
dotDelay = 1000
dotCount = 0


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

##################################################
#Cookoos
##################################################

def cookoo5():
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

#color flip numners
def cookoo3(plannedDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0)]

    for k in range (0,15):
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (0,3):
            for j in range (0,7):
                if getPixel(i,j) != bgcolor:
                    setPixel (i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (4,7):
            for j in range (0,7):
                if getPixel(i,j) != bgcolor:
                    setPixel (i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (9,9):
            for j in range (0,7):
                if getPixel(i,j) != bgcolor:
                    setPixel (i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (11,14):
            for j in range (0,7):
                if getPixel(i,j) != bgcolor:
                    setPixel (i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (15,18):
            for j in range (0,7):
                if getPixel(i,j) != bgcolor:
                    setPixel (i, j, color)
        np.write()
        sleep_ms(300)
                    
    for i in range (0,18):
        for j in range (0,7):
            if getPixel(i,j) != bgcolor:
                setPixel (i, j, ocolor)
    np.write()

#color from bottom to top
def cookoo2(plannedDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0)]
    for k in range (0,5):
        for color in colors:
            for j in range (0,7):
                for i in range (0,19):
                    if getPixel(i,j) != bgcolor:
                        setPixel (i, j, color)
        np.write()
        sleep_ms(20)       

    for j in range (0,7):
        for i in range (0,19):
            if getPixel(i,j) != bgcolor:
                setPixel (i, j, ocolor)
        np.write()
        sleep_ms(20)  


#color from left to right
def cookoo1(plannedDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0)]

    for k in range (0,5):
        for color in colors:
            for i in range (0,19):
                for j in range (0,7):
                    if getPixel(i,j) != bgcolor:
                        setPixel (i, j, color)
                np.write()
                sleep_ms(10)
                    
    for i in range (0,19):
        for j in range (0,7):
            if getPixel(i,j) != bgcolor:
                setPixel (i, j, ocolor)
            np.write()
            sleep_ms(10)
            
cookoos = [cookoo1,cookoo2,cookoo3]

def doCookoo(plannedDisplay, color, bgcoler):
    cookoos[0](plannedDisplay, color, bgcoler)
    cookoos.append(cookoos.pop(0))
    
##################################################
#Cookoos Ende
##################################################

ntp_success = False
ntp_counter = 10
last_minute = 0
last_sec = 0


while True:
    #set time
    time = machine.RTC().datetime()
    hours = time[4] % 10
    hoursPoTen = time[4] // 10
    minutes = time[5] % 10
    minutesPoTen = time[5] // 10
    
    #choose color depending on daytime
    if time[4] > 18 or time[4] < 5:
        color=(200,0,0)
    if time[4] > 5 and time[4] < 10:
        color=(0,0,255)
    if time[4] > 10 and time[4] < 18:
        color=(0,255,0)    
    
    #generate time display
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 0 ,hoursPoTen, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 1 ,hours, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 2 ,minutesPoTen, color, bgcolor)
    plannedDisplay = helper.setNumberInMatrix(plannedDisplay, 3 ,minutes, color, bgcolor)
    plannedDisplay = helper.setColonInMatrix(plannedDisplay, upperDot , lowerDot)
       
    if time[6] != last_sec:
        last_sec = time[6]
        
        if last_sec % 2 == 0:
            lowerDot = color
            upperDot = color
        else:
            lowerDot = bgcolor
            upperDot = bgcolor
            
    if time[5] != last_minute:
        last_minute = time[5]

        ntp_counter += -1
        if not ntp_success:
            ntp_success = helper.getTime()
            ntp_counter=42
        elif ntp_counter == 0:
            ntp_success = helper.getTime()
            ntp_counter=42

    #if (time[5] in [0,5,30,45]):
        try:
            doCookoo(plannedDisplay, color, bgcolor)
        except:
            print("You messed up during cookoo")
                    

    currentDisplay = fadeTo(currentDisplay, plannedDisplay, 20)
            
    for x in range(0,19):
        for y in range(0,7):
            setPixel(x,y,currentDisplay[x][y])

    np.write()
    
    sleep_ms(delay_normal)
