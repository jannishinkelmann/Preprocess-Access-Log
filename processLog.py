#!/usr/bin/python
import sys
import os
import gzip
import argparse

def processLog(srcFilePath, dstFilePath, domainName=[], anonymizeIp=False):
    if os.path.isfile(dstFilePath):
        raise OSError('File ' + dstFilePath + ' already exists.')

    if _isGzipFile(srcFilePath):
        srcFile = gzip.open(srcFilePath,'r')
    else:
        srcFile = open(srcFilePath,'r')

    with open(dstFilePath, 'w') as dstFile:
        line = srcFile.readline()
        lineNum = 1
        while line:
            _processLine(line, dstFile, domainName, anonymizeIp)
            line = srcFile.readline()
            lineNum += 1

def _isGzipFile(filePath):
    return os.path.splitext(filePath)[1]=='.gz'

def _processLine(line, dstFile, domainName, anonymizeIp):
    if _isDomainToBeWatched(_getDomainName(line), domainName) or _isWatchAllSet(domainName):
        str = _removeDomainName(line)
        if anonymizeIp: str = _anonymizeIp(str)
        dstFile.write(str)

def _isDomainToBeWatched(domain, domainName):
    return domain in domainName

def _getDomainName(str):
    return str.split(' ')[1]

def _isWatchAllSet(domainName):
    return len(domainName) == 0

def _removeDomainName(str):
    split = str.split(' ', 2)
    return split[0] +' '+ split[2]

def _anonymizeIp(str):
    return '- ' + str.split(' ', 1)[1]

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('srcFilePath', help='log file to read and parse')
    argparser.add_argument('dstFilePath', help='output file, write target')
    argparser.add_argument('domainName', help='domain(s) for which entries are filtered', nargs='*')
    argparser.add_argument('-a', '--anonymizeIp', help='skip client\'s IP address', action='store_true')
    args = argparser.parse_args()
    processLog(args.srcFilePath, args.dstFilePath, args.domainName, args.anonymizeIp)
