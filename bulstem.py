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

def fetchTheRules(RULES_FILE, MIN_RULE_FREQ):
	'Read the rules and load them into dictionary'
	import codecs

	re_empty_line = re.compile('^\s*$')
	re_rule_line = re.compile(u"([а-я-]+) ==> ([a-я-]+) (\d+)", re.U)
	StemmingRules = {}

	for rule in codecs.open(RULES_FILE, 'r', 'utf-8').readlines():
		if re_empty_line.match(rule):
			continue
			
		rule_parts = re_rule_line.match(rule)
		
		if rule_parts != None:
			if rule_parts.group(3) > MIN_RULE_FREQ:
				StemmingRules[rule_parts.group(1)] = rule_parts.group(2)
		else:
			print "Bad stemming rule:",rule.encode('utf-8')
			continue

	cPickle.dump(StemmingRules, open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'wb')) 

	return StemmingRules


def stem(word):

	re_bg_vowels = re.compile(u"[аъоуеияю]")

	wordLen = len(word)

	if wordLen <= MIN_WORD_LEN:
		return word

	if not re_bg_vowels.match(word):
		return word

	c = 0
	for _ in word:
		stem = word[c:wordLen]
		c +=1

		if StemmingRules.has_key(stem):
			return word[:c-1]+StemmingRules[stem]
			break
		else:
			continue

	return word


try: StemmingRules = cPickle.load(open('rules/StemmingRules-MinFreq-'+str(MIN_RULE_FREQ)+'.pickle', 'rb'))
except: StemmingRules = fetchTheRules(RULES_FILE, MIN_RULE_FREQ)


