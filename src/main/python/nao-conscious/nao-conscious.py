'''
Created on 1 April 2014
@author: Don Najd
@description: Nao will be Sociable
'''
# python
from __future__ import print_function

# SIGINT
import signal
import sys

# naoutil & fluentnao
from naoutil import broker
import naoutil.naoenv as naoenv
import naoutil.memory as memory
from fluentnao.nao import Nao
import expressions.anim as anim

# subscribers
from subscribers.laugh_subscriber import LaughSubscriber
from subscribers.sleepy_subscriber import SleepySubscriber
from subscribers.look_around_subscriber import LookAroundSubscriber
from subscribers.greeting_subscriber import GreetingSubscriber
from subscribers.star_trek_subscriber import StarTrekSubscriber
from subscribers.voice_movement_subscriber import VoiceMovementSubscriber
from subscribers.sensitive_subscriber import SensitiveSubscriber

# providers
from providers.touch_provider import TouchProvider
from providers.time_provider import TimeProvider
from providers.face_recog_provider import FaceRecogProvider
from providers.voice_recog_provider import VoiceRecogProvider
from providers.voice_emotion_provider import VoiceEmotionProvider


#########################
# SETUP: Broker

naoIp = "nao.local"
broker.Broker('bootstrapBroker', naoIp=naoIp, naoPort=9559)

#########################
# SETUP: FluentNao

env = naoenv.make_environment(None)
log = lambda msg: print(msg) 				# lambda for loggin to the console
n = Nao(env, log)

# disable autonomous moves
n.env.add_proxy("ALAutonomousMoves")
autonomous_moves = n.env.proxies["ALAutonomousMoves"] 
autonomous_moves.setExpressiveListeningEnabled(False)


#########################
# SETUP: Nao Consious

# subscribers
laugh_subscriber = LaughSubscriber(n)
sleepy_subscriber = SleepySubscriber(n)
look_around_subscriber = LookAroundSubscriber(n)
greeting_subscriber = GreetingSubscriber(n)
star_trek_subscriber = StarTrekSubscriber(n)
voice_movement_subscriber = VoiceMovementSubscriber(n)

# providers
time_provider = TimeProvider(n)
touch_provider = TouchProvider(n, memory, 'FrontTactilTouched')
face_recog_provider = FaceRecogProvider(n, memory)
voice_recog_provider = VoiceRecogProvider(n, memory)

# sensors
# RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
# MiddleTactilTouched, RearTactilTouched, HandRightBackTouched, HandRightLeftTouched



#########################
# HELPER: tear down
def tear_down():
	n.sit_say('Rest_1', 'Deactivate')

	# teardown
	touch_provider.tear_down()	
	time_provider.tear_down()
	face_recog_provider.tear_down()
	voice_recog_provider.tear_down()
	memory.unsubscribeToEvent('RearTactilTouched')  

# sigint
def tear_down_signal_handler(signal, frame):
    tear_down()
    sys.exit(0)

signal.signal(signal.SIGINT, tear_down_signal_handler)
	
# tactil
def tear_down_tactil_handler(dataName, value, message):
	if value==1:
		tear_down()

memory.subscribeToEvent('RearTactilTouched', tear_down_tactil_handler)



#########################
# HELPER: Example Nao Conscious
def setup():
	
	# time: sleepy & look around
	time_provider.add_subscriber(sleepy_subscriber)
	time_provider.add_subscriber(look_around_subscriber)
	time_provider.setup()

	# tactile: laugh
	touch_provider.add_subscriber(laugh_subscriber)
	touch_provider.setup()

	# face recog
	face_recog_provider.add_subscriber(greeting_subscriber)
	face_recog_provider.setup()

	# voice recog
	voice_recog_provider.add_subscriber(star_trek_subscriber)
	voice_recog_provider.add_subscriber(voice_movement_subscriber)
	voice_recog_provider.setup()

# trigger setup
setup()

# sensors
# RightBumperPressed, LeftBumperPressed, ChestButtonPressed, FrontTactilTouched
# MiddleTactilTouched, RearTactilTouched, HandRightBackTouched, HandRightLeftTouched

	
# tactil
def right_bumper_handler(dataName, value, message):
	if value==1:
		n.say('that is my right foot')

def left_bumper_handler(dataName, value, message):
	if value==1:
		n.say('that is my left foot')

memory.subscribeToEvent('RightBumperPressed', right_bumper_handler)
memory.subscribeToEvent('LeftBumperPressed', left_bumper_handler)