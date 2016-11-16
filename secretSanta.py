# Jed Kafetz
# You need a list of email addresses named emailaddresses.txt in the dir of this program

import gnupg
from pprint import pprint
import random

randomNum = list()
randomNum2 = list()

def packFile(person):


	gpg = gnupg.GPG(gnupghome='/home/jed/.gnupg')
	# replace 0.0.0.0 with IP or address of keyserver
	keydata = gpg.search_keys(person.emailAddress, '0.0.0.0')
#	print keydata, person.Name
	keydata= str(keydata)
	start = keydata.find('keyid\': u\'')+10
	end = keydata.find('\', \'uids', start)
	keyid = keydata[start:end]
	import_result = gpg.recv_keys('192.168.2.73', keyid)
	dataToEncrypt = "Your secret number is " + str(person.randomNumber) + "\n " 
	encrypted_string = gpg.encrypt(dataToEncrypt , keyid, always_trust=True)
#	print encrypted_string.stderr
	with open(person.Name+".txt.pgp", "w") as f:
		f.write(encrypted_string.data)

	print keyid

def generateNumber(person, lineCount, randomNum2):
	tempNum = random.randint(1, lineCount)
#	print randomNum2
	attempt = 0
	if tempNum in randomNum2 or tempNum == person.assignednumber:
		while tempNum in randomNum2 or tempNum == person.assignednumber:
			tempNum = random.randint(1, lineCount)
			attempt = attempt + 1
			if attempt == 15:
				print "Please run the program again"
				exit()
#			print "testing" + str(tempNum)
	randomNum2.append(tempNum)
	print str(person.Name) + "  Assigned Number is:  " + str(person.assignednumber) + "\n "
	return tempNum
	
def createPerson(emaillist, lineCount, randomNum2):
# for each email address in the list
	for person in emaillist:
		# Take there name
		name = person.split(".")
		# Create an object of there name
		name[0]= teamMember(name[0], person, 0, lineCount)
		name[0].randomNumber = generateNumber(name[0], lineCount, randomNum2)
		packFile(name[0])
		fixings = name[0].Name + " is " + str(name[0].assignednumber) + "\n"
		with open("WhoYourNumberMeans", "a") as j:
			j.write(fixings)
# Creating object
class teamMember(object):
	Name = ""
	emailAddress = ""
	randomNumber = 0
	assignednumber = 0

	def __init__(self, Name, emailAddress, randomNumber, lineCount):
		self.Name = Name
		self.emailAddress = emailAddress
		self.randomNumber = 0
		# make a temp num that does not exist
		# add the number to a list, if the number is in the list, try again
		tempNum = random.randint(1, lineCount)
		while tempNum in randomNum:
			tempNum = random.randint(1, lineCount)
		randomNum.append(tempNum)
		self.assignednumber = tempNum


# Open file which contains Email address
with open("emailaddresses.txt") as f:
	emailList = f.readlines()
# Get the amount of people within the file
num_lines = sum(1 for line in open('emailaddresses.txt'))
# Send the amount of people with number of lines plus randomNum2 list
createPerson(emailList, num_lines, randomNum2)
