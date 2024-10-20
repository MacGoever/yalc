# Bibliotheken laden
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
import machine
import network
import sys
import time
import usocket as socket
import ustruct as struct
import _thread
import random
import math
from WIFI_CONFIG import SSID, PASSWORD
from ota import OTAUpdater


#dusk and dawn
duskhours = 18
dawnhours = 6
duskduration = 30
dawnduration = 30



def last_sunday(year: int, month: int, hour: int, minute: int) -> int:
        """Get the time of the last sunday of the month
        It returns an integer which is the number of seconds since Jan 1, 2000, just like mktime().
        """
        # Get the UTC time of the last day of the month
        seconds = time.mktime((year, month + 1, 0, hour, minute, 0, None, None))

        # Calculate the offset to the last sunday of the month
        (year, month, mday, hour, minute, second, weekday, yearday) = time.gmtime(seconds)
        offset = (weekday + 1) % 7

        # Return the time of the last sunday of the month
        return time.mktime((year, month, mday - offset, hour, minute, second, None, None))





def getTime():
    # WLAN-Konfiguration
    wlanSSID = SSID
    wlanPW = PASSWORD

    
    # Status-LED
    led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)

    # NTP-Host
    NTP_HOST = 'pool.ntp.org'
    
    wlan = network.WLAN(network.STA_IF)
        
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B

    ntp_success = False
    
    
    local_secs = 0
    
    if not wlan.isconnected(): 
		print('initiating Wifi...')
			
		wlan.active(True)
		print(wlanSSID)
		wlan.connect(wlanSSID, wlanPW)
		for i in range(10):    #retry wifi connect 10 times
			if wlan.status() < 0 or wlan.status() >= 3:
				break
			led_onboard.toggle()
			print('.')
			time.sleep(1)
		
		if wlan.isconnected():
			print('Wifi connected. Status:', wlan.status())
			print('Wifi parameters: ', wlan.ifconfig())
			led_onboard.on()
		else:
			print('Wifi connection error. Status: ', wlan.status())
			led_onboard.off()
			
		if wlan.isconnected():
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
				s.settimeout(1)
				res = s.sendto(NTP_QUERY, addr)
				msg = s.recv(48)
			except:
				print("Something went wrong during the NTP query")
			else:
				ntp_secs = struct.unpack("!I", msg[40:44])[0]
				utc_secs =  ntp_secs - NTP_DELTA
				utc = time.gmtime(utc_secs)
				print ("NTP says UTC is " + str(utc[3]) + ":" + str(utc[4]) + ":" + str(utc[5]) + " on " + str(utc[2]) + "." + str(utc[1]) + "." + str(utc[0]))                
			
			
				# Find start date for daylight saving, i.e. last Sunday in March (01:00 UTC)
				start_secs = last_sunday(year=utc[0], month=3, hour=1, minute=0)

				# Find stop date for daylight saving, i.e. last Sunday in October (01:00 UTC)
				stop_secs = last_sunday(year=utc[0], month=10, hour=1, minute=0)

			
				if utc_secs >= start_secs and utc_secs < stop_secs:
					delta_secs = 2 * 60 * 60  # (CEST or UTC + 2h)
					print ("It's CEST!")            
				else:
					delta_secs = 1 * 60 * 60  # (CET or UTC + 1h)
					print ("It's CET!")

				local_secs = utc_secs + delta_secs
				local_time = time.localtime(local_secs)
				print ("Local time is " + str(local_time[3]) + ":" + str(local_time[4]) + ":" + str(local_time[5]) + " on " + str(local_time[2]) + "." + str(local_time[1]) + "." + str(local_time[0]))                
			
				machine.RTC().datetime((local_time[0], local_time[1], local_time[2], local_time[6], local_time[3], local_time[4], local_time[5], 0))
				ntp_success = True
			finally: 
				s.close()

    return ntp_success
             
pixelmap = [ [-1]*7 for i in range(19)]
pixelmap[0][0] = 73
pixelmap[0][1] = 72
pixelmap[0][2] = 71
pixelmap[0][4] = 70
pixelmap[0][5] = 69
pixelmap[0][6] = 68

pixelmap[3][6] = 67
pixelmap[3][5] = 66
pixelmap[3][4] = 65
pixelmap[3][2] = 64
pixelmap[3][1] = 63
pixelmap[3][0] = 62

pixelmap[4][0] = 61
pixelmap[4][1] = 60
pixelmap[4][2] = 59
pixelmap[4][4] = 58
pixelmap[4][5] = 57
pixelmap[4][6] = 56

pixelmap[7][6] = 55
pixelmap[7][5] = 54
pixelmap[7][4] = 53
pixelmap[7][2] = 52
pixelmap[7][1] = 51
pixelmap[7][0] = 50

