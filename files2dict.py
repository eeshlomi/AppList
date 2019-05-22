#!/usr/bin/python


def parse_wmic_output(dir, files, ext):
    result = {}
    for file in files:
        fullPath = dir+file+ext
        with open(fullPath, encoding='utf-16-le') as f:
            next(f)  # to skip the header
            for line in f:
                line = line.strip()
                if len(line) > 1:
                    try:
                        result[line].append(file)
                    except KeyError:
                        result[line] = [file]
    return result


if __name__ == '__main__':
    dir = 'C:\\temp\\'
    files = ['adrian', 'shlomi']
    ext = '.0'
    print(parse_wmic_output(dir, files, ext))
