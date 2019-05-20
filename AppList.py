#!/usr/bin/python

__version__ = '1.0'

import sys
import traceback


def applist(node, cred):
    return node, cred


def auth(cred):
    cred_given = {}
    if cred['auth'] == 'SCRAM':
        import getpass
        passwd = getpass.getpass('Password for %s:' % (cred['user']))
        cred_given['user'] = cred['user']
        cred_given['passwd'] = passwd
    return cred_given


def main(cfg):
    cred = auth(cfg['credentials'])
    for node in cfg['nodes']:
        print(applist(node, cred))
    return 0


def parseYml(configfile='AppList.yml'):
    import yaml
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return main(cfg)
    except IOError:  # FileNotFoundError
        if configfile == '-h' or configfile == '--help':
            return 'Usage: AppList.py [config-file]'
        elif configfile[:1] == '-':
            return 'unknown argument'
        else:
            ''' We include function name to help identifying
            what type of file we can't access (config/log...)
            since it's inherited to the next functions'''
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb, 1)
            fname = stk[0][2]
            return '%s: File access error' % (fname)
    except (TypeError, yaml.scanner.ScannerError):
        mSubject = '%s is not a valid yml file'
        return mSubject % (configfile)
    except KeyError:
        mSubject = 'The key %s is missing in %s'
        return mSubject % (sys.exc_info()[1], configfile)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'AppList.yml'
    sys.exit(parseYml(configfile))
