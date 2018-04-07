# !/usr/bin/env python
# coding=utf-8

#
# Helps generating a .csv Anki flashcard import file of the forms of [some] German irregular verbs
# (specified below), plus a translation into lang (ru by default).
#

import urllib2
import time
import random
import re
from bs4 import BeautifulSoup

words = [ \
 u'dürften', \
 u'denken', \
 u'haben', \
 u'kennen', \
 u'nennen', \
 u'rennen', \
 u'senden', \
 u'stehen', \
 u'tun', \
 u'wenden', \
 u'bitten', \
 u'essen', \
 u'bringen' , \
 u'fressen', \
 u'geben', \
 u'geschehen', \
 u'lesen', \
 u'liegen', \
 u'messen', \
 u'sehen', \
 u'sein', \
 u'sitzen', \
 u'treten', \
 u'vergessen', \
 u'befehlen', \
 u'beginnen', \
 u'brechen', \
 u'empfehlen', \
 u'erschrecken', \
 u'gelten', \
 u'gewinnen', \
 u'helfen', \
 u'kommen', \
 u'nehmen', \
 u'schwimmen', \
 u'sprechen', \
 u'stechen', \
 u'stehlen', \
 u'sterben', \
 u'treffen', \
 u'verderben', \
 u'werben', \
 u'werfen', \
 u'binden', \
 u'eindringen', \
 u'empfinden', \
 u'finden', \
 u'gelingen', \
 u'klingen', \
 u'singen', \
 u'sinken', \
 u'springen', \
 u'stinken', \
 u'trinken', \
 u'verschwinden', \
 u'zwingen', \
 u'blasen', \
 u'braten', \
 u'empfangen', \
 u'fallen', \
 u'fangen', \
 u'gehen', \
 u'geraten', \
 u'halten', \
 u'hängen', \
 u'lassen', \
 u'laufen', \
 u'raten', \
 u'schlafen', \
 u'heißen', \
 u'beißen', \
 u'bleiben', \
 u'gleichen', \
 u'gleiten', \
 u'greifen', \
 u'leiden', \
 u'leihen', \
 u'meiden', \
 u'pfeifen', \
 u'reiben', \
 u'reißen', \
 u'reiten', \
 u'scheinen', \
 u'schleichen', \
 u'schmeißen', \
 u'schneiden', \
 u'schreiben', \
 u'schreien', \
 u'schweigen', \
 u'steigen', \
 u'streichen', \
 u'streiten', \
 u'treiben', \
 u'verzeihen', \
 u'weichen', \
 u'weisen', \
 u'stoßen', \
 u'rufen', \
 u'betrügen', \
 u'bewegen', \
 u'biegen', \
 u'bieten', \
 u'erlöschen', \
 u'erwägen', \
 u'fliegen', \
 u'fliehen', \
 u'fließen', \
 u'frieren', \
 u'genießen', \
 u'gießen', \
 u'heben', \
 u'können', \
 u'kriechen', \
 u'lügen', \
 u'mögen', \
 u'riechen', \
 u'schieben', \
 u'schießen', \
 u'schließen', \
 u'schmelzen', \
 u'schwellen', \
 u'schwören', \
 u'verlieren', \
 u'wiegen', \
 u'ziehen', \
 u'backen', \
 u'fahren', \
 u'graben', \
 u'laden', \
 u'schaffen', \
 u'schlagen', \
 u'tragen', \
 u'wachsen', \
 u'waschen', \
 u'werden', \
 u'müssen', \
 u'wissen'
]

lang = 'ru'

csv_separator = u';'
translations_separator = u', '

warnings = []

for word in words:
	warning = False

	# look less like a robot (introduce 0..2 sec random page reload delay), in order to not to get banned by the web server
	time.sleep(4 * random.random())

	backoff = 2
	while True:
		try:
			response = urllib2.urlopen('https://de.thefreedictionary.com/' + urllib2.quote(word.encode('utf8')))
			break
		except urllib2.HTTPError as e:
			to = int(random.random() * backoff)
			# print("Oops! %s, Try again in %d sec ..." % (str(e), to))
			time.sleep(to)
			backoff = backoff * 2

	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	forms_section = soup.find(id='Definition').find('section', {'data-src': 'pons'}).encode('utf8')

	# there might be multiple entries of verb form lists, tokenize them
	forms_lists = re.findall(r'&lt;(?:<b>[^<]+</b>(?:,\s*)?){3,4}&gt;', forms_section)

	if len(forms_lists) < 2:
		warning = True
	else:
		if len(forms_lists) == 2 and forms_lists[0] != forms_lists[1]:
			warning = True
		else:
			forms_lists = [unicode(s, "utf-8") for s in re.findall('<b>(.*?)</b>', forms_lists[0])]

			if len(forms_lists) == 4 and \
				forms_lists[2].startswith('hat ') and \
				forms_lists[3].startswith('ist ') and \
				forms_lists[2][4:] == forms_lists[3][4:]:
				forms_lists[2] = 'hat/ist ' + forms_lists[2][4:]
				forms_lists = forms_lists[:-1]

			forms_lists = forms_lists[1:]

	if warning:
		forms_lists = [unicode(' ??? '.join(re.findall('<b>(.*?)</b>', s)), "utf-8") for s in forms_lists]
		forms_lists = [ ' --- ' ] + forms_lists + [ ' --- ' ]

	forms = [ word ] + forms_lists

	t_list = soup.select('#translbody > * > span[lang=%s] > a' % lang)
	translations = [u''.join(elem.get_text()) for elem in t_list]

	if (len(translations) < 1):
		warning = True
		translations = [ u'???' ]

	# Indikativ Praesens forms

	# ipf_list = soup.select('#VerbTableN1_1 > * > td')
	ip_forms = [] # [u''.join(ipf.get_text()) for ipf in ipf_list ]

	# if (len(ip_forms) != 6):
	# 	if (len(ip_forms) == 0):
	# 		ip_forms = ['' for i in range(6)]
	# 	else:
	# 		warning = True

	# digest

	line = csv_separator.join(forms + [ translations_separator.join(translations) ] + ip_forms + [ '' ])

	if warning:
		warnings.append(line)
		print ''
	else:
		print line

if len(warnings) > 0:
	print ''
	print ' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	print ' ! PLEASE CHECK AND ADD MANUALLY: !'
	print ' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	print ''
	for line in warnings:
		print line