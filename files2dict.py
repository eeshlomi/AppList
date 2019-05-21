#!/usr/bin/python


def parse_wmic_output(dir, files, ext):
    result = {}
    for file in files:
        file = dir+file+ext
        print(file)
        with open(file, encoding='utf-16-le') as f:
            next(f)  # to skip the header
            for line in f:
                line = line.strip()
                if len(line) > 1:
                    try:
                        result[line].append('b')
                    except KeyError:
                        result[line] = ['a']
    return result


if __name__ == '__main__':
    dir = 'C:\\temp\\'
    files = ['test1', 'test2']
    ext = '.0'
    print(parse_wmic_output(dir, files, ext))
