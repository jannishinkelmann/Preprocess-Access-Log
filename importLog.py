import os
import argparse
import processlog
import ConfigParser


def importlogdir(inputPath):
    if os.path.isfile(getTempFileName()):
        raise OSError('Cannot write temp file. File ' + getTempFileName() + ' already exists.')

    if os.path.isdir(inputPath):
        for file in os.listdir(inputPath):
            _importlog(inputPath)
    else:
        _importlog(inputPath)


def _importlog(inputPath):
    if os.path.isfile(inputPath):
        processlog.processLog(inputPath, getTempFileName(), getDomains(), getAnonymizeIp())
        os.remove(getTempFileName())


def getProcessScriptPath():
    return getconfig().get('importer', 'process_script_path')


def getImportScriptPath():
    return getconfig().get('importer', 'import_script_path')


def getDomains():
    configStr = getconfig().get('importer', 'domains').strip()
    domainList = str.split(configStr, ',')
    return domainList


def getAnonymizeIp():
    return getconfig().getboolean('importer', 'anonymize_ip')


def getTempFileName():
    return getconfig().get('importer', 'temp_file_name')


def getMatomoUrl():
    return getconfig().get('matomo', 'url')


def getMatomoUser():
    return getconfig().get('matomo', 'user')


def getMatomoPass():
    return getconfig().get('matomo', 'pass')


def getMatomoSiteId():
    return getconfig().get('matomo', 'site_id')


def getMatomoOptions():
    return getconfig().get('matomo', 'options')


__config = None

def getconfig():
    global __config

    if __config is None:
        __config = ConfigParser.ConfigParser()

        if os.path.isfile('settings.ini'):
            __config.read('settings.ini')
        else:
            raise OSError('settings.ini not found')

    return __config


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputPath', help='log file or dir of log files to import')
    args = argparser.parse_args()
    importlogdir(args.inputPath)
