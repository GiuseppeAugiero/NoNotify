#!/usr/bin/env python
# NoNotify.py - version 1.1
# Thanks to Sherpya

import telnetlib
import time
import sys

#DEBUG = False
DEBUG = True

def getCSMP(tn):
    while 1:
        tn.write('AT+CSMP?\r\n')
        result = tn.read_until('+CSMP: ', 1)
        if result.startswith('+CSMP:'):
            break

    result = tn.read_eager()
    return result.split('\r', 1)[0]

def setCSMP(tn):
    print 'Setto CSMP'
    tn.write('AT+CSMP=17,255,0,0\r\n')

def process(tn, no):
    print 'Processo modulo %d' % no
    tn.write('module%d\r\n' % no)
    tn.read_until('module %d.', no)
    while 1:
        csmp = getCSMP(tn)
        print 'Letto CSMP: %s' % csmp
        if not csmp.startswith('49'):
            break
        setCSMP(tn)

def connect(host):
    tn = telnetlib.Telnet(host)
    if DEBUG:
        tn.set_debuglevel(255)
    tn.read_until('username:')
    tn.write('USERNAMEPORTECH\r\n')
    tn.read_until('password:')
    tn.write('PASSWORDPORTECH\r\n')
    tn.read_until('module2.')
    return tn

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Utilizzo: %s host modulo' % sys.argv[0]
        sys.exit(1)

    tn = connect(sys.argv[1])
    process(tn, int(sys.argv[2]))
    tn.close()
