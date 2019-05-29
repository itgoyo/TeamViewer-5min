#!/usr/bin/env python 

#coding:utf-8
import sys
import os
import glob
import platform
import re
import random
import string

print('''
--------------------------------
TeamViewer ID Changer for MAC OS
--------------------------------
''')

if platform.system() != 'Darwin':
    print('This script can be run only on MAC OS.')
    sys.exit();

if os.geteuid() != 0:
    print('This script must be run form root.')
    sys.exit();

if os.environ.has_key('SUDO_USER'):
    USERNAME = os.environ['SUDO_USER']
    if USERNAME == 'root':
       print('Can not find user name. Run this script via sudo from regular user')
       sys.exit();
else:
    print('Can not find user name. Run this script via sudo from regular user')
    sys.exit();

HOMEDIRLIB = '/Users/' + USERNAME  + '/library/preferences/'
GLOBALLIB  =  '/library/preferences/'

CONFIGS = []

# Find config files

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

for file in listdir_fullpath(HOMEDIRLIB):
    if 'teamviewer'.lower() in file.lower():
        CONFIGS.append(file)

if not CONFIGS:
    print ('''
There is no TemViewer configs found.
Maybe you have deleted it manualy or never run TeamViewer after installation.
Nothing to delete.
''')
# Delete config files
else:
    print("Configs found:\n")
    for file in CONFIGS:
        print file

    print('''
This files will be DELETED permanently.
All TeamViewer settings will be lost
''')
    raw_input("Press Enter to continue or CTR+C to abort...")

    for file in CONFIGS:
        try:
            os.remove(file)
        except:
            print("Cannot delete config files. Permission denied?")
            sys.exit();
    print("Done.")

# Find binaryes

TMBINARYES = [
'/Applications/TeamViewer.app/Contents/MacOS/TeamViewer',
'/Applications/TeamViewer.app/Contents/MacOS/TeamViewer_Service',
'/Applications/TeamViewer.app/Contents/Helpers/TeamViewer_Desktop',
]

for file in TMBINARYES:
    if os.path.exists(file):
        pass
    else:
        print("File not found: " + file)
        print ("Install TeamViewer correctly")
        sys.exit();

# Patch files

def idpatch(fpath,platf,serial):
    file = open(fpath, 'r+b')
    binary = file.read()
    PlatformPattern = "IOPlatformExpert.{6}"
    SerialPattern =  "IOPlatformSerialNumber%s%s%sUUID"

    binary = re.sub(PlatformPattern, platf, binary)
    binary = re.sub(SerialPattern % (chr(0), "[0-9a-zA-Z]{8,8}", chr(0)), SerialPattern%(chr(0), serial, chr(0)), binary)

    file = open(fpath,'wb').write(binary)
    return True

def random_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

RANDOMSERIAL = random_generator()
RANDOMPLATFORM = "IOPlatformExpert" + random_generator(6)


for file in TMBINARYES:
        try:
            idpatch(file,RANDOMPLATFORM,RANDOMSERIAL)
        except:
            print "Error: can not patch file " + file
            print "Wrong version?"
            sys.exit();

print "PlatformDevice: " + RANDOMPLATFORM
print "PlatformSerial: " + RANDOMSERIAL

print('''
ID changed sucessfully.
!!! Restart computer before using TeamViewer !!!!
''')
