# Get light values from ESP32 at regular intervals and store in tLightValues

import mysql.connector
import logging
import requests
import time

from datetime import datetime

# Set up logging
logging.basicConfig(filename="/home/jkumar/Projects/logs/lightTracker/lightTracker.log", level=logging.INFO,format="%(asctime)s:[%(levelname)s]:%(message)s")
logging.info('------------------------------------')
logging.info('lightTracker Application starting up')
logging.info('------------------------------------')

# Create DB Connection
logging.info('Attempting to connect to DB lighttracker')
try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="jkumar",
      password="system64",
      database="lighttracker"
    )
    
    mycursor = mydb.cursor()
except:
    logging.critical('Unable to connect to DB')
    logging.critical('Program will exit')
    quit()

logging.info('Connection to DB successful')

# Setup ESP32 details
lightURL = "http://192.168.1.128/light"
# Sleep time is 10 seconds
sleepTime = 10
retryTime = 5
# Setup consequtive errors after which program should quit
errorTimeout = 20
consErrors = 0
# Setup http request timeout
httpTimeout = 5

logging.info("Setup Complete")
logging.info("ESP32 endpoint: %s",lightURL)
logging.info("Time interval : %s seconds",sleepTime)
logging.info("Retry interval: %s seconds",retryTime)
logging.info("Error timeout : %s",errorTimeout)
logging.info("HTTP timeout  : %s seconds",httpTimeout)

# Create new run in DB
now = datetime.now()
crDate = now.strftime("%Y-%m-%d %H:%M:%S")
sql = "insert into tLightRuns (cr_date) values (%s)"
val = (str(crDate))
try:
    mycursor.execute(sql, val)
    mydb.commit()
    rowID = mycursor.lastrowid
except Exception as e:
    logging.error(str(e))
    logging.error("Unable to add run to DB, exiting")
    quit()

logger.info("Starting run %s",rowID)

while consErrors < errorTimeout:

    try:
        r = requests.get(lightURL, timeout=httpTimeout)
    except:
        consErrors = consErrors + 1
        logging.error("Unable to connect to %s retries %s/%s",lightURL,consErrors,errorTimeout)
        time.sleep(retryTime)
        continue

    respStatus = r.status_code

    if (respStatus != 200):
        consErrors = consErrors + 1
        logging.error("Unsuccessful response %s retries %s/%s",respStatus,consErrors,errorTimeout)
        time.sleep(retryTime)
        continue

    lightValue = r.text
    logging.info("Got light value %s",lightValue)
    # Success reset consErrors
    consErrors = 0

    # Insert value into DB

    # Set to sleep before next request
    time.sleep(sleepTime)

# Error timeout has been reached, exit application
logging.info('Application exiting')
