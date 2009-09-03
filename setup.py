#!/usr/bin/env python
  
# nab our smrt version
import sys, os, glob
from distutils.core import setup

mythtvfiles = glob.glob('mythtv/*py')

setup ( name="Mythrip",
        version = '0.9.0',
        license = "GPLv2",
        author = "Sean McLean",
        author_email = "smclean_no@spam_gmail.com",
        url = "http://mythrip.longstair.com",
        description = "wxWidgets GUI to encode reportings from MythTV",
        long_description = "MythRip is a wxWidgets GUI to encode reportings from MythTV, licensed under the GPLv2",
        data_files = [ ('/usr/bin/', ['mythrip'] ),
                       ('/usr/share/mythrip/mythtv', mythtvfiles )
		     ],
	
      )

