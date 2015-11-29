#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from socket import *

class Scanner(object):
    def __init__(self, timeout=5):
        super(Scanner, self).__init__()

        self.check     = '✓'
        self.times     = '×'
        self.important = '!'
        self.args      = sys.argv
        self.timeout = timeout

        self.colors = {
            'green': '\033[92m',
            'purple': '\033[95m',
            'orange': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'reset': '\033[0m',
            'underline': '\033[4m',
            'bold': '\033[1m'
        }

        if int(len(self.args)) == 1:
            return self.help()

        if int(len(self.args)) < 3:
            self.message('Faltam argumentos', 'error')
            return

        self.file  = self.args.pop(0)
        self.ip    = self.args.pop(-1)

        self.scan()


    def scan(self):
        try:
            self.valid_ip(self.ip)

            self.message('Iniciando escaneamento...', 'info', True, 'orange')
            
            if '-' in str(self.args):
                ports = self.args[0].split('-')

                for port in range(int(ports[0]), int(ports[1])):
                    try:
                        sock = socket(AF_INET, SOCK_STREAM)
                        sock.settimeout(self.timeout)
                        sock.connect((self.ip, int(port)))
                        sock.settimeout(None)
                        self.message('PORTA: %d - ABERTA' % int(port))
                    except timeout:
                        self.message('Timeout ao escanear a porta', 'error')
                        continue
                    except:
                        self.message('PORTA: %d - FECHADA' % int(port), 'error')
                        continue
            else:
                for port in self.args:
                    try:
                        sock = socket(AF_INET, SOCK_STREAM)
                        sock.settimeout(self.timeout)
                        sock.connect((self.ip, int(port)))
                        sock.settimeout(None)
                        self.message('PORTA: %d - ABERTA' % int(port))
                    except:
                        self.message('PORTA: %d - FECHADA' % int(port), 'error')
                        continue
        except Exception, e:
            raise e

    def valid_ip(self, ip):
        try:
            inet_aton(ip)
        except Exception, e:
            self.message('IP inválido, tente novamente.', 'error', True)
            raise e

    def message(self, message, type='success', important=False, color='blue'):
        if type == 'success':
            type = self.check
        elif type == 'error':
            type = self.times
            color = 'red'
        elif type == 'info':
            type = self.important

        message = '[%s] %s' % (type, message)

        if important:
            print '%s %s %s' % (self.colors[color], '=' * len(message), self.colors['reset'])
            print '%s %s %s' % (self.colors[color], message, self.colors['reset'])
            print '%s %s %s' % (self.colors[color], '=' * len(message), self.colors['reset'])
        else:
            print '%s %s %s' % (self.colors[color], message, self.colors['reset'])

    def help(self):
        print 'ajuda'


def main():
    scanner = Scanner()

if __name__ == '__main__':
    main()