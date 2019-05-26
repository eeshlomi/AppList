#!/usr/bin/python

import sys
import os
from parseConf import parseYml


def parse_wmic_output(dir, files):
    for file in files:
        fullPath = dir+file
        with open(fullPath, encoding='utf-16-le') as f:
            next(f)  # skips the header
            for line in f:
                line = line.strip()
                if len(line) > 1:  # skips empty lines
                    print('%s, %s' % (line, file))
    return 0


def main(dir):
    files = filesIn(dir)
    return(parse_wmic_output(dir, files))


def filesIn(dir):
    result = []
    for r, d, f in os.walk(dir):
        for file in f:
            result.append(os.path.join(file))
    return result


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'AppList.yml'
        cfg = parseYml('AppList.yml', 'MakeCSV')
    if len(cfg):
        sys.exit(main(cfg['outputDir']))
