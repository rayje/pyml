from pandas import DataFrame
import numpy as np
import os

NEWLINE = '\n'
SKIP_FILES = {'cmds'}
HAM = 'ham'
SPAM = 'spam'

SOURCES = [
    ('data/spam', SPAM),
    ('data/easy_ham', HAM),
    ('data/hard_ham', HAM),
    ('data/beck-s', HAM),
    ('data/farmer-d', HAM),
    ('data/kaminski-v', HAM),
    ('data/kitchen-l', HAM),
    ('data/lokay-m', HAM),
    ('data/williams-w3', HAM),
    ('data/BG', SPAM),
    ('data/GP', SPAM),
    ('data/SH', SPAM)
]

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    past_header, lines = False, []
                    with open(file_path, encoding="latin-1") as f:
                        for line in f:
                            if past_header:
                                lines.append(line)
                            elif line == NEWLINE:
                                past_header = True
                    content = NEWLINE.join(lines)
                    yield file_path, content

def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text':text,'class':classification})
        index.append(file_name)

    return DataFrame(rows, index=index)

if __name__ == '__main__':
    data = DataFrame({'text':[], 'class':[]})
    for path, classification in SOURCES:
        data = data.append(build_data_frame(path, classification))
    data = data.reindex(np.random.permutation(data.index))
