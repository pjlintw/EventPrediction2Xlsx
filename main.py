"""Map monk_name, subject and keyword to model predictions"""

import pickle
import pandas as pd

def load_items_from_file(fn):
    """Load items from file"""
    result = [kw.strip() for kw in open(fn, 'r', encoding='utf-8').readlines()]
    return result

def open_pkl(fn):
    """Load pickle"""
    with open(fn, 'rb') as f:
        data = pickle.load(f)
    return data

def map_name_subject(prediction_lst, monk_lst, monk_dict):
    """Add `monk_name` and `subject` to sentence_line as tuple in list

    Args:
      prediction_lst: label and Sentence separate by `\t`
      monk_lst: list of monk name
      monk_dict: dictionary that key is monk name, value contians its subject, text

    Returns:
      results_lst: tuple of list, tuple contains (monk_name, label, sentence_line)
    """
    result_lst = list()

    for line in prediction_lst:
        label, sentence_line = line.split('\t')

        if label == '0':
            continue

        if sentence_line[0] == '」' or sentence_line[0] == '』':
            sentence_line = sentence_line[1:]
    
        for name in monk_lst:
            # unpack `subject`, `volume`, `monk_txt_lst`
            subject, volume, *monk_txt_lst = monk_dict[name]
            monk_txt = ''.join(monk_txt_lst)
            
            if sentence_line in monk_txt:
                result_lst.append((name, subject, volume, label, sentence_line))
            
    return result_lst


def main():
    ### 1. Load monk_dict, load_lst ###
    song_monk_dict = open_pkl('./pkl/續高僧傳_monk_dict.pkl')
    song_monk_lst = open_pkl('./pkl/續高僧傳_monk_lst.pkl')

    ### 2. Load keyword ###
    kw_lst = load_items_from_file('./data_keyword/律學遊方.txt')

    ### 3. Load model prictions ###
    # line: label, sentence
    pred_lst = load_items_from_file('./results_inference/md_sent_line_tang-gaoseng-zhuan_plainText.txt')
    
    ### 4. Set write file ###
    write_fn = '律學_續高僧傳'

    ### 5. Add `monk_name` and `subject` ###
    # `name_label_sent_tuple_lst` is list of tuple
    # one tuple would like: (name, subject, label, sentence_line)
    name_label_sent_tuple_lst = map_name_subject(pred_lst, song_monk_lst, song_monk_dict)

    ### 5. dataframe ###
    df_dict = {'書目': [],
               '朝代': [],
               '科別': [],
               '卷數': [],
               '傳主': [],
               '文本敘述':[],
               '關鍵詞':[],
               '預測': []}
    
    ### 5. Match keywork and sentence_line & write file ###
    # match methods
    for name_label_sent_tuple in name_label_sent_tuple_lst:
        name, subject, volume, label, sentence_line = name_label_sent_tuple    
        for kw in kw_lst:
            if kw in sentence_line:

                df_dict['書目'].append('續高僧傳')
                df_dict['朝代'].append('唐')
                df_dict['科別'].append(subject)
                df_dict['卷數'].append(volume)
                df_dict['傳主'].append(name)
                df_dict['文本敘述'].append(sentence_line)
                df_dict['關鍵詞'].append(kw)
                df_dict['預測'].append(label)

    ### 6. to excel ###
    df = pd.DataFrame.from_dict(df_dict)
    df.to_excel(write_fn+'.xlsx', index=False)

if __name__ == '__main__':
    main()