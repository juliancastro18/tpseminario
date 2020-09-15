from io import open

class ScoreFile():
    def __init__(self):
        self.path = 'data\\score.txt'
    
    def save_score(self, name : str, score : int, override = False):
        open_ = False
        try:
            if self.check_name(name) and not override:
                raise ValueError('[WARINING] EXISTE ESE NOMBRE')
            elif override:
                print('Todavia no se implemento')
            else:
                arc = open(self.path,'a')
                open_ = True
                arc.write('{}:{}\n'.format(name, score))
        except ValueError as Existe:
            print('[WARINING] EXISTE ESE NOMBRE')
            return False
        except:
            print('[WARNING] Not found')
        finally:
            if open_:
                arc.close()
    
    def __load_scores(self):
        scores = ''
        try:
            arc = open(self.path,'r')
            arc.seek(0)
            scores =  arc.readlines()
        except:
            print('[WARNING] Not found')
        finally:
            arc.close()
            return scores
    
    def check_name(self, name):
        scores = self.__load_scores()
        if scores == '':
            raise Exception('[WARNING] Not found or empty txt')
        else:
            exists = False
            index = 0
            len_of_scores = len(scores)
            while(not exists and len_of_scores > index):
                pos_of_delimiter = scores[index].find(':')
                aux_name = scores[index][:pos_of_delimiter]
                exists = aux_name == name
                index+=1
            return exists
        
    def __str__int__(self):
        scores = self.__load_scores()
        if scores == '':
            raise Exception('[WARNING] Not found or empty txt')
        else:
            index = 0
            len_of_scores = len(scores)
            lst = []
            while(len_of_scores > index):
                pos_of_delimiter = scores[index].find(':')
                aux_name = scores[index][:pos_of_delimiter]
                aux_score = int(scores[index][pos_of_delimiter + 1:] )
                lst.append((aux_name,aux_score))
                index+=1
            return sorted(lst,key = lambda x : x[1],reverse = True)


def main():
    file_ =  ScoreFile()
    for element in file_.__str__int__():
        print(element)
    file_.save_score('pepe_grillo',100,override=True)
    
if __name__ == "__main__":
    main()

# scorefile.filemanager