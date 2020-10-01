from io import open

class ScoreFile():
    def __init__(self):
        self.path = 'data\\score.txt'
        
    def check_top(self, player_score:int):
        result = True
        score_lst = self.__str__int__()
        #revisa la ultima posicion y se fija si entra en el top o no
        result = player_score > score_lst[-1][1] or len(score_lst)<5
        return result
     
    
    def save_score(self, name : str, score : int):
        open_ = False
        try:
            arc = open(self.path,'a')
            open_ = True
            arc.write('{}:{}\n'.format(name, score))
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
        
    def override_file(self):
        scores = self.__str__int__()
        try:
            file_ = open(self.path,'w')
            index = 0
            for e in scores:
                file_.write('{}:{}\n'.format(e[0],e[1]))
                index+=1
                if index>4:
                    break
        except:
            raise Exception('[WARNING] Not found or empty txt')
        finally:
            file_.close()

def main():
    file_ =  ScoreFile()
    if file_.check_top(11):
        print("No entra en el top 10")
    else:
        print("Entra en el top 10")
    
if __name__ == "__main__":
    main()

# scorefile.filemanager