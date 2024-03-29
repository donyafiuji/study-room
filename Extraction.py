import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import spacy
from gensim.parsing.preprocessing import STOPWORDS as GENSIM_STOPWORDS
from PyDictionary import PyDictionary
import string
import requests






class Model():    

    def DialogueExtraction(self, path):
        
        # S1E1 for pilot
        with open(path, 'r', encoding='ISO-8859-1') as file:
            
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




    def tag(self, path, season_dir):
        
        matches = self.DialogueExtraction(path)[0]
        for match in matches:
            start_time, end_time, text = match
            time = f'start time = {start_time} , end time = {end_time}'

            if text.startswith ('The One W'):
                tag = f'season {season_dir}, {text}'
            else:
                tag = ''

        return tag, time





    def StopWords(self):

        my_stopwords = set(['the','id','guys','guy','salad','bye', 'gone', 'reason', 'load', 'feeling', 'look', 'phone', 
                            'a', 'an', 'and', 'but', 'or', '1','0','2','3','4','5','6','7','8','liza','brothers','sisters','im','theres','ill','thats','goes','isnt','thats','took','youre','ive','hed','wasnt','la','wee',
    '9','00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', 
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', 
    '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', 'monica', 
    'ross', 'chandler', 'joey', 'rachel','paul','phoebe', 'janice', 'gunther', 'carol', 'susan', 'emily', 'paolo', 'richard', 'frank', 
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
    "'ll",'abandon', 'ability', 'able', 'abortion', 'about', 'above', 'abroad', 'absence', 'absolute', 'absolutely', 'absorb', 'abuse', 'academic', 'accept', 'access', 'accident', 'accompany', 'accomplish', 'according', 'account', 'accurate', 'accuse', 'achieve', 'achievement', 'acid', 'acknowledge', 'acquire', 'across', 'act', 'action', 'active', 'activist', 'activity', 'actor', 'actress', 'actual', 'actually', 'ad', 'adapt', 'add', 'addition', 'additional', 'address', 'adequate', 'adjust', 'adjustment', 'administration', 'administrator', 'admire', 'admission', 'admit', 'adolescent', 'adopt', 'adult', 'advance', 'advanced', 'advantage', 'adventure', 'advertising', 'advice', 'advise', 'adviser', 'advocate', 'affair', 'affect', 'afford', 'afraid', 'African', 'African-American', 'after', 'afternoon', 'again', 'against', 'age', 'agency', 'agenda', 'agent', 'aggressive', 'ago', 'agree', 'agreement', 'agricultural', 'ah', 'ahead', 'aid', 'aide', 'AIDS', 'aim', 'air', 'aircraft', 'airline', 'airport', 'album', 'alcohol', 'alive', 'all', 'alliance', 'allow', 'ally', 'almost', 'alone', 'along', 'already', 'also', 'alter', 'alternative', 'although', 'always', 'AM', 'amazing', 'American', 'among', 'amount', 'analysis', 'analyst', 'analyze', 'ancient', 'and', 'anger', 'angle', 'angry', 'animal', 'anniversary', 'announce', 'annual', 'another', 'answer', 'anticipate', 'anxiety', 'any', 'anybody', 'anymore', 'anyone', 'anything', 'anyway', 'anywhere', 'apart', 'apartment', 'apparent', 'apparently', 'appeal', 'appear', 'appearance', 'apple', 'application', 'apply', 'appoint', 'appointment', 'appreciate', 'approach', 'appropriate', 'approval', 'approve', 'approximately', 'Arab', 'architect', 'area', 'argue', 'argument', 'arise', 'arm', 'armed', 'army', 'around', 'arrange', 'arrangement', 'arrest', 'arrival', 'arrive', 'art', 'article', 'artist', 'artistic', 'as', 'Asian', 'aside',
    'ask', 'asleep', 'aspect', 'assault', 'assert', 'assess', 'assessment', 'asset', 'assign', 'assignment', 'assist', 'assistance', 'assistant', 'associate', 'association', 'assume', 'assumption', 'assure', 'at', 'athlete', 'athletic', 'atmosphere', 'attach', 'attack', 'attempt', 'attend', 'attention', 'attitude', 'attorney', 'attract', 'attractive', 'attribute', 'audience', 'author', 'authority', 'auto', 'available',
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
    '’ve',
    'rachel',
    'ross',
    'monica',
    'chandler',
    'phoebe',
    'joey',
    'janice',
    'gunther',
    'mr. heckles',
    'carol',
    'susan',
    'ben',
    'judy',
    'jack',
    'frank',
    'alice',
    'estelle',
    'richard',
    'emily',
    'janine',
    'ursula',
    'mike',
    'amy',
    'paolo',
    'tag',
    'eddie',
    'gary',
    'stephanie',
    'jill',
    'cecilia',
    'pete',
    'elizabeth',
    'mona',
    'jade',
    'zelner',
    'mr. treeger',
    'cassie',
    'aunt iris',
    'aunt lillian',
    'aunt cookie',
    'nora',
    'helena',
    'frank sr.',
    'phoebe sr.',
    'lily',
    'leslie',
    'howard',
    'cookie',
    'terry',
    'leila',
    'colleen',
    'duncan',
    'trudy',
    'rory',
    'parker',
    'sandrine',
    'the chick',
    'emma',
    'rachel green',
    'ross geller',
    'monica geller',
    'chandler bing',
    'phoebe buffay',
    'joey tribbiani',
    'janice litman goralnik',
    'gunther',
    'mr. heckles',
    'carol willick',
    'susan bunch',
    'ben geller',
    'judy geller',
    'jack geller',
    'frank buffay jr.',
    'alice knight buffay',
    'estelle leonard',
    'richard burke',
    'emily waltham',
    'janine lacroix',
    'ursula buffay',
    'mike hannigan',
    'amy green',
    'paolo',
    'tag jones',
    'eddie menuek',
    'gary',
    'stephanie schiffer',
    'jill green',
    'cecilia monroe',
    'dr. richard burke',
    'pete becker',
    'elizabeth stevens',
    'mona',
    'jade',
    'zelner',
    'mr. treeger',
    'cassie geller',
    'aunt iris',
    'aunt lillian',
    'aunt cookie',
    'nora bing','helena handbasket','frank buffay','phoebe abbott','phoebe buffay','lily buffay','leslie buffay','howard buffay','cookie buffay','terry buffay','leila buffay','colleen buffay','duncan','geller', 'buffay', 'green', 'tribbiani', 'bing', 'perry','trudy','rory','parker','gotta','heres','cancel','helped','things','thing','hes',
    'sandrine','didnt','dont','hed','geller', 'buffay', 'green', 'tribbiani', 'bing', 'perry',
    'the chick','emma geller-green', 'the', 'god','of', 'and', 'to', 'a', 'in', 'that', 'is', 'for', 'it', 'with', 'was', 'as', 'be', 'on', 'not', 'he',
         'by', 'are', 'this', 'or', 'from', 'but', 'have', 'an', 'they', 'which', 'one', 'you', 'were', 'her', 'all',
         'she', 'there', 'would', 'their', 'we', 'him', 'been', 'has', 'when', 'who', 'will', 'more', 'no', 'if',
         'out', 'so', 'said', 'what', 'up', 'its', 'about', 'into', 'than', 'them', 'can', 'only', 'other', 'new',
         'some', 'could', 'these', 'two', 'may', 'then', 'do', 'first', 'any', 'my', 'now', 'such', 'like', 'our',
         'over', 'man', 'me', 'even', 'most', 'made', 'after', 'also', 'did', 'many', 'before', 'must', 'through',
         'back', 'years', 'where', 'much', 'your', 'way', 'well', 'down', 'should', 'because', 'each', 'just', 'those',
         'people', 'mr', 'how', 'too', 'little', 'state', 'good', 'very', 'make', 'world', 'still', 'own', 'see',
         'men', 'work', 'long', 'get', 'here', 'between', 'both', 'life', 'being', 'under', 'never', 'day', 'same',
         'another', 'know', 'while', 'last', 'might', 'us', 'great', 'old', 'year', 'off', 'come', 'since', 'against',
         'go', 'came', 'right', 'used', 'take', 'three', 'without', 'just', 'every', 'think', 'dont', 'might',
         'place', 'end', 'again', 'home', 'himself', 'away', 'part', 'went', 'old', 'want', 'school', 'children',
         'number', 'very', 'she', 'her', 'way', 'even', 'year', 'great', 'such', 'before', 'must', 'went', 'came',
         'own', 'work', 'last', 'many', 'know', 'where', 'these', 'back', 'take', 'through', 'off', 'left', 'under',
         'also', 'might', 'something', 'went', 'went', 'why', 'look', 'want', 'few', 'never', 'house', 'place', 'year',
         'thing', 'every', 'small', 'woman', 'man', 'new', 'life', 'same', 'child', 'work', 'know', 'try', 'hand',
         'every', 'number', 'page', 'should', 'country', 'found', 'answer', 'found', 'sound', 'study', 'still',
         'learn', 'plant', 'cover', 'food', 'sun', 'four', 'between', 'state', 'keep', 'eye', 'never', 'last',
         'let', 'thought', 'city', 'tree', 'cross','about', 'above', 'after', 'again', 'all', 'almost', 'along', 'also', 'always', 'among', 'and', 
         'another', 'any', 'anything', 'are', 'around', 'as', 'at', 'back', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'big', 'both', 'but', 'by', 'call', 'can', 
         'come', 'could', 'day', 'did', 'different', 'do', 'does', 'don\'t', 'down', 'each', 'end', 'even', 'every', 'few', 'find', 'first', 'for', 'found', 'from', 'get', 'give', 'go', 'good', 'great', 'had', 'has', 'have', 'he', 'help', 'her', 'here', 'him', 'his', 'how', 'I', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'know', 'large', 'last', 'left', 'like', 'little', 'long', 'look', 'made', 'make', 'many', 
         'may', 'me', 'men', 'might', 'more', 'most', 'much', 'must', 'my', 'never', 'new', 'no', 'not', 'now', 'of', 'off', 'old', 'on', 'once', 'one', 'only', 'or', 'other', 'our', 'out', 'over', 'own', 'part', 'people', 'place', 'put', 'read', 
         'right', 'said', 'same', 'saw', 'say', 'see', 'she', 'should', 'show', 'small', 'so', 'some', 'something', 'sound', 'still', 'such', 'take', 'tell', 'than', 'that', 'the', 'them', 'then', 'there', 'these', 'they', 'thing', 'think', 'this', 'those', 'thought', 'three', 'through',
          'time', 'to', 'together', 'too', 'two', 'under', 'up', 'us', 'use', 'very', 'want', 'was', 'way', 'we', 'well', 'went', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'why', 'will', 'with', 'without', 'woman', 'work', 'would', 'year', 'you', 'young', 'your','a', 'able', 'about', 'above', 'accept', 'according', 'account', 'across', 'act', 'action', 'active', 'activity', 'actually', 'add', 'address', 'administration', 'admit', 'adult', 'affect', 'after', 'again', 'against', 'age', 'agency', 'agent', 'ago', 'agree', 'agreement', 'ahead', 'air', 'all', 'allow', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'amazing', 'american', 'among', 'amount', 'analysis', 'and', 'animal', 'another', 'answer', 'any', 'anyone', 'anything', 'appear', 'approach', 'area', 'argue', 'arm', 'around', 'arrive', 'art', 'article', 'artist', 'as', 'ask', 'assume', 'at', 'attack', 'attention', 'attorney', 'audience', 'author', 'authority', 'available', 'avoid', 'away', 'baby', 'back', 'bad', 'bag', 'ball', 'bank', 'bar', 'base', 'be', 'beat', 'beautiful', 'because', 'become', 'bed', 'before', 'begin', 'behavior', 'behind', 'believe', 'benefit', 'best', 'better', 'between', 'beyond', 'big', 'bill', 'billion', 'bit', 'black', 'blood', 'blue', 'board', 'body', 'book', 'born', 'both', 'box', 'boy', 'break', 'bring', 'brother', 'budget', 'build', 'building', 'business', 'but', 'buy', 'by', 'call', 'camera', 'campaign', 'can', 'cancer', 'candidate', 'capital', 'car', 'card', 'care', 'career', 'carry', 'case', 'catch', 'cause', 'cell', 'center', 'central', 'century', 'certain', 'certainly', 'chair', 'challenge', 'chance', 'change', 'character', 'charge', 'check', 'child', 'choice', 'choose', 'church', 'citizen', 'city', 'civil', 'claim', 'class', 'clear', 'clearly', 'close', 'coach', 'cold', 'collection', 'college', 'color', 'come', 'commercial', 'common', 'community', 'company', 'compare', 'computer', 'concern', 'condition', 'conference', 'Congress', 'consider', 'consumer', 'contain', 'continue', 'control', 'cost', 'could', 'country', 'couple', 'course', 'court', 'cover', 'create', 'crime', 'cultural', 'culture', 'cup', 'current', 'customer', 'cut', 'dark', 'data', 'daughter', 'day', 'dead', 'deal', 'death', 'debate', 'decade', 'decide', 'decision', 'deep', 'defense', 'degree', 'democrat', 'demonstrate', 'design', 'despite', 'detail', 'determine', 'develop', 'development', 'die', 'difference', 'different', 'difficult', 'dinner', 'direction', 'director', 'discover', 'discuss', 'discussion', 'disease', 'do', 'doctor', 'dog', 'door',
        'baby', 'bird', 'blue', 'book', 'box', 'boy', 'bread', 'cake', 'car', 'cat', 'city', 'day', 'dog', 'door', 'duck', 'egg', 'eye', 'farmer', 'fish', 'flower', 'food', 'frog', 'girl', 'grass', 'hand', 'hat', 'head', 'hill', 'home', 'house', 'ink', 'job', 'juice', 'king', 'kite', 'leaf', 'leg', 'letter', 'light', 'lion', 'man', 'map', 'milk', 'money', 'moon', 'morning', 'mother', 'music', 'name', 'nest', 'night', 'nose', 'orange', 'paper', 'party', 'pen', 'pencil', 'person', 'picture', 'pie', 'pig', 'plant', 'play', 'rabbit', 'rain', 'ring', 'river', 'road', 'rock', 'room', 'rose', 'school', 'seed', 'sheep', 'shoe', 'shop', 'show', 'singer', 'sister', 'sky', 'snow', 'song', 'sound', 'star', 'street', 'sun', 'table', 'teacher', 'thing', 'time', 'toe', 'tree', 'water', 'way', 'web', 'wind', 'window', 'woman', 'wood', 'word', 'world', 'year', 'yellow',
'apple', 'banana', 'car', 'dog', 'elephant', 'fox', 'grape', 'hat', 'igloo', 'jacket', 'kangaroo', 'lemon', 'monkey', 'notebook', 'orange', 'pear', 'queen', 'rabbit', 'sun', 'table', 'umbrella', 'violin', 'water', 'xylophone', 'yak', 'zebra', 'ant', 'boat', 'cat', 'duck', 'egg', 'fish', 'goose', 'horse', 'ink', 'jungle', 'key', 'lion', 'mango', 'night', 'owl', 'pizza', 'quilt', 'rose', 'snake', 'tree', 'unicorn', 'van', 'window', 'xylophone', 'yarn', 'zealot', 'airplane', 'bag', 'computer', 'desk', 'ear', 'football', 'guitar', 'hat', 'ice', 'juice', 'kite', 'lion', 'money', 'note', 'pencil', 'queen', 'rain', 'snake', 'table', 'umbrella', 'vase', 'watch', 'xylophone', 'yacht', 'zeppelin', 'bee', 'carrot', 'dog', 'elephant', 'frog', 'goat', 'hamster', 'igloo', 'jellyfish', 'koala', 'lizard', 'moon', 'nest', 'octopus', 'penguin', 'quail', 'rooster', 'shark', 
'turtle', 'umbrella', 'volcano', 'watermelon', 'xylophone', 'yak', 'zebra', 'air', 'balloon', 'cat', 'donkey', 'eggplant', 'frog', 'grass', 'hamster', 'igloo', 'jacket', 'kite', 'laptop', 'monkey', 'nail', 'orange', 'panda', 'quiche', 'rabbit', 'star', 'tiger', 'unicorn', 'violin', 'water', 'xylophone', 'yogurt', 'zealot',
'a', 'able', 'about', 'above', 'across', 'act', 'actor', 'active', 'activity', 'add', 'afraid', 'after', 'again', 'age', 'ago', 'agree', 'air', 'all', 'alone', 'along', 'already', 'always', 'am', 'amount', 'an', 'and', 'angry', 'another', 'answer', 'any', 'anyone', 'anything', 'anytime', 'appear', 'apple', 'are', 'area', 'arm', 'army', 'around', 'arrive', 'art', 'as', 'ask', 'at', 'attack', 'aunt', 'autumn', 'away',
'baby', 'base', 'back', 'bad', 'bag', 'ball', 'bank', 'basket', 'bath', 'be', 'bean', 'bear', 'beautiful', 'beer', 'bed', 'bedroom', 'behave', 'before', 'begin', 'behind', 'bell', 'below', 'besides', 'best', 'better', 'between', 'big', 'bird', 'birth', 'birthday', 'bit', 'bite', 'black', 'bleed', 'block', 'blood', 'blow', 'blue', 'board', 'boat', 'body', 'boil', 'bone', 'book', 'border', 'born', 'borrow', 'both', 'bottle', 'bottom', 'bowl', 'box', 'boy', 'branch', 'brave', 'bread', 'break', 'breakfast', 'breathe', 'bridge', 'bright', 'bring', 'brother', 'brown', 'brush', 'build', 'burn', 'business', 'bus', 'busy', 'but', 'buy', 'by', 'bundle','cake', 'call', 'can', 'candle', 'cap', 'car', 'card', 'care', 'careful', 'careless', 'carry', 'case', 'cat', 'catch', 'central', 'century', 'certain', 'chair', 'chance', 'change', 'chase', 'cheap', 'cheese', 'chicken', 'child', 'children', 'chocolate', 'choice', 'choose', 'circle', 'city', 'class', 'clever', 'clean', 'clear', 'climb', 'clock', 'cloth', 'clothes', 'cloud', 'cloudy', 'close', 'coffee', 'coat', 'coin', 'cold', 'collect', 'colour', 'comb', 'come', 'comfortable', 'common', 'compare', 'complete', 'computer', 'condition', 'continue', 'control', 'cook', 'cool', 'copper', 'corn', 'corner', 'correct', 'cost', 'contain', 'count', 'country', 'course', 'cover', 'crash', 'cross', 'cry', 'cup', 'cupboard', 'cut',
"dance","danger", "dangerous", "dark", "daughter", "day", "dead", "decide", "decrease", "deep", "deer", "depend", "desk", "destroy", "develop", "die", "different", "difficult", "dinner", "direction", "dirty", "discover", "dish", "do", "dog", "door", "double", "down", "draw", "dream", "dress", "drink", "drive", "drop", "dry", "duck", "dust", "duty", "destroy", "dedicated", "each", "ear", "early", "earn", "earth", "east", "easy", "eat", "education", "effect", "egg", "eight", "either", "electric", "elephant", "else", "empty", "end", "enemy", "enjoy", "enough", "enter", "equal", "entrance", "escape", "even", "evening", "event", "ever", "every", "everyone", "exact", "everybody", "examination", "example", "except", "excited", "exercise", "expect", "expensive", "explain", "extremely", "eye", "face", "fact", "fail", "fall", "false", "family", "famous", "far", "farm", "father", "fast", "fat", "fault", "fear", "feed", "feel", "female", "fever", "few", "fight", "fill", "film", "find", "fine", "finger", "finish", "fire", "first", "fit", "five", "fix", "flag", "flat", "float", "floor", "flour", "flower", "fly", "fold", "food", "fool", "foot", "football", "for", "force", "foreign", "forest", "forget", "forgive", "fork", "form", "fox", "four", "free", "freedom", "freeze", "fresh", "friend", "friendly", "from", "front", "fruit", "full", "fun", "funny", "furniture", "further", "future", "game", "garden", "gate", "general", "gentleman", "get", "gift", "give", "glad", "glass", "go", "goat", "god", "gold", "goodbye", "grandfather", "grandmother", "grass", "grave", "great", "green", "grey", "ground", "group", "grow", "gun", "hair", "half", "hall", "hammer", "hand", "happen", "happy", "hard", "hat", "hate", "have", "he", "head", "healthy", "hear", "heavy", "hello", "help", "heart", "heaven", "height", "hen", "her", "here", "hers", "hide", "high", "hill", "him", "his", "hit", "hobby", "hold", "hole", "holiday", "home", "hope", "horse", "hospital", "hot", "hotel", "house", "how", "hundred", "hungry", "hour", "hurry", "husband", "hurt", "I", "ice", "idea", "if", "important", "in", "increase", "inside", "into",'introduce', 'invent', 'iron', 'invite', 'is', 'island', 'it', 'its', 'job', 'join', 'juice', 'jump', 'just', 'keep', 'key', 'kid', 'kill', 'kind', 'king', 'kitchen', 'knee', 'knife', 'knock', 'know', 'ladder', 'lady', 'lamp', 'land', 'large', 'last', 'late', 'lately', 'laugh', 'lazy', 'lead', 'leaf', 'learn', 'leave', 'leg', 'left', 'lend', 'length', 'less', 'lesson', 'let', 'letter', 'library', 'lie', 'life', 'light', 'like', 'lion', 'lip', 'list', 'listen', 'little', 'live', 'lock', 'lonely', 'long', 'look', 'lose', 'lot', 'love', 'low', 'lower', 'luck', 'machine', 'main', 'make', 'male', 'man', 'many', 'map', 'mark', 'market', 'marry', 'matter', 'may', 'me', 'meal', 'mean', 'measure', 'meat', 'medicine', 'meet', 'member', 'mention', 'method', 'middle', 'milk', 'mill', 'million', 'mind', 'mine', 'minute', 'miss', 'mistake', 'mix', 'model', 'modern', 'moment', 'money', 'monkey', 'month', 'moon', 'more', 'morning', 'most', 'mother', 'mountain', 'mouse', 'mouth', 'move', 'much', 'music', 'must', 'my', 'name', 'narrow', 'nation', 'nature', 'near', 'nearly', 'neck', 'need', 'needle', 'neighbor', 'neither', 'net', 'never', 'new', 'news', 'newspaper', 'next', 'nice', 'night', 'nine', 'no', 'noble', 'noise', 'none', 'nor', 'north', 'nose', 'not', 'nothing', 'notice', 'now', 'number','obey', 'object', 'ocean', 'of', 'off', 'offer', 'office', 'often', 'oil', 'old', 'on', 'one', 'only', 'open', 'opposite', 'or', 'orange', 'order', 'other', 'our', 'out', 'outside', 'over', 'own', 'page', 'pain', 'paint', 'pair', 'pan', 'paper', 'parent', 'park', 'part', 'partner', 'party', 'pass', 'past', 'path', 'pay', 'peace', 'pen', 'pencil', 'people', 'pepper', 'per', 'perfect', 'period', 'person', 'petrol', 'photograph', 'piano', 'pick', 'picture', 'piece', 'pig', 'pill', 'pin', 'pink', 'place', 'plane', 'plant', 'plastic', 'plate', 'play', 'please', 'pleased', 'plenty', 'pocket', 'point', 'poison', 'police', 'polite', 'pool', 'poor', 'popular', 'position', 'possible', 'potato', 'pour', 'power', 'present', 'press', 'pretty', 'prevent', 'price', 'prince', 'prison', 'private', 'prize', 'probably', 'problem', 'produce', 'promise', 'proper', 'protect', 'provide', 'public', 'pull', 'punish', 'pupil', 'Purple', 'push', 'put', 'queen', 'question', 'quick', 'quiet', 'quite', 'radio', 'rain', 'rainy', 'raise', 'reach', 'read', 'ready', 'real', 'really', 'receive', 'record', 'red', 'remember', 'remind', 'remove', 'rent', 'repair', 'repeat', 'reply', 'report', 'rest', 'restaurant', 'result', 'return', 'rice', 'rich', 'ride', 'right', 'ring', 'rise', 'road', 'rob', 'rock', 'room', 'round', 'rubber', 'rude', 'rule', 'ruler', 'run', 'rush', 'sad', 'safe', 'sail', 'salt', 'same', 'sand', 'save', 'say', 'school', 'science', 'scissors', 'search', 'seat', 'second', 'see', 'seem', 'sell', 'send', 'sentence', 'serve', 'seven', 'several', 'sex', 'shade', 'shadow', 'shake', 'shape', 'share', 'sharp', 'she', 'sheep', 'sheet', 'shelf', 'shine', 'ship', 'shirt', 'shoe', 'shoot', 'shop', 'short', 'should', 'shoulder', 'shout', 'show', 'sick', 'side', 'signal', 'silence', 'silly', 'silver', 'similar', 'simple', 'single', 'since', 'sing', 'sink', 'sister', 'sit', 'six', 'size', 'skill', 'skin', 'skirt', 'sky', 'sleep', 'slip', 'slow', 'small', 'smell', 'smile', 'smoke', 'snow', 'so', 'soap', 'sock', 'soft', 'some', 'someone', 'something', 'sometimes', 'son', 'soon', 'sorry', 'sound', 'soup', 'south','space', 'speak', 'special', 'speed', 'spell', 'spend', 'spoon', 'sport', 'spread', 'spring', 'square', 'stamp', 'stand', 'star', 'start', 'station', 'stay', 'steal', 'steam', 'step', 'still', 'stomach', 'stone', 'stop', 'store', 'storm', 'story', 'strange', 'street', 'strong', 'structure', 'student', 'study', 'stupid', 'subject', 'substance', 'successful', 'such', 'sudden', 'sugar', 'suitable', 'summer', 'sun', 'sunny', 'support', 'sure', 'surprise', 'sweet', 'swim', 'sword', 'table', 'take', 'talk', 'tall', 'taste', 'taxi', 'tea', 'teach', 'team', 'tear', 'telephone', 'television', 'tell', 'ten', 'tennis', 'terrible', 'test', 'than', 'that', 'the', 'their', 'theirs', 'then', 'there', 'therefore', 'these', 'thick', 'thin', 'thing', 'think', 'third', 'this', 'those', 'though', 'threat', 'three', 'tidy', 'tie', 'title', 'to', 'today', 'toe', 'together', 'tomorrow', 'tonight', 'too', 'tool', 'tooth', 'top', 'total', 'touch', 'town', 'train', 'tram', 'travel', 'tree', 'trouble', 'true', 'trust', 'twice', 'try', 'turn', 'type', 'uncle', 'under', 'understand', 'unit', 'until', 'up', 'use', 'useful', 'usual', 'usually', 'vegetable', 'very', 'village', 'voice', 'visit', 'value', 'vacuum', 'vampire', 'verb', 'validation', 'wait', 'wake', 'walk', 'want', 'warm', 'wash', 'waste', 'watch', 'water', 'way', 'we', 'weak', 'wear', 'weather', 'wedding', 'week', 'weight', 'welcome', 'well', 'west', 'wet', 'what', 'wheel', 'when', 'where', 'which', 'while', 'white', 'who', 'why', 'wide', 'wife', 'wild', 'will', 'win', 'wind', 'window', 'wine', 'winter', 'wire', 'wise', 'wish', 'with', 'without', 'woman', 'wonder', 'word', 'work', 'world', 'worry', 'worst', 'write', 'wrong', 'year', 'yellow', 'yes', 'yesterday', 'yet', 'you', 'young', 'your', 'yours', 'zero', 'zoo', 'zoom'
])
       
        # stop_words = set(stopwords.words('english'))

        # stop_words.update(my_stopwords)

        nlp = spacy.load("en_core_web_sm")
        spacy_stopwords = nlp.Defaults.stop_words
        gensim_stopwords = set(GENSIM_STOPWORDS)
        stopwords = spacy_stopwords.union(gensim_stopwords)
        my_stopwords.update(stopwords)

        return my_stopwords
    





    # def filter_compound_words(self, dialogue):


    #     prepositions = ["out", "off", "in", "on", "over", "down", "under", "back", "forth", "away", 
    #                     "around", "through", "across", "within", "inside", "outside", "forward", "upon", 
    #                     "with", "through", "to", "toward", "past", "onto", "near", "of", "for", "from", "by", 
    #                     "after", "about", "above", "up"]

    #     # filtered_words = []
    #     # for diag in dialogue:
    #     words = word_tokenize(dialogue.lower())
    #     for i, word in enumerate(words):
    #         if word in prepositions and i + 1 < len(words):
    #             prev_word = words[i - 1]
    #             # Check the POS (Part-of-Speech) tag of the next word
    #             pos = pos_tag([prev_word])[0][1]
    #             # Include compound words with nouns, adjectives, or verbs
    #             if pos.startswith('VB'):
    #                 compound_word = f"{prev_word} {word}"
    #                 # input(compound_word)

    #                 return compound_word
    



    
    def RemovePuncs(self, dialogues):

        # punctuation_marks = '!#$%&\()*+,-./:;<=>?@[\\]^_`{|}~' +"'ll"+'INC'+"''"+'Hi' 
        punctuation_marks = string.punctuation
        translator = str.maketrans('', '', punctuation_marks)

        new_dialogues = []
        dialogues = dialogues

        # Remove punctuation marks from each line in dialogues and append to new_dialogues
        for line in dialogues:
            line = line.translate(translator)
            new_dialogues.append(line)

        return new_dialogues
    
    




    def WordFilter(self, dialogues):

        stop_words = self.StopWords()
        words = dialogues.lower().split()

        filtered_words = [word for word in words if word not in stop_words]

        prepositions = ["out", "off", "in", "on", "over", "down", "under", "back", "forth", "away", 
                "around", "through", "across", "within", "inside", "outside", "forward", "upon", 
                "with", "through", "to", "toward", "past", "onto", "near", "of", "for", "from", "by", 
                "after", "about", "above", "up"]

        # filtered_words = []
        # for diag in dialogue:
        words = word_tokenize(dialogues.lower())
        for i, word in enumerate(words):
            if word in prepositions and i + 1 < len(words):
                prev_word = words[i - 1]
                # Check the POS (Part-of-Speech) tag of the next word
                pos = pos_tag([prev_word])[0][1]
                # Include compound words with nouns, adjectives, or verbs
                if pos.startswith('VB'):
                    compound_word = f"{prev_word} {word}"
                    # input(compound_word)
                    filtered_words.append(compound_word)

        return filtered_words
    




    def Translator(self, word):



        """ this uses a local dataset or WordNet database to retrieve the meanings. """
        dictionary = PyDictionary()

        # meaning = GoogleTranslator(source='auto', target='fa').translate(word)
        meaning = dictionary.meaning(word)


        synonyms = []
        translations =[]

        # Get synsets (sets of synonyms) for the word
        synsets = wordnet.synsets(word)

        # Extract synonyms from each synset
        for synset in synsets:
            for lemma in synset.lemmas():
                synonyms.append(lemma.name())

        synonyms=set(synonyms)

        # for syn in synonyms:
            
        #     translations.append(f" {GoogleTranslator(source='auto', target='fa').translate(syn)} ")




        return meaning,synonyms






    def persian_mean(self, word):
        


        api_url = "https://www.faraazin.ir/api/dictionary"
        params = {"text": word}

        response = requests.get(api_url, params=params)
        data = response.json()

        if data['notFound'] == False: 

            # Assuming you have the JSON response stored in the variable 'response'

            type_to_meanings = data['typeToMeanings']

            # Create a list to store the categorized meanings
            categorized_meanings = []

            # Iterate over each type and extract the meanings
            for word_type, meanings_info in type_to_meanings.items():
                meanings = meanings_info['meanings']
                categorized_meanings.append(f'{word_type}: {meanings}')

            # Join the categorized meanings into a single string
            output = '\n'.join(categorized_meanings)

            return output, type_to_meanings
        
        elif data['notFound'] == True: 

            output = GoogleTranslator(source='auto', target='fa').translate(word)
            print('the alternative applied')
                
            return output, None
        
    




    def persian_mean2(self, word):



        """ this uses a local dataset or WordNet database to retrieve the meanings. """
        dictionary = PyDictionary()

        meaning = GoogleTranslator(source='auto', target='fa').translate(word)
        # meaning = dictionary.meaning(word)


        # synonyms = []
        # translations =[]

        # # Get synsets (sets of synonyms) for the word
        # synsets = wordnet.synsets(word)

        # # Extract synonyms from each synset
        # for synset in synsets:
        #     for lemma in synset.lemmas():
        #         synonyms.append(lemma.name())

        # synonyms=set(synonyms)

        # for syn in synonyms:
            
        #     translations.append(f" {GoogleTranslator(source='auto', target='fa').translate(syn)} ")




        return meaning






    def JSON(self, word):


        api_url = "https://www.faraazin.ir/api/dictionary"
        params = {"text": word}

        response = requests.get(api_url, params=params)
        data = response.json()

        return data
    



    
    def Example(self, word):

        example_sentences = []
        synsets = wordnet.synsets(word)

        if synsets:
            # first_synset = synsets[0]
            # examples = first_synset.examples()
            # if examples:
            #     if word in examples:
            #         return examples

            # else:
            #     try:
            #         first_synset = synsets[1]
            #         examples = first_synset.examples()
            #         if examples:
            #             if word in examples:
            #                 return examples
            #     except:
            #         pass         
            for synset in synsets:
                for lemma in synset.lemmas():
                    for example in lemma.synset().examples():
                        sentences = sent_tokenize(example)
                        for sentence in sentences:
                            if word in sentence.lower():
                                example_sentences.append(sentence)

            example_sentences = list(set(example_sentences))

        return example_sentences