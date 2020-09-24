# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 11:39:22 2020

@author: Thijs Weenink

Systeem:
    Processor:	Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz, 2808 Mhz, 4 Core(s), 8 Logical Processor(s) | 3.6 Ghz volgens taakbeheer.
    RAM: 16GB, waarvan rond de 10GB beschikbaar om dit uit te voeren.
     
"""
from numpy import mean
import matplotlib.pyplot as plt

import time

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
    
    Context:
        1.
        Aangezien ik de gemiddelde scores direct bereken, voordat ik de data verder
        verwerk, is er maar 1 variabel nodig en een if-statement in de for-loop
        die door het bestand gaat.
        
        2.
        Technieken:
            - if-statement
            - x >= y
            
        3.
        Zie regel 7
        
        4.
        Hiervoor een time.time()/time.time_ns() aanmaken is wat overbodig.
        
        5.
        Een if-statement maakt code altijd langzamer dan wanneer het niet wordt gebruikt,
        maar het valt niet te vergelijken met elkaar.
        
        6.
        Als er waarden onder de threshold in de data staan, dan is er wat fout.
        
        7.
        Zo'n simpel if-statement is niet te versnellen.           
    """
    # Set to 0 to allow all scores.
    threshold = 0
    FastQ_entries = file_parser(filename, threshold)
    
    """ 
    2) Retourneer een sequentie op basis van een sequentie ID. 
    
    Context:
        1. 'Het is vast wel mogelijk om een specifiek object terug te krijgen 
        op basis van een sequentie'
        
        2.
        Technieken:
            - Objecten
            - lambda
            - filter()
            
        3.
        Zie regel 7
        
        4.
        Met 20.000 entries is het opzoeken nog steeds 0 nano seconds.
        
        5.
        Het is mij niet helemaal bekend hoe dit precies werkt, dit is de eerste keer
        dat ik dit gebruik. Het is een build-in python methode, wat vaak de snelste methode is.
        
        6.
        De gekozen header komt origineel uit de data zelf. Deze moet er dus in zitten.
        
        7.
        Ik zie geen mogelijkheden om dit te versnellen.
    """
    print("\nReturn a sequence based on header:")
    header = "@10031000100220645" # index 50 of list of objects
    start_fil = time.time_ns()
    filtered = filter(lambda FastQ_entry: FastQ_entry.header == header, FastQ_entries)
    print("Time to find it:",time.time_ns()-start_fil,"ns")
    print(next(filtered))
    
    
    """
    4) Retourneer de sequentie met hoogste / laagste Phred Score.
    
    Context:
        1. 
        'Met lambda is alles op te lossen'
        
        2.
        Technieken:
            - Objecten
            - max()
            - min()
            - lambda
            - format() (voor printen)
            
        3.
        Zie regel 7
        
        4.
        Het uitvoeren van de functies kost zo'n 0.001 tot 0.002 seconden.
        Dat is niet veel.
        
        5.
        Hier wordt weer gebruik gemaakt van build-in python functies, wat vaak
        de snelste manier is. Maar aangezien de min()/max() wel alle entries
        moeten vergelijken, kost dit meer tijd dan een enkele sequentie ophalen.
        
        6.
        4) en 6) vullen elkaar aan, de eerste index van 6) zou of de minimale waarde of
        de maximale waarde moeten zijn. Als deze overeenkomen, dan zijn beide uitwerkingen
        goed.
        
        7.
        Ook hier zie ik geen mogelijkeheden om de code te versnellen.
    """
    start_max = time.time()
    max_score = max(FastQ_entries, key=lambda FastQ_entry: FastQ_entry.score)
    end_max = time.time()
    start_min = time.time()
    min_score = min(FastQ_entries, key=lambda FastQ_entry: FastQ_entry.score)
    end_min = time.time()
    print("\nMax:\n{} @ {} @ {} s".format(max_score.sequence, max_score.score, (end_max-start_max)))
    print("Min:\n{} @ {} @ {} s".format(min_score.sequence, min_score.score, (end_min-start_min)))
    
    
    
    """
    6) Sorteer het bestand op basis van Phred Score.
    
    Context:
        1.
        Sorteren van een lijst met objecten kan heel makkelijk met lambda.
        
        2.
        Technieken:
            - list().sort()
            - lambda
            - indexen bij printen
            
        3.
        Zie regel 7
        
        4.
        Sorteren kost zo'n 0.003 tot 0.004 seconden met 7981 entries. 
        
        5.
        list().sort() is ook een build-in functie. list().sort() gebruikt een van
        de snelste manieren om de sorteren.
        
        6.
        Als de eerste index van de gesorteerde lijst overeenkomt met de minimale waarde
        of de maximale waarde van de lijst, gekregen van 4), afhankelijk van sorteer 
        volgorde. Dan klopt het resultaat.
        
        7.
        Ook hier zien ik geen mogelijkeheden om de code te versnellen.
    """
    print("\nSorted based on score:")
    print("First index's score before sorting:", FastQ_entries[0].get_score())
    start_sort = time.time()
    FastQ_entries.sort(key=lambda FastQ_entry: FastQ_entry.get_score(), reverse=True)
    end_sort = time.time()
    print("First index's score after sorting:",FastQ_entries[0].get_score())
    print("Time to sort:", end_sort-start_sort, "s")
    
    
    """
    7) Plot de distributie van alle gevonden Phred Scores in een histogram.
    
    Context:
        1.
        matplotlib.pyplot heeft een histogram plotter. Er hoeft alleen een lijst
        met scores in om een resultaat te geven.
        
        2.
        Technieken:
            - Objecten met getters
            - list comprehension
            - plt.hist()
            - plt.title(), etc, (voor opmaak)
            
        3.
        Zie regel 7
        
        4.
        Het aanmaken van de lijst met scores kost zo'n 0.001 tot 0.002 seconden.
        
        5.
        List comprehension is een snelle manier om dit te doen en het ophalen van de 
        score uit het object gaat heel gemakkelijk via een getter.
        
        6.
        Je zou kunnen kijken of de minimale waarde en maximale waarde in het histogram
        overeenkomen met de waardes die in 4) zijn gevonden.
    
        7.
        Dit zou alleen sneller gemaakt kunnen worden als ik een manier kan vinden om
        de lijst met scores sneller aan te maken.     
    """
    start_lc = time.time()
    scores = [fastq_object.get_score() for fastq_object in FastQ_entries]
    end_lc = time.time()
    print("\nTime to make scores list for histogram:", (end_lc-start_lc), "s")
    make_histogram(scores)
    
    
    


