#!pip install sudachipy
#!pip install sudachidict_core
#上記２つのライブラリを先にインストール


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sudachipy import tokenizer
from sudachipy import dictionary
 
rawdate = r"読み込みたいファイルのパスを指定"
data = pd.read_excel(rawdate, usecols=["使いたいカラムの番号を指定"])#rawdateで指定したファイル形式に合わせてメソッドを変える。例⇒「rawdate」でcsvファイルを読み込んでいたらはpd.read_csv()と書き換える
input_text_data = data["カラム名を指定"]

input_text_data
 
TARGET_POS = ["名詞"]
 
stop_words_dict = r"ストップワード設定用ファイル.xlsxをダウンロードしてパスを指定。"
stop_words_dict = pd.read_excel(stop_words_dict, header=None)#stop_words_ristにcsvファイルを読み込んでいたらpd.read_csv()に変更
STOP_WORDS = [i for i in stop_words_dict[0]]
 
fpath = "PCのフォントパスを指定"

tokenizer_obj = dictionary.Dictionary().create()
 
mode = tokenizer.Tokenizer.SplitMode.C
 
def create_add_info_morph_list(input_text_data):
    
    input_text_list = [i for i in input_text_data]
    morph_list = []
    add_info_morph_list = []
    for sentence in input_text_list:
        base = [m.dictionary_form() for m in tokenizer_obj.tokenize(sentence, mode)]
        norm = [m.normalized_form() for m in tokenizer_obj.tokenize(sentence, mode)]
        pos = [m.part_of_speech()[0] for m in tokenizer_obj.tokenize(sentence, mode)]
        pos1 = [m.part_of_speech()[1] for m in tokenizer_obj.tokenize(sentence, mode)]
        for b, n, p, p1 in zip(base, norm, pos, pos1):
            morph = {"base":b, "norm":n, "pos":p, "pos1":p1}
            if morph["pos"] == "名詞" and morph["pos1"] == "固有名詞":
                morph["base"] = morph["norm"]
            if morph["pos"] in TARGET_POS and\
            morph["base"] not in STOP_WORDS:
                morph_list.append(morph)
        add_info_morph_list.append(morph_list)
        morph_list = []
    return add_info_morph_list
 
add_info_morph_list = create_add_info_morph_list(input_text_data)
 
add_info_morph_list
 
word_list = []
words_list = []
for sentence in add_info_morph_list:
    for i in range(0, len(sentence)):
        word = sentence[i]["base"]
        word_list.append(word)
    words_list.append(word_list)
    word_list = []
 
words_list
 
wc_list = []
for word in words_list:
    for w in word:
        wc_list.append(w)
        wc_str = " ".join(wc_list)
 
wordcloud = WordCloud(
    font_path = fpath,
    width = 900, height=500,
    background_color = "white",
    max_words = 500,
    max_font_size = 150,
    min_font_size = 4,
    collocations = False,
).generate(wc_str)

plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
