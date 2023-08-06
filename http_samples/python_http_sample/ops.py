import wave
import difflib
import matplotlib.pyplot as plt
import numpy as np


def read_wav_data(filename: str) -> tuple:
    wav = wave.open(filename,"rb") 
    num_frame = wav.getnframes()
    num_channel=wav.getnchannels()
    framerate=wav.getframerate()
    num_sample_width=wav.getsampwidth()
    str_data = wav.readframes(num_frame)
    wav.close() 
    wave_data = np.fromstring(str_data, dtype = np.short) 
    wave_data.shape = -1, num_channel
    wave_data = wave_data.T 
    return wave_data, framerate, num_channel, num_sample_width


def read_wav_bytes(filename: str) -> tuple:
    wav = wave.open(filename,"rb") 
    num_frame = wav.getnframes() 
    num_channel=wav.getnchannels() 
    framerate=wav.getframerate() 
    num_sample_width=wav.getsampwidth()
    str_data = wav.readframes(num_frame) 
    wav.close() 
    return str_data, framerate, num_channel, num_sample_width


def get_edit_distance(str1, str2) -> int:
    leven_cost = 0
    sequence_match = difflib.SequenceMatcher(None, str1, str2)
    for tag, index_1, index_2, index_j1, index_j2 in sequence_match.get_opcodes():
        if tag == 'replace':
            leven_cost += max(index_2-index_1, index_j2-index_j1)
        elif tag == 'insert':
            leven_cost += (index_j2-index_j1)
        elif tag == 'delete':
            leven_cost += (index_2-index_1)
    return leven_cost


def ctc_decode_delete_tail_blank(ctc_decode_list):
    p = 0
    while p < len(ctc_decode_list) and ctc_decode_list[p] != -1:
        p += 1
    return ctc_decode_list[0:p]


def visual_1D(points_list, frequency=1):
    
    fig, ax = plt.subplots(1)
    x = np.linspace(0, len(points_list)-1, len(points_list)) / frequency

    ax.plot(x, points_list)
    fig.show()


def visual_2D(img):
    plt.subplot(111)
    plt.imshow(img)
    plt.colorbar(cax=None, ax=None, shrink=0.5)
    plt.show() 


def decode_wav_bytes(samples_data: bytes, channels: int = 1, byte_width: int = 2) -> list:
    numpy_type = np.short
    if byte_width == 4:
        numpy_type = np.int
    elif byte_width != 2:
        raise Exception('error: unsurpport byte width `' + str(byte_width) + '`')
    wave_data = np.fromstring(samples_data, dtype=numpy_type)
    wave_data.shape = -1, channels
    wave_data = wave_data.T  
    return wave_data


def get_symbol_dict(dict_filename):
    txt_obj = open(dict_filename, 'r', encoding='UTF-8') 
    txt_text = txt_obj.read()
    txt_obj.close()
    txt_lines = txt_text.split('\n') 

    dic_symbol = {}  
    for i in txt_lines:
        list_symbol = [] 
        if i != '':
            txt_l=i.split('\t')
            pinyin = txt_l[0]
            for word in txt_l[1]:
                list_symbol.append(word)
        dic_symbol[pinyin] = list_symbol

    return dic_symbol


def get_language_model(model_language_filename):
    
    txt_obj = open(model_language_filename, 'r', encoding='UTF-8')  
    txt_text = txt_obj.read()
    txt_obj.close()
    txt_lines = txt_text.split('\n')  

    dic_model = {}  
    for i in txt_lines:
        if i != '':
            txt_l = i.split('\t')
            if len(txt_l) == 1:
                continue
            dic_model[txt_l[0]] = txt_l[1]

    return dic_model


def ctc_decode_stream(tokens):
    i = 0
    while i < len(tokens):
        while i+1 < len(tokens) and tokens[i] == tokens[i+1]:
            i += 1
        if i+1 == len(tokens) and tokens[i] != -1:
            return tokens[0], []
        if tokens[i] != -1:
            return tokens[i], tokens[i+1:]
        i += 1
    return -1, []
