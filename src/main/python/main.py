'''
Created on 1 April 2014
@author: don Najd
@description: Nao will be Sociable
'''
from __future__ import print_function

from naoutil import broker
import naoutil.naoenv as naoenv
import naoutil.memory as memory

from fluentnao.nao import Nao

#########################
# SETUP
######################### 

# Broker (must come first)
#naoIp = "nao.local"
naoIp = "192.168.2.15"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

# FluentNao
env = naoenv.make_environment(None)
log = lambda msg: print(msg) 				# lambda for loggin to the console
nao = Nao(env, log)

# init
nao.say('I think')
nao.wait(.5)
nao.say('therefore')
nao.wait(.5)
nao.say('I')
nao.wait(.1)
nao.say('am')