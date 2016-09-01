#!/usr/bin/python
#http://www.recantha.co.uk/blog/?p=4849

import smbus
import time
import MySQLdb
import lcddriver
import datetime
from db_helper import MyDB


def main():
    print "Creating DB"
    #Connect to DB
    db = MyDB('localhost', 'root', '', 'test')
    db.autocommit(True)
    
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
    temp_upper = [0.5, 0.5, 0.5]
    temp_lower = [0.5, 0.5, 0.5]

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
            		    print "LCD Updated 1"

                if temps_changed:
                    update_lcd(temps, temp_names)

                time.sleep(0.1)

            else:
                data = data + recv

                if(inputs != oldinput):
                   # print inputs     
                    bus.write_byte(address, inputs)
                    oldinput = inputs

        except Exception as e :
              print ("Error:",str(e))
              time.sleep(1)



def update_lcd(temps, temp_names):
    try:
        #print("Updating LCD \n Temp 1",temps[0])
        lcd = lcddriver.lcd()
        for i in range(0,3)
            lcd.lcd_display_string(temp_names[i] + temps[i] + "DegC", i)
    	print ("Temp 1:", temps[0])
    	print ("Temp 2:", temps[1])
    	print ("Temp 3:", temps[2])
    except Exception as e:
        lcd.lcd_clear()
        lcd.lcd_display_string("Error Displaying Temps",1)
        lcd.lcd_display_string(str(e),2)

def temp_in_limits(upper, lower, setpoint, temp):
    return (temp  > (setpoint + upper)) or (temp < (setpoint - lower))

if __name__ == "__main__":
    main()


