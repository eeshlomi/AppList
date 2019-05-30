#!/usr/bin/python

__version__ = '1.0'

import sys
import os
from parseConf import parseYml


def applist(nodeName, nodeIP, cred, outputDir):
    cmd = ("wmic /output:'%s%s' /user:%s /password:'%s' /node:'%s' "
           "product get name"
           % (outputDir, nodeName, cred['user'], cred['passwd'], nodeIP))
    wmic_output = os.popen(cmd).read()
    return wmic_output


def applistLocal(nodeName, nodeIP, outputDir):
    cmd = ("wmic /output:'%s%s' /node:'%s' "
           "product get name"
           % (outputDir, nodeName, nodeIP))
    wmic_output = os.popen(cmd).read()
    return wmic_output


def auth(cred):
    cred_given = {'user': cred['user']}
    if cred['auth'] == 'SCRAM':
        import getpass
        passwd = getpass.getpass('Password for %s:' % (cred['user']))
        cred_given['passwd'] = passwd
    else:
        print('WARNING: password is stored in the config file. '
              'Please use SCRAM instead')
        cred_given['passwd'] = cred['auth']
    return cred_given


def main(cfg):
    cred = auth(cfg['credentials'])
    if cfg['localNode'] is not None:
        for nodeName, nodeIP in cfg['localNode'].items():
            print(nodeName)
            print(applistLocal(nodeName, nodeIP, cfg['outputDir']))
    if cfg['remoteNodes'] is not None:
        for node in cfg['remoteNodes']:
            for nodeName, nodeIP in node.items():
                print(nodeName)
                print(applist(nodeName, nodeIP, cred, cfg['outputDir']))
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 2:
        configfile = '--help'
    elif len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile = 'AppList.yml'
    cfg = parseYml(configfile, 'AppList')
    if len(cfg):
        sys.exit(main(cfg))
