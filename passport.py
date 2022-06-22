import sys
import argparse
import time
import hashlib
import logging
from urllib.request import urlopen, Request


parser = argparse.ArgumentParser()

parser.add_argument("appointmentType", nargs="?", default="premium", 
	help='Set as premium or fasttrack dependant on the type of appointment you want to check for')

args = parser.parse_args()

if args.appointmentType == "premium":
  url = Request('https://www.passport.service.gov.uk/urgent/',
			headers={'User-Agent': 'Mozilla/5.0'})
elif args.appointmentType == "fasttrack":
  url = Request('https://www.passportappointment.service.gov.uk/outreach/publicbooking.ofml',
			headers={'User-Agent': 'Mozilla/5.0'})

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info("Running Passport Appointment Checker for " + args.appointmentType + " appointments.")	
log.info("Checking every 30 seconds...")

if 'url' in locals():
	log.info('Variable Set')
else:
	log.error("Incorrect varible set")
	sys.exit(1)

response = urlopen(url).read()
currentHash = hashlib.sha224(response).hexdigest()

time.sleep(10)
while True:
	try:
		response = urlopen(url).read()
		currentHash = hashlib.sha224(response).hexdigest()
		
		time.sleep(30)

		response = urlopen(url).read()

		newHash = hashlib.sha224(response).hexdigest()

		if newHash == currentHash:
			continue

		else:

			log.info("Website has changed, maybe there are new appoitments")

			response = urlopen(url).read()

			currentHash = hashlib.sha224(response).hexdigest()
			time.sleep(30)
			continue
			
	# To handle exceptions
	except Exception as e:
		log.error(str(e))
