#! /usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################
# uart_power_bank
#  Python interface for a power bank via sertial/uart
########################

#imports
import os, sys
import time, datetime
import random
import string
import serial

#constants


#global variables


# usefull functions
def END(code = 1) :
    """Areter le programme"""
    sys.exit(code)

def ERROR(msg, code = 1):
    """Affiche un message d'erreur"""
    _len = len(str(msg))
    sys.stderr.write(str(msg) + "\n")
    END(code)

def WARNING(msg):
    """Affiche un message d'erreur"""
    sys.stderr.write(str(msg) + "\n")


# Objects
class TimerMilli(object):
    """
    Used for timing
    """
    def __init__(self, duration_s) :
        """
        Initiate the timer

        @param duration_s : Duration of the timer in seconds (float)

        """

        self._start_time = self.now()
        self.duration = duration_s

    def now(self):
        """
        Returns the curent time
        """

        return time.time()

    def hasExpired(self):
        """
        Returns True when the timer expired
        """
        _now = self.now()
        return ((self._start_time + self.duration) < _now)


class PBControler(object):
    """
    Instance of a power bank controler
    """

    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, port, baudrate = 38400, timeout = 1):
        """
        Default initiator
        """

        self.timeout = timeout
        self._operational = False

        try:
            self._tty = serial.Serial(port, baudrate)
            self._tty.timeout = self.timeout
            self._operational = True

            time.sleep(1)
            print(self.getWelcome())
        except serial.SerialException:
            ERROR("Connot open the serial port : %s" % (port))

        

    def _write_tty(self, text):
        """
        send a commande into the open serial port
        """
        # flush input
        self._tty.flushInput()
        self._tty.write(bytes(text + os.linesep, 'ascii'))

    def _read_tty(self, timeout):
        """
        send a commande into the open serial port
        """

        _timer = TimerMilli(timeout)

        _lines = []

        while (not _timer.hasExpired()) :
            time.sleep(0.1)
            _inWaiting = self._tty.inWaiting()
            _data = self._tty.read(_inWaiting)


            _line = ""

            try :
                _decoded = _data.decode()
            except :
                print(_data)
                _decoded = ""


            for _car in _decoded:
                if _car in (["\n", "\r"]):
                    if (0 < len(_line) ):
                        _lines.append(_line)
                    _line = ""
                else :
                    _line += _car

            if (0 < len(_line)) :
                _lines.append(_line)

            self._tty.flushInput()
            self._tty.flushOutput()

        return _lines

    def getWelcome(self):
        """
        read the welcom message
        """

        return self._read_tty(1)

    def getInfo(self):
        """
        Get the power bank general infiormations

        Returns the information in a dict
        """
        self._write_tty("INFO")

        _data = {}
        _lines = self._read_tty(1)

        # process data and extracy properties
        for _l in _lines :
            _splited = _l.strip().split(" ")

            for _d in  _splited:
                try :
                    _k, _v = _d.split("=")

                    if _k in ["VBAT", "VOUT", "VDC", "VIN", "IOUT", "TEMP"] :
                        _data[_k] =  float(_v)
                    elif _k in ["CHG", "WRN", "PWR"] :
                        _data[_k] =  ("1" == _v)
                    else :
                        ERROR("INFO Property unknown : %s" % (_k), 1)
                except :
                    ERROR("INFO Property unknown : %s" % (_d), 1)

        print("Rep to INFO")
        print (_data)

        return _data

    def _processTimeResp(self):
        """
        Process date time response

        returns time as datetime
        """

        _lines = self._read_tty(1)
        _dt = _dt = datetime.datetime(1900,1,1,0,0,0)  # default value

        if 1 == len(_lines) :
            print("Rep to TIME")

            _date = _lines[0]

            try :
                _dt = datetime.datetime.strptime(_date, PBControler.DATE_TIME_FORMAT)
            except ValueError:
                WARNING("Wrong date/time format : %s" % (_date))

            print(_date, _dt)
            
        else :
            WARNING("Bad response to commande TIME")

        return _dt

    def getTime(self):
        """
        Get the date/time from the power bank
        """
        self._write_tty("TIME")

        return self._processTimeResp()

        

    def setTime(self, date_time):
        """
        set the time
        """

        assert isinstance(date_time, datetime.datetime), 'setTime requires argument type datetime'

        _cmd = "TIME %s" %(date_time.strftime(PBControler.DATE_TIME_FORMAT))
        self._write_tty(_cmd)

        return self._processTimeResp()

    def _processOKNOKResp(self):
        """
        processes response for command with OK ERROR
        """

        _lines = self._read_tty(1)
        _rep = False

        if 1 == len(_lines) :
            

            _data = _lines[0]

            if "OK" == _data :
                _rep = True

            print(_data)
        else :
            WARNING("Bad response to commande PWR")

        return _rep

    def setPoweOff(self, delay):
        """
        Power off with with timer
        """

        assert isinstance(delay, int), 'setPoweOff requires argument type integer'
        # assert ((0 <= delay) and (delay < 1000)), 'setPowerOff delay should be in range 0, 9999'

        _cmd = "PWR %d" % delay

        self._write_tty(_cmd)
        print("Rep to " + _cmd)

        return self._processOKNOKResp()

    def resetPowerOff(self):
        """
        Reset Power off timer
        """

        _cmd = "PWR"

        self._write_tty(_cmd)
        print("Rep to " + _cmd)

        return self._processOKNOKResp()

    def setWDT(self, delay):
        """
        Power reset with timer
        """

        assert isinstance(delay, int), 'setPoweOff requires argument type integer'
        # assert ((0 <= delay) and (delay < 1000)), 'setPowerOff delay should be in range 0, 9999'

        _cmd = "RST %d" % delay

        self._write_tty(_cmd)
        print("Rep to " + _cmd)

        return self._processOKNOKResp()

    def resetWDT(self):
        """
        Reset power reset with timer
        """

        _cmd = "RST"

        self._write_tty(_cmd)
        print("Rep to " + _cmd)

        return self._processOKNOKResp()


