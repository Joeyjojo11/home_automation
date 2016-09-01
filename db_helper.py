import sys
import MySQLdb as mdb
import time
import datetime

class MyDB():

	def __init__(self, host, user, passw, db):
		try:
			self.con = mdb.connect(host, user, passw, db)
			self.cur = self.con.cursor()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

	def show_version(self):
			self.cur.execute("SELECT VERSION()")
			print "Database version : %s " % self.cur.fetchone()

	def test1(self):
		# Do something with self.con or self.cur
		self.cur.execute("SELECT name from test1 where id=1")
		print "First Item : %s " % self.cur.fetchone()

	def test2(self):
		# Do something with self.con or self.cur
		self.cur.execute("SELECT name from test1 where id=2")
		print "Second Item : %s " % self.cur.fetchone()

	def update_temp(self, sensor_id, sensor_temp):
		try:
			
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			#print st
			self.cur.execute("INSERT INTO temps( sensor_id, Value, timestamp) VALUES (%s, %s, %s)", (sensor_id, float(sensor_temp), st))
			print "Temps Updated"
			# Execute the SQL command
			#cursor.execute(sql)
		except Exception as e:
			print ("Error:",str(e))

	def get_inputs_status(self):
		self.cur.execute("SELECT SQL_NO_CACHE name,status FROM test.test1")
		return self.cur.fetchall()


if __name__ == '__main__':  # If it's executed like a script (not imported)
	db = MyDB('localhost', 'root', '', 'test')
	db.show_version()
	db.test1()
	db.test2()
