#!/usr/bin/python
#
#  File name:   sim.py
#  Author:      Melanie Tosik
#  Platform:    Ubuntu 13.04
#  Description: Lin Similarity

import sys
import math
from decimal import *
import operator

class LinSimilarity(object):
    """ Computes Lin similarity of a given input noun and all other nouns in a given input file """
    
    def __init__(self, conllfile):
        # Feature dictionary  {noun : set([features])}
        self.chart = {}
        # Set of unique nouns
        self.nouns = set()
        # Feature information dictionary {feature : I(fi)}
        self.inf = {}
        
        self.build_chart(conllfile)
        self.get_feature_information()

    def build_chart(self, conllfile):
        """ Creates a feature matrix out of the given input file in conll format """
        
        # Current sentence 
        sentence = []
        # STTS POS tags for nouns
        noun_tags = ['NN', 'NE']
        # STTS POS tags for verbs
        verb_tags = ['VAFIN', 'VAINF', 'VAIMP', 'VAPP', 'VMFIN', 'VMINF', 'VMPP', 'VVFIN', 'VVINF', 'VVIZU', 'VVIMP', 'VVPP']
        # Tags for edge labels
        edge_labels = ['OA', 'OA2', 'OC', 'OG', 'OP', 'SB', 'SBP']
    
        with open(conllfile, 'r') as f:
            for line in f:
                # Gets single sentences
                if line.strip():
                    sentence.append(line.split('\t'))
                else:
                    # Processes current sentence
                    for field_line in sentence:
                        # If word is noun and in argument position...
                        if field_line[4] in noun_tags and field_line[10] in edge_labels:
                            # stores word, dependency relation and projective head
                            noun = field_line[2]
                            label = field_line[10]
                            head = int(field_line[8])
                            # determines head in corresponding line
                            head_field_line = sentence[head-1]
                            # If head is verb...
                            if head_field_line[4] in verb_tags:
                                # stores verb lemma
                                verb = head_field_line[2]
                                # Creates new dictionary entry if necessary
                                if noun not in self.chart:
                                    self.chart[noun] = set()
                                # adds features
                                self.chart[noun].add((label,verb))
                            else:
                                continue
                        # Counts nouns for later computation       
                        if field_line[4] in noun_tags:
                            self.nouns.add(field_line[2])
                    sentence = []
        
    def get_feature_information(self):
        """ Computes I(f) for every feature in chart """
        
        noun_cnt = len(self.nouns)
        # Gets feature frequencies
        for noun, feature_set in self.chart.iteritems():
            for feature in feature_set:
                if not feature in self.inf.keys():
                    self.inf[feature] = 1
                else:
                    self.inf[feature] += 1
        # Computes feature information I(f)            
        for feature, count in self.inf.iteritems():
            getcontext().prec = 20
            self.inf[feature] = -(math.log10((Decimal(count)/Decimal(noun_cnt))))
    
    def sim(self, word):
        """ Computes most similar words for an input word """
        
        # Set of features of the given word
        word_feature_set = set()
        # Set of feature information
        word_feature_inf_set = set()
        # Set of similar words
        sim_word_set = set()
        # Set of feature information of current similar word
        sim_word_inf = set()
        # Dictionary of similar words and similarity {word : sim}
        sim_dict = {}
        # Input word
        word = sys.argv[2]
        
        # If word was seen in given input file...
        if word in self.chart.keys():
            
            # gets features and feature information of given word
            for feature in self.chart[word]:
                word_feature_set.add(feature)
                word_feature_inf_set.add(self.inf[feature])
            
            # gets similar words
            for word in self.chart:
                if set.intersection(word_feature_set, self.chart[word]):
                    sim_word_set.add(word)
            
            # gets feature information of similar words        
            for word in sim_word_set:
                for feature in self.chart[word]:
                    sim_word_inf.add(self.inf[feature])
                
                # computes similarity 
                num = 2*(sum(set.intersection(word_feature_inf_set, sim_word_inf)))
                den = sum(list(word_feature_inf_set)+list(sim_word_inf))
                sim = num / den
                
                # stores similar words and similarity in sorted dictionary
                sim_dict[word] = sim
                sim_word_inf = set()
                sorted_sim_dict = sorted(sim_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
            
            # prints 50 most similar words in descending order of their similarity
            for tupel in sorted_sim_dict[1:51]:
                print tupel[0]
            ### Enable to print words with similarity to the given input word greater than 0.04
            #for tupel in sorted_sim_dict:
                #if Decimal(tupel[1]) >= 0.04:
                    #print tupel[0]
        else:
            print 'Word not in database. Please check spelling or try another one.'

if __name__ == '__main__':
    if len(sys.argv) == 3:
        lin = LinSimilarity(sys.argv[1])
        lin.sim(sys.argv[2])
    else:
        print 'Usage: python sim.py <file> <word>'
    
    
            
    
