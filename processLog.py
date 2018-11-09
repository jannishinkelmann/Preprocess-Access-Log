#!/usr/bin/python
import sys
import os
import gzip
import argparse

def processLog(srcFilePath, dstFilePath, domainFilterList=[], switchAnonymizeIp=False):
    if os.path.isfile(dstFilePath):
        raise OSError('File ' + dstFilePath + ' already exists.')

    srcFile = _getFile(srcFilePath)

    with open(dstFilePath, 'w') as dstFile:
        line = srcFile.readline()
        lineNum = 1
        while line:
            if _isRelevantLine(line, domainFilterList): _processLine(line, dstFile, switchAnonymizeIp)
            line = srcFile.readline()
            lineNum += 1

def _getFile(filePath):
    if _isGzipFile(filePath):
        return gzip.open(filePath,'r')
    else:
        return open(filePath,'r')

def _isRelevantLine(line, domainFilterList):
    if _isWatchAllSet(domainFilterList):
        return true
    if _getDomain(line) in domainFilterList:
        return true

def _processLine(line, dstFile, switchAnonymizeIp):
    str = _removeDomain(line)
    if switchAnonymizeIp: str = _anonymizeIp(str)
    dstFile.write(str)

def _isGzipFile(filePath):
    return os.path.splitext(filePath)[1]=='.gz'

def _getDomain(str):
    return str.split(' ')[1]

def _isWatchAllSet(domainFilterList):
    return len(domainFilterList) == 0

def _removedomain(str):
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
