# Bibliotheken laden
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from time import sleep_us
import machine
import network
import sys
import time
import usocket as socket
import ustruct as struct
import random
import math
from helper import getPixel
from helper import setPixel
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
currentDisplay = np.buf
timeDisplay = [0] * leds * 3

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
#helper.getWifi()

firmware_url = "https://github.com/MacGoever/yalc/refs/heads/main/"
ota_updater = OTAUpdater(firmware_url, "main.py", "helper.py")
#ota_updater.download_and_install_update_if_available()

cookooDone = False

#currentDisplay = [ [(0,0,0)]*7 for i in range(19)]
#timeDisplay = [ [(0,0,0)]*7 for i in range(19)]


upperDot = green
lowerDot = red
dotDelay = 1000
dotCount = 0




def fadeTo(buf, duration):
    global currentDisplay
    stepDuration_us = 15*1000
    numberOfSteps = math.trunc(duration / stepDuration_us * 1000)
    if not numberOfSteps:
        numberofSteps = 1

    diffMatrix = [0] * leds * 3
    tempMatrix = [0] * leds * 3

    preFillTime=time.ticks_us()
    #calc the diffs 
    for index, (current, planned) in enumerate(zip(currentDisplay,buf)):
        #diffMatrix[index] = math.trunc((current - planned) / numberOfSteps)
        diffMatrix[index] = (current - planned) / numberOfSteps
        tempMatrix[index] = current
    
    fillTime=time.ticks_diff(time.ticks_us(),preFillTime)

    #do the fading
    
    for i in range(0,numberOfSteps-1):
        preStepTime=time.ticks_us()
        for index, diff in enumerate(diffMatrix):
            #currentDisplay[index] = currentDisplay[index] + diff
            currentDisplay[index] = tempMatrix[index] + round(diff * i)
                
        np.write()
        
        stepTime=time.ticks_diff(time.ticks_us(),preStepTime)

        if (stepTime + fillTime) < stepDuration_us:
            
            sleep_us(stepDuration_us - stepTime - fillTime)
            
        fillTime=0

    #finalize the transfer
    preStepTime=time.ticks_us()
    for index, finalValue in enumerate(buf):
        currentDisplay[index] = finalValue
                
    np.write()
        
    stepTime=time.ticks_diff(time.ticks_us(),preStepTime)

    sleep_us(stepDuration_us - stepTime)
           
##################################################
#Cookoos
##################################################
#color fade digits
def cookoo5(timeDisplay, ocolor, bgcoler):
    
    colors=[(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(0,255,255),(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(255,0,0),(255,255,0),(255,255,255),(255,255,0),(0,255,0),(0,0,255),(0,255,255)]
    
    for k in range(20):
        cookoo2Color = colors[k]
        timeDisplay = helper.setNumberInMatrix(timeDisplay, 0 ,hoursPoTen, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 3) % 20]
        timeDisplay = helper.setNumberInMatrix(timeDisplay, 1 ,hours, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 7) % 20]
        timeDisplay = helper.setNumberInMatrix(timeDisplay, 2 ,minutesPoTen, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 11) % 20]
        timeDisplay = helper.setNumberInMatrix(timeDisplay, 3 ,minutes, cookoo2Color, bgcolor)
        cookoo2Color = colors[(k + 15) % 20]
        timeDisplay = helper.setColonInMatrix(timeDisplay, cookoo2Color, cookoo2Color)
            
        for j in range(255 / 20):       
            #currentDisplay = fadeTo(currentDisplay, timeDisplay, 20)
                     
            for x in range(0,19):
                for y in range(0,7):
                    setPixel(x,y,currentDisplay[x][y])

            np.write()
            
            sleep_ms(delay_normal)

