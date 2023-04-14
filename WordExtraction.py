import re
import nltk
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator
import spacy
from gensim.parsing.preprocessing import STOPWORDS as GENSIM_STOPWORDS


def DialogueExtraction(path):
    
    # S1E1 for pilot
    with open(path, 'r') as file:
        
        content = file.read()

        # Use regex to separate timestamp and subtitle text
        pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d{2}:\d{2}:\d{2},\d{3}|\n\n|$)'
        matches = re.findall(pattern, content, re.DOTALL)

    start_times = []
    end_times = []
    dialogues = []

    # Print the matches
    for match in matches:
        start_time, end_time, dialogue = match
        dialogue = dialogue.replace('\n', ' ')
        dialogue = dialogue.replace('\ ', '')
        dialogues.append(dialogue)
        start_times.append(start_time)
        end_times.append(end_time)
    
    return matches, dialogues,start_times, end_times

def tag(path):
    
    matches = DialogueExtraction(path)[0]
    for match in matches:
        start_time, end_time, text = match
        if text.startswith ('The One W'):
            tag = f'season 1 , {text}'
            time = f'start time = {start_time} , end time = {end_time}'

    return tag, time

def StopWords():

    nltk.download('stopwords')
    my_stopwords = set(['the','The', 'a', 'an', 'and', 'but', 'or', 1','0','2','3','4','5','6','7','8',
 '9',
 'One',
 'Two',
 'There',
 'Four',
 'Five',
 'Six',
 'Sex',
 'Seven',
 'Eight',
 'Nine',
 'Ten',
 "It's",
 'That',
 'have',
 'Where',
 'What',
 'Who',
 'All',
 'I',
 'You',
 'A',
 'An',
 'Joey',
 'Ross',
 'Phoebe',
 'Rachel',
 'Carl',
 'Monica',
 'Chandler',
 'Carol',
 'Jennis',
 'With',
 'To',
 'to',
 'too',
 'Too',
 'They',
 'Mom',
 'Dad'])
    
    filtered_words = []
    stop_words = set(nltk.corpus.stopwords.words('english'))

    stop_words.update(my_stopwords)

    nlp = spacy.load("en_core_web_sm")
    spacy_stopwords = nlp.Defaults.stop_words
    gensim_stopwords = set(GENSIM_STOPWORDS)
    stopwords = spacy_stopwords.union(gensim_stopwords)
    stop_words.update(stopwords)

    return stop_words



def Translator(dialogues):

    stop_words = StopWords()
    words = dialogues.lower().split()

    filtered_words = [word for word in words if word not in stop_words]
    
    translateds = []

    for word in filtered_words:

        translated = GoogleTranslator(source='auto', target='fa').translate(word)
        translateds.append(translated)

    return translateds, filtered_words