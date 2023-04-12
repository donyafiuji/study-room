import re

class WordExtraction():

    def DialogueExtraction(self):
        
        # S1E1 for pilot
        with open('english/season 1/Friends - 1x01 - The One Where Monica Gets A Roommate.SAiNTS.en.srt', 'r') as file:
            
            content = file.read()

            # Use regex to separate timestamp and subtitle text
            pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\d{2}:\d{2}:\d{2},\d{3}|\n\n|$)'
            matches = re.findall(pattern, content, re.DOTALL)
        
        dialogues = []
        # Print the matches
        for match in matches:
            start_time, end_time, dialogue = match
            dialogue = dialogue.replace('\n', ' ')
            dialogue = dialogue.replace('\ ', '')
            dialogues.append(dialogue)
        
        return matches, dialogues

    def tag(self):

        for match in DialogueExtraction.matches:
            start_time, end_time, text = match
            if text.startswith ('The One W'):
                tag = f'season 1 , {text}'
                time = f'start time = {start_time} , end time = {end_time}'
                print(tag)
                print(time)
        return tag,time