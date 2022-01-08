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
from upbc.uart_power_bank import *

#constants


#global variables


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
