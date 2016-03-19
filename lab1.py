#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib2  # the lib that handles the url stuff
import math
from collections import Counter
'''
clean_text fuction
'''
import unicodedata

total = 0.00000000000000000000
def clean_text(txt):
	txt = txt.lower()
	txt = txt.translate(None, "\"\'()[]{}?.!/;:,&%/$*^+-_1234567890@#")	
	return txt

def rm_pagebreak(dirty_txt):
	return dirty_txt.replace('\n', ' ').replace('\r', ' ')

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def rep_decor(decor_txt):
	decor_txt = unicode(decor_txt, errors='ignore')
	return unicodedata.normalize('NFKD', unicode(decor_txt)).encode('ASCII','ignore')
	

'''
frequencies of letters
'''
def getLetterCount(message):
	global letterCount
	global total
	letterCount = Counter(message)
	total = len(message)
	return letterCount
	'''global total
	global letterCount
	#to discard the numbers
	LETTERS = 'abcdefghijklmnopqrstuvwxyz '
	# Returns a dictionary with keys of single letters and values of the
	# count of how many times they appear in the message parameter.
	letterCount = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0, ' ': 0}
	for letter in message:
		# if is a letter and not a numbers
		if letter in LETTERS:
			letterCount[letter] += 1
			total += 1
	return letterCount'''
total_pair = 0

def get_pair_count(message):
	global total_pair
	listaux = {}
	for i in range(total-1):
		xy = message[i]
		xy += message[i+1]
		total_pair += 1
		if xy not in listaux:
			listaux[xy] = 1
		else:
			listaux[xy] += 1
	return listaux
'''
Random
'''

import random as rd
def rd_sample(X,k = 1):
    return rd.sample(X,k)

def rd_sample_XY(message):
	global total
	randpos = rd.randrange(0,total)
	xy = message[randpos]
	xy += message[randpos+1]
	return xy

'''
PRobability
'''
def prob_of(num_lett):
	global total
	return float(num_lett)/float(total)

def prob_of_pair(num_lett):
	global total_pair
	return float(num_lett)/float(total_pair)
'''
gentext
'''
random_txt=""
def gentext(message):
	global random_txt
	global letterCount
	aux = letterCount
	aux1 = total
	for i in range(total):
		letter = rd_sample(message)
		if aux[letter[0]] != 0:
			random_txt += letter[0]
			print aux[letter[0]]
			aux[letter[0]] -= 1
		else:
			total += 1


	return


'''
Entropy
'''
def log2( x ):
     return math.log( x ) / math.log( 2 )

def ent_h1(w):
	global letterCount
	prb = prob_of(letterCount[w])
	return prb*(log2(1/prb))

def entropy(W):
	global letterCount
	summatory = 0.0000000
	for n in letterCount:
		prb = prob_of(letterCount[n])
		summatory += prb*(log2(1/prb))
	return summatory

def join_entropy(W):
	summ = 0.000
	for n in W:
		prb = prob_of_pair(W[n])
		summ += prb*(log2(1/prb))
	return summ
'''
MAIN
'''

with open('22884-8.txt', 'rw') as myfiles:
    i = myfiles.read()	
    i = clean_text(i)
    i = rm_pagebreak(i)
    i = rep_decor(i)
    rdm = rd.choice(i)
    frq = getLetterCount(i)
    ent = entropy(i)
    f = ent_h1(rdm)
    dictionary_pair = get_pair_count(i)
    #gentext(i)    
    print total #Nuber of letters of a file.txt
    print ent #Entropy of this text
    print rdm #rdm letter of a text
    print f 
    print rd_sample_XY(i)    
    print join_entropy(dictionary_pair)




#data = urllib2.urlopen('http://www.gutenberg.org/cache/epub/22884/pg22884.txt') # it's a file like object and works just like a file
#for line in data: # files are iterable
#    print line
#*/