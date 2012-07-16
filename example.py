#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# PyBulStem example usage

from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize
from bulstem import stem

text = u""" "Името на Мирослава Тодорова ми стана известно, когато към мен се обърнаха жертвите на престъпността", заяви по повод дисциплинарното уволнение на съдията вицепремиерът и министър на вътрешните работи Цветан Цветанов. В сутрешния блок на БНТ Цветанов наблегна на проблемите в съдебната система, като започна разговора с думите "ВСС е независима съдебна институция, която не бих искал да коментирам" """ 



for word in wordpunct_tokenize(text):
	print stem(word).encode('utf-8'),
	# print word.encode('utf-8'),
