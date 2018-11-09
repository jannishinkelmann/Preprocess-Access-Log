#!/usr/bin/python
import sys
import os
import gzip
import argparse

def processLog(outputFile, inputFile, domainName=[], anonymizeIp=False, zipfile=False):
    if os.path.isfile(outputFile):
        raise OSError('File ' + outputFile + ' already exists.')

    if zipfile:
        with gzip.open(inputFile,'r') as srcFile, open(outputFile, 'w') as dstFile:
            _processFile(srcFile, dstFile, domainName, anonymizeIp)
    else:
        with open(inputFile,'r') as srcFile, open(outputFile, 'w') as dstFile:
            _processFile(srcFile, dstFile, domainName, anonymizeIp)

def _anonymizeIp(str):
    return '- ' + str.split(' ', 1)[1]

def _removeDomainName(str):
    split = str.split(' ', 2)
    return split[0] +' '+ split[2]

def _getDomainName(str):
    return str.split(' ')[1]

def _isWatchAllSet(domainName):
    return len(domainName) == 0

def _isDomainToBeWatched(domain, domainName):
    return domain in domainName

def _processLine(line, dstFile, domainName, anonymizeIp):
    if _isDomainToBeWatched(_getDomainName(line), domainName) or _isWatchAllSet(domainName):
        str = _removeDomainName(line)
        if anonymizeIp: str = _anonymizeIp(str)
        dstFile.write(str)

def _processFile(srcFile, dstFile, domainName, anonymizeIp):
    line = srcFile.readline()
    lineNum = 1
    while line:
        _processLine(line, dstFile, domainName, anonymizeIp)
        line = srcFile.readline()
        lineNum += 1

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputFile', help='log file to read and parse')
    argparser.add_argument('outputFile', help='output file, write target')
    argparser.add_argument('domainName', help='domain(s) for which entries are filtered', nargs='*')
    argparser.add_argument('-a', '--anonymizeIp', help='skip client\'s IP address', action='store_true')
    argparser.add_argument('-z', '--zipfile', help='open Gzip input file', action='store_true')
    args = argparser.parse_args()
    processLog(args.outputFile, args.inputFile, args.domainName, args.anonymizeIp, args.zipfile)
