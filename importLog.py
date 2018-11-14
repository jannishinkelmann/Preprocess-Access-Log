import os
import argparse
import configparser
import processlog


config = configparser.configparser()
if os.path.isfile('settings.ini'):
    config.read()
else:
    raise OSError('settings.ini not found')


PROCESS_SCRIPT_PATH = config.get('importer', 'process_script_path')
IMPORT_SCRIPT_PATH = config.get('importer', 'import_script_path')
DOMAINS = config.get('importer', 'domains')
ANONYMIZE_IP = config.get('importer', 'anonymize_ip')
TMP_FILE_NAME = config.get('importer', 'temp_file_name')
MATOMO_URL = config.get('matomo', 'url')
MATOMO_USER = config.get('matomo', 'user')
MATOMO_PASS = config.get('matomo', 'pass')
MATOMO_SITE_ID = config.get('matomo', 'site_id')
MATOMO_OPTIONS = config.get('matomo', 'options')


if os.path.isfile():
    raise OSError('Cannot write temp file. File ' + TMP_FILE_NAME + ' already exists.')


def importLog(input):
    if os.path.isdir(input):
        for file in os.listdir(input):
            processlog.processLog(file, TMP_FILE_NAME, DOMAINS, ANONYMIZE_IP)
    else:
        if os.path.isfile(input):
            processlog.processLog(input, TMP_FILE_NAME, DOMAINS, ANONYMIZE_IP)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input', help='log file or dir of log files to import')
    args = argparser.parse_args()
    importLog(args.input)
