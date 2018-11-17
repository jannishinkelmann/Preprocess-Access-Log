import os
import argparse
import processlog
import ConfigParser


def getconfig():
    config = ConfigParser.ConfigParser()

    if os.path.isfile('settings.ini'):
        config.read('settings.ini')
    else:
        raise OSError('settings.ini not found')

    return config

    # getconfig().get('importer', 'process_script_path')
    # getconfig().get('importer', 'import_script_path')
    # str.split(',', getconfig().get('importer', 'domains'))
    # getconfig().getboolean('importer', 'anonymize_ip')
    # getconfig().get('importer', 'temp_file_name')
    # getconfig().get('matomo', 'url')
    # getconfig().get('matomo', 'user')
    # getconfig().get('matomo', 'pass')
    # getconfig().get('matomo', 'site_id')
    # getconfig().get('matomo', 'options')


def importlogdir(inputPath):
    if os.path.isfile(getconfig().get('importer', 'temp_file_name')):
        raise OSError('Cannot write temp file. File ' + getconfig().get('importer', 'temp_file_name') + ' already exists.')

    if os.path.isdir(inputPath):
        for file in os.listdir(inputPath):
            _importlog(inputPath)
    else:
        _importlog(inputPath)


def _importlog(inputPath):
    if os.path.isfile(inputPath):
        processlog.processLog(inputPath, getconfig().get('importer', 'temp_file_name'), str.split(',', getconfig().get('importer', 'domains')), getconfig().getboolean('importer', 'anonymize_ip'))
        os.remove(getconfig().get('importer', 'temp_file_name'))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputPath', help='log file or dir of log files to import')
    args = argparser.parse_args()
    importlogdir(args.inputPath)
