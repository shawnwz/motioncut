#! /usr/bin/python
# -*- coding: utf-8 -*-

######################################
#gaopin read excel into import_images table
#coding licl
#20141201 
#beijing
######################################

import MySQLdb, sys, traceback, time, datetime, types

import GpLog, GpUtils

class GpConfig:
	######################### manual begin ###############
	####mysql db config
	host = '192.168.1.21'
	port = 3306
	user = 'root'
	pw   = '07ac211b992005eff804f71ce794b699'
	db   = 'gaopin_images'

	#####mongo config 
	serverUrl  = 'mongodb://192.168.1.21:27017'
	mongoUser  = 'gpImage'
	mongoPassw = '_gpImage'

	mongoAdminUser  = 'gaopin'
	mongoAdminPassw = 'gaopin@2014'


	desStorageId = '3'
	remark = '0619_1'
	status = '1'
	######################### manual end ###############

	#######const
	orgi_table = 'orgi_motions'
	imp_table  = 'import_images'

	#####config file name
	#impCfgFile = './col_i.cfg'
	orgiCfgFile = './test.cfg'
	########excel col name
	enKeyName = 'keyEnglish'
	cnKeyName = 'keyChinese'

	def __init__(self):
		pass

	def __del__(self):
		pass
