#!/usr/bin/env python

import MySQLdb, os

class mythRipSQL():
    
    def __init__(self):        

        userHomeDir = os.path.expanduser("~")
        mythtvFile = os.path.join( userHomeDir, '.mythtv', 'mysql.txt' )
        
        # dictionary we'll be stuffing settings in to
        self.mythtvFileSettings = {}

        for line in file(mythtvFile):
            
            # if not a comment, contains a key=value pair
            if line[0] != '#' and '=' in line:
                
                equalPos = line.find('=')

                self.mythtvFileSettings[ line[0:equalPos] ] = line[equalPos+1:].strip()

        print self.mythtvFileSettings

            
            
