#!/usr/bin/python

import sys


def parseYml(configfile='default.yml', appname='appname'):
    import yaml
    try:
        with open(configfile, 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg
    except IOError:  # FileNotFoundError
        if configfile == '-h' or configfile == '--help':
            print('Usage: %s [config-file]' % (appname))
            return {}
        elif configfile[:1] == '-':
            print('unknown argument')
            return {}
        else:
            print('Cannot access %s' % (configfile))
            return {}
    except (TypeError, AttributeError, yaml.scanner.ScannerError):
        msg = 'Unexpected yaml format: %s'
        print(msg % (configfile))
        return {}
    except KeyError:
        msg = 'The key %s is missing in %s'
        print(msg % (sys.exc_info()[1], configfile))
        return {}