pixelmap[9][1] = 49
pixelmap[9][5] = 48

pixelmap[11][6] = 47
pixelmap[11][5] = 46
pixelmap[11][4] = 45
pixelmap[11][2] = 44
pixelmap[11][1] = 43
pixelmap[11][0] = 42

pixelmap[14][0] = 41
pixelmap[14][1] = 40
pixelmap[14][2] = 39
pixelmap[14][4] = 38
pixelmap[14][5] = 37
pixelmap[14][6] = 36

pixelmap[15][6] = 35
pixelmap[15][5] = 34
pixelmap[15][4] = 33
pixelmap[15][2] = 32
pixelmap[15][1] = 31
pixelmap[15][0] = 30

pixelmap[18][0] = 29
pixelmap[18][1] = 28
pixelmap[18][2] = 27
pixelmap[18][4] = 26
pixelmap[18][5] = 25
pixelmap[18][6] = 24

pixelmap[1][0] = 0
pixelmap[2][0] = 1
pixelmap[5][0] = 2
pixelmap[6][0] = 3
pixelmap[12][0] = 4
pixelmap[13][0] = 5
pixelmap[16][0] = 6
pixelmap[17][0] = 7

pixelmap[1][3] = 15
pixelmap[2][3] = 14
pixelmap[5][3] = 13
pixelmap[6][3] = 12
pixelmap[12][3] = 11
pixelmap[13][3] = 10
pixelmap[16][3] = 9
pixelmap[17][3] = 8

pixelmap[1][6] = 16
pixelmap[2][6] = 17
pixelmap[5][6] = 18
pixelmap[6][6] = 19
pixelmap[12][6] = 20
pixelmap[13][6] = 21
pixelmap[16][6] = 22
pixelmap[17][6] = 23

