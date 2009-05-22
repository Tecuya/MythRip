#!/usr/bin/env python

import MySQLdb

class MythSQL():
    
    def __init__(self):        

        userHomeDir = os.path.expanduser("~")
        mythtvFile = os.path.join( userHomeDir, '.mythtv', 'mysql.txt' )
        
        # dictionary we'll be stuffing settings in to
        self.mythtvFileSettings = {}

        for line in file(mythtvFile):
            
            # if not a comment, contains a key=value pair
            if line[0] != '#' && '=' in line:
                
                equalPos = line.find('=')

                mythtvFileSettings[ line[0:equalPos] ] = line[equalPos:]

        print mythtvFileSettings

            
            
