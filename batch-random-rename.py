from os import getcwd, chdir, listdir, rename, remove
from random import seed, randint
from sys import argv, exit
from re import match

seed()

def is_indexed(prefix, files):
    for f in files:
        if match(prefix + '_[0-9]+', f):
            return True
    return False

def split_audio(files):
    audio = filter(lambda x: x.split('.')[-1] == 'wav', files)
    util = filter(lambda x: x.split('.')[-1] != 'wav', files)
    return (audio, util)

def del_util_files(files):
    for f in files:
        remove(f)

def split_indexed(prefix, files):
    indexed = []
    not_indexed = []
    audio, util = split_audio(files)

    del_util_files(util)

    for f in audio:
        if match(prefix + '_[0-9]+', f):
            indexed.append(f)
        else:
            not_indexed.append(f)
    return (indexed, not_indexed)

def index_files(prefix, start_val, files):
    i = len(files)
    max_zeroes = len(str(i))

    while i > 0:
        index = str(i + start_val).rjust(max_zeroes, '0')
        file = files.pop(randint(0, i-1))
        ext = file.split('.')[-1]
        rename(file, prefix + '_' + index + '.' + ext.lower())
        i -= 1

def main():
    try:
        cwd = getcwd() + '\\' + argv[1]
        prefix = argv[2]
    except:
        print('Too few arguments')
        exit(-1)

    try:
        chdir(cwd)
    except:
        print(argv[1] + 'is no valid dir')
        exit(-2)

    indexed, not_indexed = split_indexed(prefix, listdir(cwd))

    if len(not_indexed) == 0:
        print('Nothing to do.')
        exit(1)
    elif len(indexed) == 0:
        index_files(prefix, 0, not_indexed)

    else:
        last_index = int(indexed[-1].split('_')[1])
        index_files(prefix, last_index, not_indexed)

if __name__ == '__main__':
    main()