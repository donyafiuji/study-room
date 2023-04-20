import glob



class loadSubtitle():


    def loadseasons(self, parent_dir):

        # parent_dir = str(parent_dir)
        seasons =[] 
        file_adresess = []

        for season in range(1, 11):
            season_dir = f'{parent_dir}/season {season}'
            seasons.append(f'season {season}')

            for filename in glob.glob(f'{season_dir}/*.srt'):
                file_adresess.append(filename)
                with open(filename, 'r+', encoding='ISO-8859-1') as file:

                    # this code removes the empty lines of the file
                    content = file.readlines()
                    content = [line for line in content if line.strip()]
                    file.seek(0) 
                    file.writelines(content)
                    file.truncate()


        return seasons, file_adresess



    def process_subtitles(self, parent_dir):


        parent_dir = str(parent_dir)

        for season in range(1, 11):
            season_dir = f'{parent_dir}/season {season}'

            for filename in glob.glob(f'{season_dir}/*.srt'):
                with open(filename, 'r+', encoding='ISO-8859-1') as file:

                    # filters out lines that start with a unknown char
                    content = file.readlines()
                    content = [line for line in content if not line.startswith('[')]
                    file.seek(0) 
                    file.writelines(content)
                    file.truncate()  


        for season in range(1, 11):

            season_dir = f'{parent_dir}/season {season}'
            for filename in glob.glob(f'{season_dir}/*.srt'):
                with open(filename, 'r+', encoding='ISO-8859-1') as file:

                    # filters out lines that start with a digit
                    content = file.readlines()
                    content = [line for line in content if not line.lstrip().startswith(tuple(str(x) for x in [1,2,3,4,5,6,7,8,9]))]  
                    file.seek(0) 
                    file.writelines(content)
                    file.truncate()  


