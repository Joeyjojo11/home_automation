#!/usr/bin/python
#http://www.recantha.co.uk/blog/?p=4849

import smbus
import time
import MySQLdb
import lcddriver



print "Creating DB"
#Connect to DB
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
db.autocommit(True)
#cur = db.cursor()

bus = smbus.SMBus(1)
address = 0x20

#LCD_Add = 0x3f
data = ""
temps = list()

DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d
#Char ON = 'ON'

oldinput = -1
print "Starting"

while True:
    try:
        
        #DB Stuff
        cur = db.cursor()
        cur.execute("SELECT SQL_NO_CACHE name,status FROM test.test1")
        cur.close
        # loop to iterate
        i=0
        inputs = 0
        
        for row in cur.fetchall() :
            #data from rows
            #input_name = str(row[0])
            #input_status = str(row[1])
            if row[1]:
                print str(row[0]), 'is ON'
                inputs = inputs + (1 << i)

            else:
                print str(row[0]), 'is OFF'
            i=i+1
            #print it
            #print input_name + " has status " + input_status
            
        
        recv = chr(bus.read_byte(address));
	
        if ord(recv) == 0:
            temps = data.split(",")
            print ("Temp 1:", temps[0])
            print ("Temp 2:", temps[1])
            print ("Temp 3:", temps[2])
            time.sleep(0.1)
            
        else:
	    #print data
            data = data + recv

        
        '''    
        input1 = False
        input2 = False
        input3 = True
        
        if(input1):
            inputs = inputs + (1 << 0)
        if(input2):
            inputs = inputs + (1 << 1)
        if(input3):
            inputs = inputs + (1 << 2)
        '''
        
        if(inputs != oldinput):   
           # print inputs     
        
            bus.write_byte(address, inputs)
            #bus.write_byte(LCD_Add, inputs)
            oldinput = inputs
        #time.sleep(1)
        #Write an array of registers
        #ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
        #bus.write_i2c_block_data(DEVICE_ADDRESS, DEVICE_REG_LEDOUT0, ledout_values)
                    
    except Exception as e:
        print ("Error:",str(e))
        time.sleep(1)
        
    lcd = lcddriver.lcd()
    lcd.lcd_display_string("DHW Top " + temps[0] + "DegC", 1)
    lcd.lcd_display_string("DHW Mid " + temps[1] + "DegC", 2)   
    lcd.lcd_display_string("DHW Bot " + temps[2] + "DegC", 3)  



#lcd.lcd_display_string("Middle" + temps[1] + " C", 2)
#lcd.lcd_display_string("Bottom" + temps[2] + " C", 3)
#lcd.lcd_display_string("OAT", 4)        

