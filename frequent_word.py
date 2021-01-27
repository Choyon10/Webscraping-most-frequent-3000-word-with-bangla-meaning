import requests
import pandas as pd
from bs4 import BeautifulSoup
from google_trans_new import google_translator 
from collections import OrderedDict 
import json
import pickle

def raw_data():
    page = requests.get('https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/')
    soup = BeautifulSoup(page.content,'html.parser') 
    body = str(soup.findAll('p'))
    all_word = ' '.join(body.split('<br/>')).split('</p>')[-2].split()
    for i in all_word:
        if not i.isalpha():
            all_word.remove(i)
    return all_word

def translate_word(word):
    translator = google_translator()  
    return translator.translate(word,lang_tgt='bn') 

def make_excel(word,meaning):
    df = pd.DataFrame({'Word':word,
                        'Meaning':meaning})
    return df
def save_excel(df):
    df.to_excel('most_frequent_word.xlsx',index=False)


if __name__ == "__main__":   
    word_list = raw_data()[1:]
    word_meaning = OrderedDict()
    for word in word_list:
        try:
            word_meaning[word] = translate_word(word)
        except:
            pass

    in_json = json.dumps(word_meaning)
    with open('word_meaning.pickle', 'wb') as handle:
        pickle.dump(word_meaning, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('meaning.txt','w') as f:
        for key,val in word_meaning.items():
            f.write("%s %s \n"%(key,val))
    
    # word_meaning = make_excel(word_list[:10],meaning_list)
    # save_excel(word_meaning)
