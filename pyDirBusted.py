#!/usr/bin/python3
""" 
*** pyDirBusted ***

Author: Jeremy Schoeneman (y4utj4)
Thanks to: Coldfusion39 and zero_steiner for the help!!
 
pyDirBuster is a python version of DirBuster which brute-forces and enumerates directories within a website. 
You'll need your own directory wordlist. 

** Distributed under the GNU General Public License. See LISCENSE file **

"""

import aiohttp
import argparse
import asyncio
import signal
from urllib.parse import urlparse
import urllib.request

@asyncio.coroutine
def get_status(site, verbose, outfile, sem):
	
	with (yield from sem):
		response = yield from aiohttp.request('GET', site, compress=True)

	# Prints / outputs status
	if response.status == 200: # Site Reached
		if verbose:
			print("[+] FOUND: {0} - Code:{1}".format(site, response.status))
		if outfile:
			outfile.write("{0}: {1}".format(response.status, site) + '\n')
	elif 300 < response.status < 308: # Web Redirects
		if verbose:
			print("[!] Web Redirect: {0} - Code:{1}".format(site, response.status))	
		if outfile:
			outfile.write("{0}: {1}".format(response.status, site) + '\n')
	elif response.status == 401: # Authorization Required
		if verbose:
			print("[!] Authorization Required: {0} - Code:{1}".format(site, response.status))
		if outfile:
			outfile.write("{0}: {1}".format(response.status, site) + '\n')
	elif response.status == 403: # Forbidden
		if verbose:
			print("[!] Forbidden: {0} - Code:{1}".format(site, response.status))
	elif response.status == 404: # Website not found
		if verbose:
			print("[-] Not Found: {0} - Code:{1}".format(site, response.status))
	elif response.status == 503: # Service Unavailable
		if verbose:
			print("[-] Service Unavailable: {0} - Code:{1}".format(site, response.status))
	else:
		if verbose: #catch all. Look up the status number
			print("[?] Unknown Response: {0} - Code:{1}".format(site, response.status))
	yield from response.release()

def signal_handler():
	# cleans up
	print('Stopping all tasks')
	for task in asyncio.Task.all_tasks():
		task.cancel()

def url_checker(url):
	# Checks to see if your site is valid first. If not, attempts to add the appropriate
	# scheme (https, then http) and if still fails, shows site error. 
	# Using urlparser/urllib.request to check for valid url. 
	parsed_url = urlparse(url)	
	if not parsed_url.scheme == None:
		secure_url = "https://" + url
		try:
			urllib.request.urlopen(secure_url)
			return secure_url
		except:
			url = "http://" + url
			urllib.request.urlopen(url)
			return url
		else:
			print ('It appears your site isn\'t valid. Please verify your input and run again.')
			return False

 #	trying to convert to aiohttp, not working. returns generator object
#	parsed_url = urlparse(url)	
#	if not parsed_url.scheme == None:
#		secure_url = 'https://' + url
#		response = yield from aiohttp.request('GET', secure_url)
#		if resp.status == 200:
#			return secure_url
#		else:
#			unsecure_url = 'http://' + url
#			response = yield from aiohttp.request('GET', unsecure_url)
#			if response.status == 200:
#				return unsecure_url
#			else:
#				print ('[-] It appears your site (' + url + ') isn\'t valid. Please verify your input and run again.')
#	else:
#		return url

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Python web directory brute-force enumeration utility')
	parser.add_argument('-u', '--url', help='URL to look up', required=True)
	parser.add_argument('-w', '--wordlist', help='directory listing', required=True)
	parser.add_argument('-o', '--outfile', help='File to write found directories')
	parser.add_argument('-v', '--verbose', help='Prints results to the screen. By Default verbose is off', action='store_true')

	# Assigning args
	args = parser.parse_args()
	outfile = 0
	if args.outfile:
		outfile = open(args.outfile, 'w')
	url = args.url
	valid_url = url_checker(url)
	verbose = args.verbose
	directories = open(args.wordlist, 'r')

	#limits the amount of concurrent open sockets to the server you can change the 1000
	sem = asyncio.Semaphore(1000)

	# Assigning loop and connection
	loop = asyncio.get_event_loop()
	loop.add_signal_handler(signal.SIGINT, signal_handler)

	#Do the things
	print ('[->] Checking base url: ',valid_url)
	f = asyncio.wait([get_status(valid_url + directory.rstrip('\n'), verbose, outfile, sem) for directory in directories])
	try:
		loop.run_until_complete(f)
	except asyncio.CancelledError:
		print('Tasks were canceled')

	print('[+] pyDirBuster completed successfully. Happy Hunting.')

if __name__ == '__main__':
	main()
