import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import spacy
from gensim.parsing.preprocessing import STOPWORDS as GENSIM_STOPWORDS
from PyDictionary import PyDictionary
import string



class Model():    

    def DialogueExtraction(self, path):
        
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


    def tag(self, path):
        
        matches = self.DialogueExtraction(path)[0]
        for match in matches:
            start_time, end_time, text = match
            if text.startswith ('The One W'):
                tag = f'season 1 , {text}'
                time = f'start time = {start_time} , end time = {end_time}'

        return tag, time


    def StopWords(self):

        my_stopwords = set(['the','The', 'a', 'an', 'and', 'but', 'or', '1','0','2','3','4','5','6','7','8',
    '9','00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', 
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', 
    '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', 'monica', 
    'ross', 'chandler', 'joey', 'rachel', 'phoebe', 'janice', 'gunther', 'carol', 'susan', 'emily', 'paolo', 'richard', 'frank', 
    'alice', 'judy', 'jack', 'jill', 'barry', 'estelle', 'mr', 'mrs', 'dr', 'aunt', 'uncle', 'grandma', 'grandpa', 'cousin', 
    'niece', 'nephew', 'brother', 'sister', 'dad', 'mom', 'baby', 'child', 'children', 'kid', 'kids', 'friend', 'friends', 'hey', 
    'hi', 'hello', 'okay', 'ok', 'yes', 'no', 'yeah', 'uh', 'um', 'well', 'like', 'right', 'just', 'really', 'know', 'got', 'get', 
    'go', 'gonna', 'wanna', 'let', 'oh', 'ooh', 'woo', 'ha', 'haha', 'he', 'she', 'him', 'her', 'they', 'them', 'us', 'we', 'you', 
    'me', 'my', 'mine', 'our', 'yours', 'his', 'hers', 'theirs', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
    'has', 'had', 'do', 'does', 'did', 'done', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'ought', 'shall', 
    'shouldn', 'couldn', 'can', 'wouldn', 'wasn', 'a', 'about', 'above', 'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 
        'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 
        'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 
        'back', 'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes', 'been', 'before', 
        'began', 'behind', 'being', 'beings', 'best', 'better', 'between', 'big', 'both', 'but', 'by', 'c', 'came', 
        'can', 'cannot', 'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 'did', 
        'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'downed', 'downing', 'downs', 'during', 
        'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 'ever', 'every',
        'everybody', 'everyone', 'everything', 'everywhere', 'f', 'face', 'faces', 'fact', 'facts', 'far', 'felt', 
        'few', 'find', 'finds', 'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 'furthering',
        'furthers', 'g', 'gave', 'general', 'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good',
        'goods', 'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has', 
        'have', 'having', 'he', 'her', 'here', 'herself', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 
        'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 'interesting', 'interests', 'into', 'is', 
        'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 'l', 
        'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 'lets', 'like', 'likely', 'long', 'longer',
        'longest', 'm', 'made', 'make', 'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 
        'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed','a', 'about', 
        'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being'
        , 'below', 'between', 'both', 'but', 'by', 'could', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further',
        'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it',
        'its', 'itself', 'just', 'me', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
        'own', 'same', 'she', 'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 
        'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves',"'d",
    "'ll",
    "'m",
    "'re",
    "'s",
    "'ve",
    '-',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'a',
    'about',
    'above',
    'across',
    'after',
    'afterwards',
    'again',
    'against',
    'ain',
    'all',
    'almost',
    'alone',
    'along',
    'already',
    'also',
    'although',
    'always',
    'am',
    'among',
    'amongst',
    'amoungst',
    'amount',
    'an',
    'and',
    'another',
    'any',
    'anyhow',
    'anyone',
    'anything',
    'anyway',
    'anywhere',
    'are',
    'aren',
    "aren't",
    'around',
    'as',
    'at',
    'back',
    'be',
    'became',
    'because',
    'become',
    'becomes',
    'becoming',
    'been',
    'before',
    'beforehand',
    'behind',
    'being',
    'below',
    'beside',
    'besides',
    'between',
    'beyond',
    'bill',
    'both',
    'bottom',
    'but',
    'by',
    'ca',
    'call',
    'can',
    'cannot',
    'cant',
    'carl',
    'carol',
    'chandler',
    'co',
    'computer',
    'con',
    'could',
    'couldn',
    "couldn't",
    'couldnt',
    'cry',
    'd',
    'dad',
    'de',
    'describe',
    'detail',
    'did',
    'didn',
    "didn't",
    'do',
    'does',
    'doesn',
    "doesn't",
    'doing',
    'don',
    "don't",
    'done',
    'down',
    'due',
    'during',
    'each',
    'eg',
    'eight',
    'either',
    'eleven',
    'else',
    'elsewhere',
    'empty',
    'enough',
    'etc',
    'even',
    'ever',
    'every',
    'everyone',
    'everything',
    'everywhere',
    'except',
    'few',
    'fifteen',
    'fifty',
    'fill',
    'find',
    'fire',
    'first',
    'five',
    'for',
    'former',
    'formerly',
    'forty',
    'found',
    'four',
    'from',
    'front',
    'full',
    'further',
    'get',
    'give',
    'go',
    'had',
    'hadn',
    "hadn't",
    'has',
    'hasn',
    "hasn't",
    'hasnt',
    'have',
    'haven',
    "haven't",
    'having',
    'he',
    'hence',
    'her',
    'here',
    'hereafter',
    'hereby',
    'herein',
    'hereupon',
    'hers',
    'herself',
    'hi.',
    'him',
    'himself',
    'his',
    'how',
    'however',
    'hundred',
    'i',
    "i'd",
    "i'm",
    "i've",
    'ie',
    'if',
    'in',
    'inc',
    'indeed',
    'interest',
    'into',
    'is',
    'isn',
    "isn't",
    'it',
    "it's",
    'it.',
    'its',
    'itself',
    'jennis',
    'joey',
    'just',
    'keep',
    'kg',
    'km',
    'last',
    'latter',
    'latterly',
    'least',
    'less',
    'll',
    'ltd',
    'm',
    'ma',
    'made',
    'make',
    'many',
    'may',
    'me',
    'meanwhile',
    'might',
    'mightn',
    "mightn't",
    'mill',
    'mine',
    'mom',
    'monica',
    'more',
    'moreover',
    'most',
    'mostly',
    'move',
    'much',
    'must',
    'mustn',
    "mustn't",
    'my',
    'myself',
    "n't",
    'name',
    'namely',
    'needn',
    "needn't",
    'neither',
    'never',
    'nevertheless',
    'next',
    'nine',
    'no',
    'nobody',
    'none',
    'noone',
    'nor',
    'not',
    'nothing',
    'now',
    'nowhere',
    'n‘t',
    'n’t',
    'o',
    'of',
    'off',
    'often',
    'on',
    'once',
    'one',
    'one.',
    'only',
    'onto',
    'or',
    'other',
    'others',
    'otherwise',
    'our',
    'ours',
    'ourselves',
    'out',
    'over',
    'own',
    'part',
    'per',
    'perhaps',
    'phoebe',
    'please',
    'put',
    'quite',
    'rachel',
    'rather',
    're',
    'really',
    'regarding',
    'ross',
    's',
    'same',
    'say',
    'see',
    'seem',
    'seemed',
    'seeming',
    'seems',
    'serious',
    'seven',
    'several',
    'sex',
    'shan',
    "shan't",
    'she',
    "she's",
    'should',
    "should've",
    'shouldn',
    "shouldn't",
    'show',
    'side',
    'since',
    'sincere',
    'six',
    'sixty',
    'so',
    'some',
    'somehow',
    'someone',
    'something',
    'sometime',
    'sometimes',
    'somewhere',
    'still',
    'such',
    'system',
    't',
    'take',
    'ten',
    'than',
    'that',
    "that'll",
    'the',
    'their',
    'theirs',
    'them',
    'themselves',
    'then',
    'thence',
    'there',
    'thereafter',
    'thereby',
    'therefore',
    'therein',
    'thereupon',
    'these',
    'they',
    'thick',
    'thin',
    'third',
    'this',
    'those',
    'though',
    'three',
    'through',
    'throughout',
    'thru',
    'thus',
    'to',
    'together',
    'too',
    'top',
    'toward',
    'towards',
    'twelve',
    'twenty',
    'two',
    'un',
    'under',
    'unless',
    'until',
    'up',
    'upon',
    'us',
    'used',
    'using',
    'various',
    've',
    'very',
    'via',
    'was',
    'wasn',
    "wasn't",
    'we',
    'well',
    'were',
    'weren',
    "weren't",
    'what',
    'whatever',
    'when',
    'whence',
    'whenever',
    'where',
    'whereafter',
    'whereas',
    'whereby',
    'wherein',
    'whereupon',
    'wherever',
    'whether',
    'which',
    'while',
    'whither',
    'who',
    'whoever',
    'whole',
    'whom',
    'whose',
    'why',
    'will',
    'with',
    'within',
    'without',
    'won',
    "won't",
    'would',
    'wouldn',
    "wouldn't",
    'y',
    'yet',
    'you',
    "you'd",
    "you'll",
    "you're",
    "you've",
    'your',
    'yours',
    'yourself',
    'yourselves',
    '‘d',
    '‘ll',
    '‘m',
    '‘re',
    '‘s',
    '‘ve',
    '’d',
    '’ll',
    '’m',
    '’re',
    '’s',
    '’ve']
    )
        
        # stop_words = set(stopwords.words('english'))

        # stop_words.update(my_stopwords)

        nlp = spacy.load("en_core_web_sm")
        spacy_stopwords = nlp.Defaults.stop_words
        gensim_stopwords = set(GENSIM_STOPWORDS)
        stopwords = spacy_stopwords.union(gensim_stopwords)
        my_stopwords.update(stopwords)

        return my_stopwords

    
    def RemovePuncs(self, dialogues):

        # punctuation_marks = string.punctuation + '.'+ ','+ '?'+ '!'+ ':'+ ';'+ '"'+ "'"+ '-'+ '—'+ '('+ ')'+ '['+ ']'+ '{'+ '}'+ '...'+ '/'+'\\'+ '&'+ '@'+ '#'+ '$'+ '%'+ '^'+ '*'+ '+'+ '='+ '<'+ '>'+ '_'+ '|'+'..'+"'s"+"'re"+"'ll"+'INC'+"''"+'Hi' 
        punctuation_marks = string.punctuation
        translator = str.maketrans('', '', punctuation_marks)

        new_dialogues = []
        dialogues = dialogues

        # Remove punctuation marks from each line in dialogues and append to new_dialogues
        for line in dialogues:
            line = line.translate(translator)
            new_dialogues.append(line)

        return new_dialogues



    def Translator(self, dialogues):


        dictionary = PyDictionary()

        stop_words = self.StopWords()
        words = dialogues.lower().split()

        filtered_words = [word for word in words if word not in stop_words]

        translateds = []
        meanings = []
        example_sentences = []


        for word in filtered_words:

            translated = GoogleTranslator(source='auto', target='fa').translate(word)
            translateds.append(translated)
            meanings.append(dictionary.meaning(word))



        for word in filtered_words:

            synsets = wordnet.synsets(word)
            print(len(synsets))

            if synsets:
                first_synset = synsets[0]
                examples = first_synset.examples()
                if examples:
                    example_sentences.append(examples)

                else:
                    try:
                        first_synset = synsets[1]
                        examples = first_synset.examples()
                        if examples:
                            example_sentences.append(examples)
                    except:
                        pass 
                        # else:
                        #     first_synset = synsets[2]
                        #     examples = first_synset.examples()
                        #     example_sentences.append(examples)

            else:
                example_sentences.append('')

    
        return translateds, filtered_words, meanings, example_sentences

        