def setNumber(numberIndex, number, numberRGB, backRGB):
    ledsNumber = []
    ledsBackground = []
    if numberIndex == 0:
            ledsBackground = [0,1,14,15,16,17,62,63,64,65,66,67,68,69,70,71,72,73]
            if number == 0:
                ledsNumber = [0,1,16,17,62,63,64,65,66,67,68,69,70,71,72,73]
            if number == 1:
                ledsNumber = [62,63,64,65,66,67]
            if number == 2:
                ledsNumber = [0,1,14,15,16,17,65,66,67,71,72,73]
            if number == 3:
                ledsNumber = [0,1,14,15,16,17,62,63,64,65,66,67]
            if number == 4:
                ledsNumber = [14,15,62,63,64,65,66,67,68,69,70]
            if number == 5:
                ledsNumber = [0,1,14,15,16,17,62,63,64,68,69,70]
            if number == 6:
                ledsNumber = [0,1,14,15,16,17,62,63,64,68,69,70,71,72,73]
            if number == 7:
                ledsNumber = [16,17,62,63,64,65,66,67]
            if number == 8:
                ledsNumber = [0,1,14,15,16,17,62,63,64,65,66,67,68,69,70,71,72,73]
            if number == 9:
                ledsNumber = [0,1,14,15,16,17,62,63,64,65,66,67,68,69,70]

    if numberIndex == 1:
            ledsBackground = [2,3,12,13,18,19,50,51,52,53,54,55,56,57,58,59,60,61]
            if number == 0:
                ledsNumber = [2,3,18,19,50,51,52,53,54,55,56,57,58,59,60,61]
            if number == 1:
                ledsNumber = [50,51,52,53,54,55]
            if number == 2:
                ledsNumber = [2,3,12,13,18,19,53,54,55,59,60,61]
            if number == 3:
                ledsNumber = [2,3,12,13,18,19,50,51,52,53,54,55]
            if number == 4:
                ledsNumber = [12,13,50,51,52,53,54,55,56,57,58]
            if number == 5:
                ledsNumber = [2,3,12,13,18,19,50,51,52,56,57,58]
            if number == 6:
                ledsNumber = [2,3,12,13,18,19,50,51,52,56,57,58,59,60,61]
            if number == 7:
                ledsNumber = [18,19,50,51,52,53,54,55]
            if number == 8:
                ledsNumber = [2,3,12,13,18,19,50,51,52,53,54,55,56,57,58,59,60,61]
            if number == 9:
                ledsNumber = [2,3,12,13,18,19,50,51,52,53,54,55,56,57,58]

    if numberIndex ==  2:
            ledsBackground = [4,5,10,11,20,21,36,37,38,39,40,41,42,43,44,45,46,47]
            if number == 0:
                ledsNumber = [4,5,20,21,36,37,38,39,40,41,42,43,44,45,46,47]
            if number == 1:
                ledsNumber = [36,37,38,39,40,41]
            if number == 2:
                ledsNumber = [4,5,10,11,20,21,36,37,38,42,43,44]
            if number == 3:
                ledsNumber = [4,5,10,11,20,21,36,37,38,39,40,41]
            if number == 4:
                ledsNumber = [10,11,36,37,38,39,40,41,45,46,47]
            if number == 5:
                ledsNumber = [4,5,10,11,20,21,39,40,41,45,46,47]
            if number == 6:
                ledsNumber = [4,5,10,11,20,21,39,40,41,42,43,44,45,46,47]
            if number == 7:
                ledsNumber = [20,21,36,37,38,39,40,41]
            if number == 8:
                ledsNumber = [4,5,10,11,20,21,36,37,38,39,40,41,42,43,44,45,46,47]
            if number == 9:
                ledsNumber = [4,5,10,11,20,21,36,37,38,39,40,41,45,46,47]

    if numberIndex ==  3:
            ledsBackground = [6,7,8,9,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
            if number == 0:
                ledsNumber = [6,7,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
            if number == 1:
                ledsNumber = [24,25,26,27,28,29]
            if number == 2:
                ledsNumber = [6,7,8,9,22,23,24,25,26,30,31,32]
            if number == 3:
                ledsNumber = [6,7,8,9,22,23,24,25,26,27,28,29]
            if number == 4:
                ledsNumber = [8,9,24,25,26,27,28,29,33,34,35]
            if number == 5:
                ledsNumber = [6,7,8,9,22,23,27,28,29,33,34,35]
            if number == 6:
                ledsNumber = [6,7,8,9,22,23,27,28,29,30,31,32,33,34,35]
            if number == 7:
                ledsNumber = [22,23,24,25,26,27,28,29]
            if number == 8:
                ledsNumber = [6,7,8,9,22,23,24,25,26,27,28,29,30,31,32,33,34,35]
            if number == 9:
                ledsNumber = [6,7,8,9,22,23,24,25,26,27,28,29,33,34,35]

  
    for k in ledsBackground :
        np[k] = backRGB
        
    for k in ledsNumber :
        np[k] = numberRGB
        
def setNumberInMatrix(outputMatrix, numberIndex, number, numberRGB, backRGB):
    xStart = 0
    if numberIndex == 1:
        xStart = 4
    if numberIndex == 2:
        xStart = 11
    if numberIndex == 3:
        xStart = 15

    for x in range(0,4):
        for y in range(0,7):
            outputMatrix[x + xStart][y] = backRGB
    
    if number == 0:
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[0 + xStart][0] = numberRGB
        outputMatrix[0 + xStart][1] = numberRGB
        outputMatrix[0 + xStart][2] = numberRGB
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
    if number == 1:
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
    if number == 2:
        outputMatrix[0 + xStart][0] = numberRGB
        outputMatrix[0 + xStart][1] = numberRGB
        outputMatrix[0 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 3:
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 4:
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 5:
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 6:
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[0 + xStart][0] = numberRGB
        outputMatrix[0 + xStart][1] = numberRGB
        outputMatrix[0 + xStart][2] = numberRGB
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 7:
        ledsNumber = [16,17,62,63,64,65,66,67]
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
    if number == 8:
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[0 + xStart][0] = numberRGB
        outputMatrix[0 + xStart][1] = numberRGB
        outputMatrix[0 + xStart][2] = numberRGB
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
    if number == 9:
        outputMatrix[1 + xStart][0] = numberRGB
        outputMatrix[2 + xStart][0] = numberRGB
        outputMatrix[1 + xStart][6] = numberRGB
        outputMatrix[2 + xStart][6] = numberRGB
        outputMatrix[3 + xStart][1] = numberRGB
        outputMatrix[3 + xStart][0] = numberRGB
        outputMatrix[3 + xStart][2] = numberRGB
        outputMatrix[3 + xStart][4] = numberRGB
        outputMatrix[3 + xStart][5] = numberRGB
        outputMatrix[3 + xStart][6] = numberRGB
        outputMatrix[0 + xStart][4] = numberRGB
        outputMatrix[0 + xStart][5] = numberRGB
        outputMatrix[0 + xStart][6] = numberRGB
        outputMatrix[1 + xStart][3] = numberRGB
        outputMatrix[2 + xStart][3] = numberRGB
        
    return outputMatrix

def setColonInMatrix(outputMatrix, upperRGB, lowerRGB):
        outputMatrix[9][1] = upperRGB
        outputMatrix[9][5] = lowerRGB      
        return outputMatrix


def setColon(upperRGB, lowerRGB):
    np[48] = upperRGB
    np[49] = lowerRGB


               
    
