# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:39:22 2020

@author: gebruiker
"""
from numpy import mean
import matplotlib.pyplot as plt

"""
Class for FastQ entries. So I don't to make everything harder by using multiple lists.
"""
class FastQ_entry():
    
    def __init__(self, header, seq, score):
        self.header = header.strip()
        self.sequence = seq.strip()
        self.score = score
        
        
    def __str__(self):
        return "{}\n{}\n{}".format(self.header, self.sequence, self.score)
    
    
    def get_header(self):
        return self.header
    
    def get_sequence(self):
        return self.sequence
    
    def get_score(self):
        return self.score
    
    

def main():
    filename = "D:/School/Minor_2020/PythonFastQ/watisdit.txt"
    """
    5) Filter het bestand op basis van een Phred Score (Threshold >9, of hoger).
    Set to 0 to allow all scores.
    """
    threshold = 0
    FastQ_entries = file_parser(filename, threshold)
    
    """ 
    2) Retourneer een sequentie op basis van een sequentie ID. 
    """
    print("\nReturn a sequence based on header:")
    header = "@10031000100220645" # index 50 of list of objects
    filtered = filter(lambda FastQ_entry: FastQ_entry.header == header, FastQ_entries)
    print(next(filtered))
    
    
    """
    4) Retourneer de sequentie met hoogste / laagste Phred Score.
    """
    max_score = max(FastQ_entries, key=lambda FastQ_entry: FastQ_entry.score)
    min_score = min(FastQ_entries, key=lambda FastQ_entry: FastQ_entry.score)
    print("\nMax:\n{} @ {}".format(max_score.sequence, max_score.score))
    print("Min:\n{} @ {}".format(min_score.sequence, min_score.score))
    
    
    
    """
    6) Sorteer het bestand op basis van Phred Score.
    """
    print("\nSorted based on score:")
    print("First index's score before sorting:", FastQ_entries[0].get_score())
    FastQ_entries.sort(key=lambda FastQ_entry: FastQ_entry.get_score(), reverse=True)
    print("First index's score after sorting:",FastQ_entries[0].get_score())
    
    
    """
    7) Plot de distributie van alle gevonden Phred Scores in een histogram.
    """
    
    scores = [fastq_object.get_score() for fastq_object in FastQ_entries]
    make_histogram(scores)
    
    


"""
Parses the file and puts entries in a list of objects.
"""
def file_parser(filename, threshold):
    
    with open(filename) as file:
        FastQ_entries = []
        for index, header in enumerate(file):
            seq = file.readline()
            plus = file.readline()
            score = calc_avg_score(file.readline())
            if score >= threshold: # Filtering based on a certain threshold
                FastQ_entries.append(FastQ_entry(header, seq, score))
                
            if index >= 2000*4:
                break
        
    return FastQ_entries



"""
3) Bereken de Phred score voor iedere Read (gebruik het gemiddelde in alle vragen). 
Phred score is de ascii score.
"""
def calc_avg_score(fastq_line):
    score = mean([ord(char)-64 for char in fastq_line])
    return score



"""
Makes a histgram based on the phred scores
"""
def make_histogram(scores):
    
    plt.hist(scores)
    plt.title("Distribution of Phred scores")
    



if __name__ == "__main__":
    main()