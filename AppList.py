#!/usr/bin/python

__version__ = '1.0'

import sys
import traceback
import os


def applist(nodeName, nodeIP, cred, csvDir):
    cmd = ("wmic /output:%s%s.csv /user:%s /password:'%s' /node:'%s' "
           "product get name,version"
           % (csvDir, nodeName, cred['user'], cred['passwd'], nodeIP))
    wmic_output = os.popen(cmd).read()
    return wmic_output
    return 0


def auth(cred):
    cred_given = {'user': cred['user']}
    if cred['auth'] == 'SCRAM':
        import getpass
        passwd = getpass.getpass('Password for %s:' % (cred['user']))
        cred_given['passwd'] = passwd
    else:
        cred_given['passwd'] = cred['auth']
    return cred_given


def main(cfg):
    cred = auth(cfg['credentials'])
    for node in cfg['nodes']:
        for nodeName, nodeIP in node.items():
            print(nodeName)
            print(applist(nodeName, nodeIP, cred, cfg['csvDir']))
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
            what kind of file can't be accessed (config/log...)
            since it's also invoked by the nesting functions '''
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
