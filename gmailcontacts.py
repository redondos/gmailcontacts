#!/usr/bin/env python
# gmailcontacts.py - search for contacts in a Gmail account
# Author: Angel Olivera <redondos@aolivera.com.ar>

import getopt, getpass, os, re, sys, libgmail

def main():
	USER = PASS = VERBOSE = None

	try:
		if len(os.environ['GMAILUSER']) >0:
			USER=os.environ['GMAILUSER']
			if len(os.environ['GMAILPASS']) >0:
				PASS=os.environ['GMAILPASS']
	except:
		pass

	try:
		opts, args = getopt.getopt(sys.argv[1:], "vu:p:", ["verbose", "username=", "password="])
	except getopt.GetoptError:
		pass

	for o, a in opts:
		if o in ("-u", "--username"):
			USER=a
		elif o in ("-p", "--password"):
			PASS=a
		elif o in ["-v", "--verbose"]:
			VERBOSE=True

	if USER == None or PASS == None:
		if USER == None:
			USER = raw_input("Gmail account: ")
		PASS = getpass.getpass("Password: ")

	if VERBOSE:
		print "Using username: " + USER
	account = libgmail.GmailAccount(USER, PASS)

	try:
		if VERBOSE:
			print "Logging in..."
		account.login()
	except libgmail.GmailLoginFailure,e:
		print e.message
	except:
		pass
	else:
		if VERBOSE:
			print "Login successful."
		if len(args) >0:
			# Lookup string was supplied in command line
			lookup = " ".join(args)
		else:
			lookup = raw_input("Lookup string: ")
		if VERBOSE:
			print "Looking up: " + lookup
		try:
			contacts = account.getContacts().getContactListByName(lookup)
			contacts_pattern = re.compile('[^ ]* ([^@]*) .*')
			contact_match_pattern = re.compile('[^ ,]*@[^ ,]*.[^ ,]*')
			if contacts != False:
				if VERBOSE:
					print "Results:"
				for i in range(len(contacts)):
					contact_name = contacts_pattern.match(str(contacts[i]))
					contact_item = str(contacts[i]).split()
					# Name empty? No way, Gmail doesn't let us.
					# if contact_item[1] != "":
					c=0
					for j in range(len(contact_item)):
						# print contact_item[j]
						contact_match = contact_match_pattern.match(contact_item[j])
						if contact_match != None:
							print contact_match.group() + "\t" + contact_name.group(1)
							c = c+1
			else:
				print "No contacts were found."
		except:
			pass


if __name__ == "__main__":
	main()