# tests
def test(port):
    _pbc = PBControler(port)

    _tmpStr = ""

    while True :
        _pbc.getInfo()

        time.sleep(0.2)

        _pbc.getTime()

        time.sleep(0.2)

        _pbc.setTime(datetime.datetime.now())

        _rep = _pbc.resetPowerOff()
        assert True == _rep, "Erreur : " + str(_rep)

        _rep = _pbc.resetWDT()
        assert True == _rep, "Erreur : " + str(_rep)

        for _i in[0, 1, 2, 50, 999] :
            _rep = _pbc.setPoweOff(_i)
            assert True == _rep, "Erreur : " + str(_rep)

            _rep = _pbc.setWDT(_i)
            assert True == _rep, "Erreur : " + str(_rep)

        for _i in[1000, 1001, 1050, 3094, 44444444455] :
            _rep = _pbc.setPoweOff(_i)
            assert False == _rep, "Erreur : " + str(_rep)

            _rep = _pbc.setWDT(_i)
            assert False == _rep, "Erreur : " + str(_rep)



    while True :
        _pbc._write_tty(_tmpStr)
        

        _data = _pbc._read_tty()

        print("CMD : ", _tmpStr)
        print("Reponse : ", _data)


        _tmpStr += random.choice(string.ascii_uppercase + string.digits) 
        time.sleep(1)

#Les fonctions genriques
def usage() : # Cette fonction indique le mode d'emploi de ce script
    """Print usage instruction"""
    print("usage : %s tty_port" %( os.path.basename( sys.argv[0])))
    END(1)
    
#Entree principale du programme
def main() : # Cette fonction est appele lors du lancement du script
    """ Called when lunching the scrpt the main function""" 

    #Verfier les argument de la ligne de commande
    if len(sys.argv[1:] ) == 1 :
        _port = sys.argv[1]
        test(_port)
    else :    
        usage()

    



#main entry
if __name__ == "__main__" :
    main()
