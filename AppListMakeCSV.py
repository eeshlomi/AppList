#!/usr/bin/python

import sys
import traceback
import os


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


def parseYml(configfile='AppList.yml'):
    import yaml
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return main(cfg['outputDir'])
    except IOError:  # FileNotFoundError
        if configfile == '-h' or configfile == '--help':
            return 'Usage: AppList.py [config-file]'
        elif configfile[:1] == '-':
            return 'unknown argument'
        else:
            ''' We include function name to help identifying
            what kind of file can't be accessed (config/log...)
            since it's also invoked by the nesting functions '''
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb, 1)
            fname = stk[0][2]
            return '%s: File access error' % (fname)
    except (TypeError, yaml.scanner.ScannerError):
        msg = '%s is not a valid yml file'
        return msg % (configfile)
    except KeyError:
        msg = 'The key %s is missing in %s'
        return msg % (sys.exc_info()[1], configfile)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'AppList.yml'
    sys.exit(parseYml(configfile))
