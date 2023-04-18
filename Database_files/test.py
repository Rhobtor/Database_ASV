import time
import datetime
import mysql.connector as mysql
import pymysql
from mysql.connector import MySQLConnection, Error
# from python_mysql_dbconfig import read_db_config
import MySQLdb
import mariadb
# General settings
# prog_name = "pilogger2.py"

# Settings for database connection
hostname = '172.17.0.1'
username = 'root'
password = 'ROOT_ACCESS_PASSWORD'
database = 'Datas'
port= 3306

# Routine to insert temperature records into the pidata.temps table:
def insert_record(ID, prct_batery, latitud,longitud,sensor_sonar,date):
	query = "INSERT INTO sensors (ID,prct_batery,latitud,longitud,sensor_sonar,date) " \
                "VALUES (%s,%s,%s,%s,%s,%s)"
    
	args = (ID,prct_batery,latitud,longitud,sensor_sonar,date)

	try:
		conn = pymysql.connect( host=hostname, user=username, passwd=password ,db=database, port=port )
		cursor_ = conn.cursor()
		cursor_.execute(query, args)
		conn.commit()

	except Exception as error:
			print(error)
		

	finally:
			cursor_.close()
			conn.close()

# # Print welcome 
# print('[{0:s}] starting on {1:s}...'.format(prog_name, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

# Main loop
try:
	while True:
		
		ID =  1
		prct_batery= 2
		latitud=3
		longitud=4
		sensor_sonar=5
		now = datetime.datetime.now()
		date = now.strftime('%Y-%m-%d %H:%M:%S')
		insert_record(format(ID,'.0f'),format(prct_batery,'.0f'),format(latitud,'.2f'),format(longitud,'.2f'),format(sensor_sonar,'.2f'),str(date))
		time.sleep(180)

except (IOError,TypeError) as e:
	print("Exiting...")

except KeyboardInterrupt:  
    	# here you put any code you want to run before the program   
    	# exits when you press CTRL+C  
	print("Stopping...")

finally:
	print("Cleaning up...")  
	# GPIO.cleanup() # this ensures a clean exit
