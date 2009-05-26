#!/usr/bin/python

"""
Provides a class giving access to the MythTV database.
"""
import os
import sys
import shlex
import code
import getopt
from datetime import datetime

from MythLog import *

# create logging object
log = MythLog(DEBUG, '%(asctime)s - %(levelname)s - DB - %(message)s', 'MythTV')

# check for dependency
try:
	import MySQLdb
except:
	log.Msg(CRITICAL, "MySQLdb (python-mysqldb) is required but is not found.")
	sys.exit(1)

class MythDB:
	"""
	A connection to the mythtv database.
	"""
	def __init__(self, args=None):
		# Setup connection variables
		dbconn = {
				'host' : None,
				'name' : None,
				'user' : None,
				'pass' : None
				}

		# Try to read the mysql.txt file used by MythTV.
		# Order taken from libs/libmyth/mythcontext.cpp
		config_files = [
				'/usr/local/share/mythtv/mysql.txt',
				'/usr/share/mythtv/mysql.txt',
				'/usr/local/etc/mythtv/mysql.txt',
				'/etc/mythtv/mysql.txt',
				os.path.expanduser('~/.mythtv/mysql.txt'),
				]

		if 'MYTHCONFDIR' in os.environ:
			config_locations.append('%s/mysql.txt' % os.environ['MYTHCONFDIR'])

		found_config = False
		for config_file in config_files:

			dbconn['host'] = None
			dbconn['name'] = None
			dbconn['user'] = None
			dbconn['pass'] = None
			
			if not os.access(config_file, os.R_OK): 
				continue

			for line in file(config_file):
				
				if line[0] != '#' and '=' in line:
					equalPos = line.find('=')
					
					key = line[0:equalPos]
					val = line[equalPos+1:].strip()

					if key == "DBHostName":
						dbconn['host'] = val
					elif key == "DBName":
						dbconn['name'] = val
					elif key == "DBUserName":
						dbconn['user'] = val
					elif key == "DBPassword":
						dbconn['pass'] = val

			if dbconn['host'] != None or dbconn['name'] != None or dbconn['user'] != None or dbconn['pass'] != None:
				log.Msg(INFO, 'Using config %s', config_file)
				found_config = True
				break

		# Overrides from command line parameters
		try:
			opts, args = getopt.getopt(args, '', ['dbhost=', 'user=', 'pass=', 'database='])
			for o, a in opts:
				if o == '--dbhost':
					dbconn['host'] = a
				if o == '--user':
					dbconn['user'] = a
				if o == '--pass':
					dbconn['pass'] = a
				if o == '--database':
					dbconn['name'] = a
		except:
			pass

		if not dbconn['host'] and not found_config:
			raise MythError('Unable to find MythTV configuration file')

		try:
			self.db = MySQLdb.connect(user=dbconn['user'], host=dbconn['host'], passwd=dbconn['pass'], db=dbconn['name'])
			log.Msg(INFO, 'DB Connection info (host:%s, name:%s, user:%s, pass:%s)', dbconn['host'], dbconn['name'], dbconn['user'], dbconn['pass'])
		except:
			raise MythError('Connection failed for \'%s\'@\'%s\' to database %s using password %s' % (dbconn['user'], dbconn['host'], dbconn['name'], dbconn['pass']))

	def getAllSettings(self, hostname=None):
		"""
		Returns values for all settings.

		Returns None if there are no settings. If multiple rows are
		found (multiple hostnames), returns the value of the first one.
		"""
		log.Msg(DEBUG, 'Retrieving all setting for host %s', hostname)
		c = self.db.cursor()
		if hostname is None:
			c.execute("""
					SELECT value, data
					FROM settings
					WHERE hostname IS NULL""")
		else:
			c.execute("""
					SELECT value, data
					FROM settings
					WHERE hostname LIKE('%s%%')""" %
					(hostname))
		rows = c.fetchall()
		c.close()

		if rows:
			return rows
		else:
			return None

	def getSetting(self, value, hostname=None):
		"""
		Returns the value for the given MythTV setting.

		Returns None if the setting was not found. If multiple rows are
		found (multiple hostnames), returns the value of the first one.
		"""
		log.Msg(DEBUG, 'Looking for setting %s for host %s', value, hostname)
		c = self.db.cursor()
		if hostname is None:
			c.execute("""
					SELECT data
					FROM settings
					WHERE value LIKE('%s') AND hostname IS NULL LIMIT 1""" %
					(value))
		else:
			c.execute("""
					SELECT data
					FROM settings
					WHERE value LIKE('%s') AND hostname LIKE('%s%%') LIMIT 1""" %
					(value, hostname))
		row = c.fetchone()
		c.close()

		if row:
			return row[0]
		else:
			return None

	def cursor(self):
		return self.db.cursor()

if __name__ == '__main__':
	banner = "'mdb' is a MythDB instance."
	try:
		import readline, rlcompleter
	except:
		pass
	else:
		readline.parse_and_bind("tab: complete")
		banner = banner + " TAB completion is available."
	mdb = MythDB(sys.argv[1:])
	namespace = globals().copy()
	namespace.update(locals())
	code.InteractiveConsole(namespace).interact(banner)

# vim: ts=4 sw=4:
