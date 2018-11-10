#!/usr/bin/python
import os
import gzip
import argparse

def processLog(srcFilePath, dstFilePath, domainFilterList=[], switchAnonymizeIp=False):
    if os.path.isfile(dstFilePath):
        raise OSError('File ' + dstFilePath + ' already exists.')

    with _openGzip(srcFilePath, 'r') as srcFile, open(dstFilePath, 'w') as dstFile:
        for lineNr,line in enumerate(srcFile):
            if _isRelevantLine(line, domainFilterList):
                line = _removeDomain(line)
                if switchAnonymizeIp: line = _anonymizeIp(line)
                dstFile.write(line)

def _openGzip(filePath, accessStr):
    if _isGzipFile(filePath):
        return gzip.open(filePath, accessStr)
    else:
        return open(filePath, accessStr)

def _isRelevantLine(line, domainFilterList):
    if _isWatchAllSet(domainFilterList):
        return True
    if _getDomain(line) in domainFilterList:
        return True
    return False

def _isGzipFile(filePath):
    return os.path.splitext(filePath)[1]=='.gz'

def _getDomain(str):
    return str.split(' ')[1]

def _isWatchAllSet(domainFilterList):
    return len(domainFilterList) == 0

def _removeDomain(str):
    split = str.split(' ', 2)
    return split[0] +' '+ split[2]

def _anonymizeIp(str):
    return '- ' + str.split(' ', 1)[1]

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('srcFilePath', help='log file to read and parse')
    argparser.add_argument('dstFilePath', help='output file, write target')
    argparser.add_argument('domainFilter', help='filter log entries for this domain name(s)', nargs='*')
    argparser.add_argument('-a', '--anonymizeIp', help='skip client\'s IP address', action='store_true')
    args = argparser.parse_args()
    processLog(args.srcFilePath, args.dstFilePath, args.domainFilter, args.anonymizeIp)
