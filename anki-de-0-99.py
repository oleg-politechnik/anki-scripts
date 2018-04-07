# !/usr/bin/env python
# coding=utf-8

'''

Generates a .csv Anki flashcard import file of German numbers 0-99 plus a set of mp3s

prerequisites: "say" -- TTS (text-to-speech) utility, available on Mac OS
               "lame" -- mp3 encoding utility, cross-platform
               Media import Anki plugin (for batch audio Anki import):
               		Tools / Add-ons / Browse & Install
               			Code: 1531997860
               		Restart Anki

Simply putting audio files in Anki's .media folder is not enough, they need to be "imported",
so that the new flashcards can reference them. In order to do that semi-automagically, a set of
simple "dummy" flashcards is created using "Media import Anki plugin", so that audio files get
referenced.

	Tools -> Media Import...
    	Select the "media/"" folder
    	(For at least Anki v2.0.48 the deck selected for audio flashcards doesn't matter --
    	 they always end up in 'Default' deck)
    After a successful creation of the audio files, the "dummy" flashcards can be deleted.

'''

import os
import errno
import subprocess

tmp_dir = 'tmp'
media_dir = 'media'

def num2str_de(num):
	digits = [ None, u'ein', u'zwei', u'drei', u'vier', u'fünf', u'sechs', u'sieben', u'acht', u'neun']
	tens = [ None, u'zehn', u'zwanzig', u'dreißig', u'vierzig', u'fünfzig', u'sechzig', u'siebzig', u'achtzig', u'neunzig']

	if num < 0 or num >= 100: 
		return None

	string = ''

	if num == 0:
		string = u'null'
	elif num == 1:
		string = u'eins'
	elif num == 11:
		string = u'elf'
	elif num == 12:
		string = u'zwölf'
	elif num == 16:
		string = u'sechzehn'
	elif num == 17:
		string = u'siebzehn'
	else:

		t = int(num / 10)
		d = int(num % 10)

		if d > 0:
			string = digits[d]

		if t > 0:
			if d > 0 and t != 1:
				string = string + u'und'
			string = string + tens[t]

	return string.capitalize()

def safe_mkdir(path):
	try:
		os.mkdir(path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise


safe_mkdir(tmp_dir)
safe_mkdir(media_dir)

for number in range(0,100):
	aiff_fname = os.path.join(tmp_dir, '%d.aiff' % number)
	mp3_fname = os.path.join(media_dir, '%d.mp3' % number)

	with open(os.devnull, 'w')  as FNULL:
		subprocess.check_call([ 'say', '-v', 'Anna', str(number), '-o', aiff_fname ], stdout=FNULL, stderr=FNULL)
		subprocess.check_call([ 'lame', aiff_fname, mp3_fname ], stdout=FNULL, stderr=FNULL)
		print ';'.join([str(number), '[sound:%d.mp3]' % number, num2str_de(number)])
