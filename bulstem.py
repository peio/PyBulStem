#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
#  Implementation author: Peio Popov <peio@peio.org> 
#  Algorithm author: Preslav Nakov, nakov@cs.berkeley.edu, UC Berkeley
#  
#  Description: Stems a text file

import cPickle, re

### CONSTANTS
RULES_FILE = "rules/stem_rules_context_2_UTF-8.txt"
MIN_RULE_FREQ = 2
MIN_WORD_LEN = 3

re_bg_vowels = re.compile(u"[аъоуеияю]")

def fetchTheRules(RULES_FILE, MIN_RULE_FREQ):
	'Read the rules and load them into dictionary'
	import codecs

	re_empty_line = re.compile('^\s*$') 
	re_rule_line = re.compile(u"([а-я-]+) ==> ([a-я-]+) (\d+)", re.U)
	StemmingRules = {}

	for rule in codecs.open(RULES_FILE, 'r', 'utf-8').readlines():
		if re_empty_line.match(rule):
			continue
			
		'Break the rule line in three parts stem(1) - reduce(2) - probability(3)'
		rule_parts = re_rule_line.match(rule)
		
		if rule_parts != None:
			if rule_parts.group(3) > MIN_RULE_FREQ:
				'Build the dictionary'
				StemmingRules[rule_parts.group(1)] = rule_parts.group(2)
		else:
			print "Bad stemming rule:",rule.encode('utf-8')
			continue

	'Using a pickle would be faster'
	cPickle.dump(StemmingRules, open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'wb')) 

	return StemmingRules


def stem(word):
	'Stemm the word'

	'Do not stem short words'
	wordLen = len(word)
	if wordLen <= MIN_WORD_LEN:
		return word

	'If no bulgarian vowel - no valid word'
	if not re_bg_vowels.match(word):
		return word

	'Convert to lower case in order to compare it easy'
	word = word.lower()

	#c = 0
	c = MIN_WORD_LEN
	for _ in word:
		'Reduce the word from the begining towards the end'
		stem = word[c:wordLen]
		c +=1

		'Check if there is a stem matching the reminder of the word'
		if StemmingRules.has_key(stem):
			'Return stemmed word'
			return word[:c-1]+StemmingRules[stem]
			break
		else:
			continue

	'Always return something'		
	return word

'Try to reload the rules or build them from the text files'
try: StemmingRules = cPickle.load(open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'rb'))
except: StemmingRules = fetchTheRules(RULES_FILE, MIN_RULE_FREQ)


