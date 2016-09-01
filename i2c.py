#!/usr/bin/python
#http://www.recantha.co.uk/blog/?p=4849

import smbus
import time
import MySQLdb
import lcddriver
import datetime
from db_helper import MyDB
import sys, os

def main():
    #Start Main
    print "Creating DB"
    #Connect to DB
    db = MyDB('localhost', 'root', '', 'test')
    #db.autocommit(True)
    
    #i2c Variables
    bus = smbus.SMBus(1)
    address = 0x20

    #LCD Variables
    data = ""
    temps = list()
    DEVICE_REG_MODE1 = 0x00
    DEVICE_REG_LEDOUT0 = 0x1d

    #Digital Input Variables
    oldinput = -1

    #Temperature Variables
    temp_names = ["HW Top Temp", "HW Bot Temp", "Hot Press"]
    temp_old = [-1.0,-1.0,-1.0] # Used to initialise the variables
    temp_upper = [0.1, 0.1, 0.1]
    temp_lower = [0.1, 0.1, 0.1]

    print "Starting"

    while True:
        try:
            #DB Stuff
            i=0
            inputs = 0

            for row in db.get_inputs_status() :
  
                if row[1]: #if input is ON
                    inputs = inputs + (1 << i)

            else: 
                i=i+1

            recv = chr(bus.read_byte(address));

            if ord(recv) == 0: #if end character received
                temps = data.split(",")
                data = ""

                temps_changed = False
                for i in range(0, len(temp_names)):
                    if temp_in_limits(temp_upper[i], temp_lower[i], temp_old[i], temps[i]) :
                        temps_changed = True
                        temp_old[i] = temps[i]
                        db.update_temp(temp_names[i], temps[i])
                        

                if temps_changed:
                    update_lcd(temps, temp_names)
                    print "LCD Updated"

                time.sleep(0.1)

            else:
                data = data + recv

                if(inputs != oldinput):
                   # print inputs     
                    bus.write_byte(address, inputs)
                    oldinput = inputs

        except Exception as e :
	      exc_type, exc_obj, exc_tb = sys.exc_info()
	      print ("Error at Line No:", exc_tb.tb_lineno)
              print ("Main Loop Error:",str(e))
              time.sleep(1)



def update_lcd(temps, temp_names):
    try:
        #print("Updating LCD \n Temp 1",temps[0])
        lcd = lcddriver.lcd()
        for i in range(0,3):
            lcd.lcd_display_string(temp_names[i] + str(temps[i]) + "DegC", i)
        print ("Temp 1:", str(temps[0]))
        print ("Temp 2:", str(temps[1]))
        print ("Temp 3:", str(temps[2]))
    except Exception as e:
        lcd.lcd_clear()
        lcd.lcd_display_string("Error Displaying Temps",1)
        lcd.lcd_display_string(str(e),2)

def temp_in_limits(upper, lower, setpoint,temp):
    try:
	#print ("Temp is %s. Old Value is %s. Upper Limit is %s. Lower Limit is %s") % (str(temp), str(setpoint),str(float(setpoint)+float(upper)), str(float(setpoint)-float(lower)))
    	return (float(temp)  > (float(setpoint) + float(upper))) or (float(temp) < (float(setpoint) - float(lower)))
    except Exception as e:
	print ("temp_in_limits Error", str(e))

if __name__ == "__main__":
    main()


