#!/usr/bin/python

# Simple Python methods for opening and closing GPIO pins on the
# Raspberry Pi

import time

def blink(pin, duration ):
    pinOpen(pin)
    time.sleep(duration)
    pinClose(pin)

def pinOpen(pin ):
    _make_available(pin)

    #Export pin number
    f= open ('/sys/class/gpio/export','w')
    f.write(str(pin))
    f.close()

    #Define Pin Direction as Output for LED
    path = '/sys/class/gpio/gpio' + str(pin) + '/direction'
    f= open (path,'w')
    f.write('out')
    f.close()

    path = '/sys/class/gpio/gpio' + str(pin) + '/value'
    f= open (path,'w')
    f.write('1')
    f.close()

def pinClose(pin ):
    path = '/sys/class/gpio/gpio' + str(pin) + '/value'
    f= open(path,'w')
    f.write('0')
    f.close()

def _make_available(pin ):
    try:
        f= open ('/sys/class/gpio/unexport','w')
        f.write(str(pin))
        f.close()
    except IOError as e:
        lol=0

def exit(pin):
    f= open ('/sys/class/gpio/unexport','w')
    f.write(str(gpio))
    f.close()

