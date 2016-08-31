#!/usr/bin/python
#http://www.recantha.co.uk/blog/?p=4849

import smbus
import time
import MySQLdb
import lcddriver
import datetime

def main():
    print "Creating DB"
    #Connect to DB
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
    db.autocommit(True)
    cur = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    #INSERT INTO temps(id, sensor_id, timestamp, value)
    #VALUES ()"

    bus = smbus.SMBus(1)
    address = 0x20

    #LCD_Add = 0x3f
    data = ""
    temps = list()

    DEVICE_REG_MODE1 = 0x00
    DEVICE_REG_LEDOUT0 = 0x1d
    #Char ON = 'ON'

    oldinput = -1
    oldtemp0 = -1.0
    oldtemp1 = -1.0
    oldtemp2 = -1.0
    print "Starting"

    while True:
        try:
            #DB Stuff
	    #print "Running Query"
            cur = db.cursor()
            cur.execute("SELECT SQL_NO_CACHE name,status FROM test.test1")
            #cur.close
            # loop to iterate
            i=0
            inputs = 0

            for row in cur.fetchall() :
                #data from rows
                #input_name = str(row[0])
                #input_status = str(row[1])
                if row[1]:
                #    print str(row[0]), 'is ON'
                    inputs = inputs + (1 << i)

            else:
                #print str(row[0]), 'is OFF'
                i=i+1
                #print it
               #print input_name + " has status " + input_status

	    #print "Receiving Temps"
            recv = chr(bus.read_byte(address));

            if ord(recv) == 0:
                temps = data.split(",")
                #print ("Temp 1:", temps[0])
                #print ("Temp 2:", temps[1])
                #print ("Temp 3:", temps[2])
		data = ""
		top_temp = float(temps[0])
		bot_temp = float(temps[1])
			
		#print "Old Temp 0: ", oldtemp0 - 0.5
		#print "Top Temp: " , top_temp
		if (top_temp  > (oldtemp0 + 0.5)) or (top_temp < (oldtemp0 - 0.5)) : 
                    update_lcd(temps)
		    oldtemp0 = top_temp
		    update_DB_Temp("HW Top Temp", top_temp)
		    print "LCD Updated 1"
		
		if (bot_temp > (oldtemp1 + 0.5) or (bot_temp < (oldtemp1 - 0.5))) :
		    update_lcd(temps)
		    oldtemp1 = bot_temp
		    update_DB_Temp("HW Bot Temp", bot_temp)
	  	    print "LCD Updated 3"
          
                time.sleep(0.1)

            else:
                # else 
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
                oldinput = inputs

        except Exception as e :
              print ("Error:",str(e))
              time.sleep(1)

def update_DB_Temp(sensor_id, sensor_temp):
    try:
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
        db.autocommit(True)
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print st
	cur = db.cursor()
        cur.execute("INSERT INTO temps( sensor_id, Value, timestamp) VALUES (%s, %s, %s)", (sensor_id, float(sensor_temp), st))
        cur.close  
	print "DB Updated"
	# Execute the SQL command
   	#cursor.execute(sql)
    except Exception as e:
	print ("Error:",str(e))

def update_lcd(temps):
    try:
        #print("Updating LCD \n Temp 1",temps[0])
        lcd = lcddriver.lcd()
        lcd.lcd_display_string("DHW Top " + temps[0] + "DegC", 1)
        lcd.lcd_display_string("DHW Mid " + temps[1] + "DegC", 2)
        lcd.lcd_display_string("DHW Bot " + temps[2] + "DegC", 3)
	print ("Temp 1:", temps[0])
	print ("Temp 2:", temps[1])
	print ("Temp 3:", temps[2])
    except Exception as e:
        lcd.lcd_clear()
        lcd.lcd_display_string("Error Displaying Temps",1)
        lcd.lcd_display_string(str(e),2)

if __name__ == "__main__":
    main()


