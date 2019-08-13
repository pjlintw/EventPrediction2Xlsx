import os
from pathlib import Path

def segmentor(text):
    """Split text into setenses
    
    Args:
      text: string of text

    Return:
      sentences_lst: list contains all sentences from text

    """
    # all sentecnes
    sentences_lst = list()  
    # collect charater to make sentence
    char_collector = list()
    # collect writing symbol for counting
    writing_start_lst = list()
    writing_end_lst = list()

    continue_writing = False
    for char in text:
        
        if len(writing_start_lst) == len(writing_end_lst):
            continue_writing = False
        else:
            continue_writing = True

        # append sentence if sentence finised and not writing anymore
        if char in ['。', '？', '！']:
            char_collector += char

            if continue_writing:
                continue
            # not writing, then append sentence
            else:
                # append sentence
                sentences_lst.append(''.join(char_collector))
                # reset sentence
                char_collector = list()
                writing_lst = list()
                writing_start_lst = list()
                writing_end_lst = list()

        # append punctuation mark of writing
        elif char in [ '「', '《', '〈', '（', '『','〈', '(']:
            char_collector += char
            #writing_lst.append(char)
            writing_start_lst.append(char)

        # append punctuation mark of writing        
        elif char in ['」', '》', '〉', '）', '』', '〉', ')']:
            char_collector += char
            writing_end_lst.append(char)

        else:
            char_collector += char

    return sentences_lst

def line_segmentor(text):
    """Segmente text, if text not contain punctuation

    """
    text_lst = [ i for i in text.split('\n') if i !='']
    return text_lst

def main():
    data_dir = './data_plainText'
    data_to_dir = './to'

    for fn in os.listdir(data_dir):

        text = Path(data_dir, fn).open('r',encoding='utf-8').readlines()
        text = ''.join([ l for l in text if l != '\n'])

        text_lst = segmentor(text)

        if len(text_lst) == 0:
            text_lst = line_segmentor(text)

        with Path(data_to_dir, f'sent_line_{fn}').open('w', encoding='utf-8') as f:
            for l in text_lst:
                f.write(l.strip()+'\n')


        


if __name__ == '__main__':
    main()