"""
1) Lees het bestand. Kan ik het bestand raadplegen? Hoe doe ik dat efficiënt?
Parses the file and puts entries in a list of objects.

Context:
    1.
    Het bestand bestaat uit 4 regels, waarna het patroon zichzelf herhaald.
    'for line in file' gaat per regel door het bestand, door 3 keer file.readline()
    aan te roepen, is 'line' in de for loop altijd de header. De 3 andere regels komen
    van de 3 file.readline(). Het gebruik van een object om de data in op te slaan is iets
    wat ik ben gaan doen met fasta bestanden, het is een stuk makkelijker als er veel
    bewerkingen gedaan moeten worden, er is tenslotte maar 1 lijst met data.
    De 'makkelijkste' methode heeft de overhand.
    
    2. 
    Technieken:
        - Objecten
        - enumerate()
        - Lijsten
        - for-loop
        - if-statements
        - ord() voor ascii score
        - numpy mean() voor gemiddelde ascii score
        
    3.
    Zie regel 7.
    
    4.
    Het lezen, verwerken en opslaan van 8000 entries (32000 regels) kost gemiddeld zo'n
    0.2 seconden, ik weet niet of dit echt heel snel is, maar het is zeker niet
    langzaam
    
    5.
    Naast de for-loop om de gemiddelde score te berekenen, wat maar rond de 35 karakters is, 
    is er maar 1 for-loop om de gehele data in te verwerken tot een lijst. Het gebruik van
    numpy's mean methode om het gemiddelde te berekenen is iet wat langzamer dan
    sum()/len(), maar bij deze lengte dat niet relevant. Bij een lengte van 1.750.000
    is het verschil tussen mean() en sum()/len(), zo'n 0.27 sec vs 0.18 sec.
    
    6. 
    Door een typ-fout in het begin van het schrijven kreeg ik een bevestiging dat
    het berekenen van het gemiddelde goed ging, ipv het gemiddelde kreeg ik de individuele
    scores terug. Waaruit bleek dat de methode werkte als ik het goed had geschreven.
    Na de 'break' in de for-loop het ik ook gekeken of de eerste volgende regel in het bestand
    een header zou zijn, wat het geval was. Dit geeft aan dat er geen fouten in het bestand
    waren en dat alle data correct was in geladen. Daarnaast, er zit geen error-handling 
    in het script, als er ergens een fout is, kwam er wel een error message. Ook het vele
    printen tijdens testen helpt hierbij.
    
    7.
    Ik kan kijken of het berekenen van het gemiddelde sneller kan, bij de rest zie ik
    geen mogelijkheden om het te versnellen.
    
    --:
        In het andere bestand staat een andere uitwerking, deze is 2 tot 4 keer zo snel
        als wat hier staat.
    

"""
def file_parser(filename, threshold):
    
    with open(filename) as file:
        FastQ_entries = []
        start = time.time()
        for index, header in enumerate(file):
            seq = file.readline()
            plus = file.readline()
            
            score = calc_avg_score(file.readline()) 
            if score >= threshold: # Filtering based on a certain threshold
                FastQ_entries.append(FastQ_entry(header, seq, score))
                
            if index >= 8000: # Total lines in file is times 4 as the index only counts the amount of headers.
                end = time.time()
                print("Time to process file:", (end-start), "s")
                break
        
    return FastQ_entries


"""
3) Bereken de Phred score voor iedere Read (gebruik het gemiddelde in alle vragen). 
Phred score is de ascii score.

Context:
    1. 
    Waarom moeilijk doen als numpy gewoon een gemiddelde (mean) methode heeft.
    
    2.
    Technieken:
        - ord()
        - List comprehension
        - numpy.mean()
        
    3.
    Zie regel 7
    
    4.
    Dit kost heel weinig tijd, sum()/len() is in principe sneller, maar dit vind ik netter.
    Het is minder regels code en het verschil tussen de twee is verwaarloosbaar in dit geval.
    
    5.
    Numpy moet het waarschijnlijk omzetten tot een numpy array, wat tijd kost.
    
    6.
    Ik heb van te voren gekeken of ord()-64 de correcte scores geeft op basis van de tabel
    uit de presentatie.
    
    7.
    Het loslaten van de 'netheid' kan dit versnellen.
    
    --:
        Versnelde methode in het andere bestand.
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
    plt.xlabel("Quality score")
    plt.ylabel("Number of entries")
    



if __name__ == "__main__":
    main()