#color flip numbers
def cookoo3(timeDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0)]

    for k in range (0,15):
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (0,5):
            for j in range (0,7):
                if getPixel(currentDisplay,i,j) != bgcolor:
                    setPixel(currentDisplay,i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (4,9):
            for j in range (0,7):
                if getPixel(currentDisplay,i,j) != bgcolor:
                    setPixel(currentDisplay,i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (9,11):
            for j in range (0,7):
                if getPixel(currentDisplay,i,j) != bgcolor:
                    setPixel(currentDisplay,i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (11,16):
            for j in range (0,7):
                if getPixel(currentDisplay,i,j) != bgcolor:
                    setPixel(currentDisplay,i, j, color)
        color = colors[0]
        colors.append(colors.pop(0))
        for i in range (15,19):
            for j in range (0,7):
                if getPixel(currentDisplay,i,j) != bgcolor:
                    setPixel(currentDisplay,i, j, color)
        np.write()
        sleep_ms(300)
                    
#color from bottom to top
def cookoo2(timeDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0),(255,255,255),ocolor]
    for k in range (0,5):
        for color in colors:
            for j in range (0,7):
                for i in range (0,19):
                    if getPixel(currentDisplay,i,j) != bgcolor:
                        setPixel(currentDisplay,i, j, color)
                np.write()
                sleep_ms(20)       

#color from left to right
def cookoo1(timeDisplay, ocolor, bgcoler):
    colors = [(0,255,255),(0,0,255),(255,0,255),(255,255,0),(255,0,0),(0,255,0),(255,255,255),ocolor]

    for k in range (0,5):
        for color in colors:
            for i in range (0,19):
                for j in range (0,7):
                    if getPixel(currentDisplay, i,j) != bgcolor:
                        setPixel(currentDisplay, i, j, color)
                np.write()
                sleep_ms(20)
                    

        
#escaping digits
def cookoo4(timeDisplay, ocolor, bgcoler):
    print("Test")
    
            
cookoos = [cookoo1,cookoo2,cookoo3]

def doCookoo(timeDisplay, color, bgcoler):
    cookoos[0](timeDisplay, color, bgcoler)
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
    timeTupel = machine.RTC().datetime()
    #print(time)
    hours = timeTupel[4] % 10
    hoursPoTen = timeTupel[4] // 10
    minutes = timeTupel[5] % 10
    minutesPoTen = timeTupel[5] // 10
    
    #choose color depending on daytime
    if timeTupel[4] > 18 or timeTupel[4] < 5:
        color=(200,0,0)
    if timeTupel[4] > 5 and timeTupel[4] < 10:
        color=(0,0,255)
    if timeTupel[4] > 10 and timeTupel[4] < 18:
        color=(0,255,0)    
    
    #generate time display
    timeDisplay = helper.setNumber(0 ,hoursPoTen, color, bgcolor, timeDisplay)
    timeDisplay = helper.setNumber(1 ,hours, color, bgcolor, timeDisplay)
    timeDisplay = helper.setNumber(2 ,minutesPoTen, color, bgcolor, timeDisplay)
    timeDisplay = helper.setNumber(3 ,minutes, color, bgcolor, timeDisplay)
    timeDisplay = helper.setColon(upperDot, lowerDot, timeDisplay)
       
    if timeTupel[6] != last_sec:
        last_sec = timeTupel[6]
        
        if last_sec % 2 == 0:
            lowerDot = color
            upperDot = color
        else:
            lowerDot = bgcolor
            upperDot = bgcolor

    fadeTo( timeDisplay, 950)
            
    #check if an NTP request is needed
    if timeTupel[5] != last_minute:
        last_minute = timeTupel[5]

        ntp_counter += -1
        if not ntp_success:
            ntp_success = helper.getTime()
            ntp_counter=42
        elif ntp_counter == 0:
            ntp_success = helper.getTime()
            ntp_counter=42

    #Every 15 minutes do something fancy with colors 
    if timeTupel[6] == 0: #and timeTupel[5] in [0,15,30,45]:
    #if time[6] == 0 and True:
        lowerDot = color
        upperDot = color
        helper.setColon(upperDot , lowerDot,timeDisplay)

        #doCookoo(timeDisplay, color, bgcolor)

        try:
            doCookoo(timeDisplay, color, bgcolor)
        except:
            print("You messed up during cookoo")
