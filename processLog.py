#!/usr/bin/python
# Custom Log parser
import sys
import os
import gzip
import argparse

def main():
    parseArguments()

    if os.path.isfile(args.outputFile):
        vPrint('Existence check of output file was positive. Break.')
        raise OSError('File ' + args.outputFile + ' already exists.')

    if args.zipfile:
        vPrint('Opening input (gzip) and output files.')
        with gzip.open(args.inputFile,'r') as srcFile, open(args.outputFile, 'w') as dstFile:
            processFile(srcFile, dstFile)
    else:
        vPrint('Opening input and output files.')
        with open(args.inputFile,'r') as srcFile, open(args.outputFile, 'w') as dstFile:
            processFile(srcFile, dstFile)

def vPrint(msg):
    if args.verbose: print(msg)

def anonymizeIp(str):
    return '- ' + str.split(' ', 1)[1]

def optAnonymizeIp(str):
    if args.anonymizeIp:
        vPrint('..Replace http client\'s IP address.')
        str = anonymizeIp(str)
    return str

def removeDomainName(str):
    vPrint('..Remove domain name.')
    split = str.split(' ', 2)
    return split[0] +' '+ split[2]

def getDomainName(str):
    return str.split(' ')[1]

def isWatchAllSet():
    return len(args.domainName) == 0

def isDomainToBeWatched(domain):
    return domain in args.domainName

def processLine(line, dstFile):
    if isDomainToBeWatched(getDomainName(line)) or isWatchAllSet():
        str = removeDomainName(line)
        str = optAnonymizeIp(str)
        vPrint('..Write Line to output file.')
        dstFile.write(str)

def processFile(srcFile, dstFile):
    vPrint('Begin reading input file.')
    line = srcFile.readline()
    lineNum = 1
    while line:
        vPrint('Read line %04d' % (lineNum,))
        processLine(line, dstFile)
        line = srcFile.readline()
        lineNum += 1

def parseArguments():
    global args
    argparser = argparse.ArgumentParser()
    argparser.add_argument('inputFile', help='log file to read and parse')
    argparser.add_argument('outputFile', help='output file, write target')
    argparser.add_argument('domainName', help='domain(s) for which entries are filtered', nargs='*')
    argparser.add_argument('-a', '--anonymizeIp', help='skip client\'s IP address', action='store_true')
    argparser.add_argument('-z', '--zipfile', help='open Gzip input file', action='store_true')
    argparser.add_argument('-v', '--verbose', help='run in verbose mode', action='store_true')
    args = argparser.parse_args()

args = 'global arguments'

main()
