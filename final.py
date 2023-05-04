from loadSubtitle import loadSubtitle
import Extraction 
from importlib import reload
import string
import csv
import itertools
import glob








WordExtraction = Extraction.Model()
load = loadSubtitle()
seasons, file_adresess = load.loadseasons('english')
load.process_subtitles('english')

season_dir = input('please enter the season name: ')
file_adresess = []

for filename in glob.glob(f'english/{season_dir}/*.srt'):
    file_adresess.append(filename)




for path in file_adresess:

    matches, dialogues, start_times, end_times  = WordExtraction.DialogueExtraction(path)

    tag, time = WordExtraction.tag(path)
    # translateds = []
    # initialwords = []
    # meanings = []
    # example_sentences = []

    new_dialogues = WordExtraction.RemovePuncs(dialogues)

    initialwords = []

    for i in range(len(new_dialogues)):

        initialwords.append(WordExtraction.WordFilter(new_dialogues[i]))
        initialwords = [x for x in initialwords if x]
    initialwords = list(itertools.chain(*initialwords))

    word_to_dialogue_indices = {}
    word_to_starttime_indices = {}
    word_to_endtime_indices = {}

    for dialogue,start_time,end_time in zip(new_dialogues,start_times,end_times):
        for word in initialwords:
            if word in dialogue:
                # if word not in word_to_dialogue_indices:
                word_to_dialogue_indices[dialogue] = [word]
                word_to_starttime_indices[start_time] = [word]
                word_to_endtime_indices[end_time] = [word]
                
            else:
                continue


    # deleting the repetetive values of the dictionary

    unique_word_to_dialogue_indices = {}
    unique_word_to_starttime_indices = {}
    unique_word_to_endtime_indices = {}

    for key, value in word_to_dialogue_indices.items():
        if value not in unique_word_to_dialogue_indices.values():
            unique_word_to_dialogue_indices[key] = value

    for key, value in word_to_starttime_indices.items():
        if value not in unique_word_to_starttime_indices.values():
            unique_word_to_starttime_indices[key] = value

    for key, value in word_to_endtime_indices.items():
        if value not in unique_word_to_endtime_indices.values():
            unique_word_to_endtime_indices[key] = value  


    # initialwords = []

    # initialwords = list(initialwords)
    # wordcount = 0

    with open('season.csv', 'w', newline='') as csvfile:
        fieldnames = ['Word', 'Translation', 'Meaning', 'Example Sentence', 'Tag', 'Dialogue', 'Start Time', 'End Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for diag, starttime, endtime in zip(unique_word_to_dialogue_indices.keys(), unique_word_to_starttime_indices.keys(), unique_word_to_endtime_indices.keys()):
            # input(unique_word_to_dialogue_indices[key])
            # initialwords.append(WordExtraction.WordFilter(new_dialogues[i]))
            # input(initialwords[0])
            # initialwords = [x for x in initialwords if x]
            # initialwords = list(itertools.chain(*initialwords))
            # input(initialwords)
                # for word in initialwords: #300         300 
            # print(diag)
            # print(starttime)
            # print(endtime)
            try:
                translated, meaning = WordExtraction.Translator(unique_word_to_dialogue_indices[diag][0])
                # input(translated)
                # input(unique_word_to_dialogue_indices[diag][0])
                # input(meaning)
                example = WordExtraction.Example(unique_word_to_dialogue_indices[diag][0])

                writer.writerow({
                    'Word': unique_word_to_dialogue_indices[diag][0],
                    'Translation': translated, 
                    'Meaning': meaning,
                    'Example Sentence': example,
                    'Tag' : tag,
                    'Dialogue' : diag,
                    'Start Time' : starttime,
                    'End Time' : endtime
                })
                
            except Exception as e:
                
                print(f"Error occurred while translating word '{word}': {e}")
                continue  # Skip to the next word if translation fails
