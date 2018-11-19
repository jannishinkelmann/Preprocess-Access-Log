import os
import argparse
import processlog
import ConfigParser


def importlogdir(inputPath):
    checkIfTmpFileExists(getTempFileName())

    if os.path.isdir(inputPath):
        for file in os.listdir(inputPath):
    else:
        _importlog(inputPath)


def _importlog(inputPath):
    if os.path.isfile(inputPath):
        processlog.processLog(inputPath, getTempFileName(), getDomains(), getAnonymizeIp())
        os.system("{} --url={} --login={} --password={} --idsite={} {} {}".format(getImportScriptPath(), getMatomoUrl(), getMatomoUser(), getMatomoPass(), getMatomoSiteId(), getMatomoOptions(), getTempFileName()))
        os.remove(getTempFileName())


def checkIfTmpFileExists(tempFileName):
    if os.path.isfile(tempFileName):
        raise OSError('Cannot write temp file. File ' + tempFileName + ' already exists.')


def getProcessScriptPath():
    return getconfig().get('importer', 'process_script_path')


def getImportScriptPath():
    return getconfig().get('importer', 'import_script_path')


def getDomainListFromString(str):
    list = str.split(' ')
    return filter(None, list)


def getDomains():
    configStr = getconfig().get('importer', 'domains')
    return getDomainListFromString(configStr)


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
    configFilePath = os.path.join(os.path.dirname(__file__), 'settings.ini')

    if __config is None:
        __config = ConfigParser.ConfigParser()

        if os.path.isfile(configFilePath):
            __config.read(configFilePath)
        else:
            raise OSError('Settings file not found at ' + configFilePath)

    return __config


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputPath', help='log file or dir of log files to import')
    args = argparser.parse_args()
    importlogdir(args.inputPath)
