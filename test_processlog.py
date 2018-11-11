import unittest
import processlog
import os


class TestProcessLog(unittest.TestCase):
    @staticmethod
    def getTestLogEntry():
        return '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestLogEntryDashedIp():
        return '- www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestLogEntryZeroedIp():
        return '0.0.0.0 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestLogEntryRemovedDomain():
        return '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestLogEntryWithoutWww():
        return '91.156.15.9 example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestLogEntryDashedIpRemovedDomain():
        return '- - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'

    @staticmethod
    def getTestUnzipedFilePath():
        return os.path.join(os.path.dirname(__file__), 'access_log.example')

    @staticmethod
    def getTestGzipedFilePath():
        return os.path.join(os.path.dirname(__file__), 'access_log.example.gz')

    @staticmethod
    def getTestTargetFilePath():
        return os.path.join(os.path.dirname(__file__), 'access_log_cleared')

    def test_anonymizeIp(self):
        result = processlog._anonymizeIp(self.getTestLogEntry())
        self.assertEqual(result, self.getTestLogEntryDashedIp())

        result = processlog._anonymizeIp(self.getTestLogEntryDashedIp())
        self.assertEqual(result, self.getTestLogEntryDashedIp())

        result = processlog._anonymizeIp(self.getTestLogEntryZeroedIp())
        self.assertEqual(result, self.getTestLogEntryDashedIp())

    def test_removeDomain(self):
        result = processlog._removeDomain(self.getTestLogEntry())
        self.assertEqual(result, self.getTestLogEntryRemovedDomain())

        result = processlog._removeDomain(self.getTestLogEntryWithoutWww())
        self.assertEqual(result, self.getTestLogEntryRemovedDomain())

        result = processlog._removeDomain(self.getTestLogEntryRemovedDomain())
        self.assertEqual(result, self.getTestLogEntryRemovedDomain())

    def test_removeDomain_anonymizeIp(self):
        result = processlog._removeDomain(processlog._anonymizeIp(self.getTestLogEntry()))
        self.assertEqual(result, self.getTestLogEntryDashedIpRemovedDomain())

        result = processlog._anonymizeIp(processlog._removeDomain(self.getTestLogEntry()))
        self.assertEqual(result, self.getTestLogEntryDashedIpRemovedDomain())

    def test_isWatchAllSet(self):
        self.assertTrue(processlog._isWatchAllSet())
        self.assertTrue(processlog._isWatchAllSet([]))
        self.assertFalse(processlog._isWatchAllSet(['example.com']))

    def test_getDomain(self):
        result = processlog._getDomain(self.getTestLogEntry())
        self.assertEqual(result, 'www.example.com')

        result = processlog._getDomain(self.getTestLogEntryWithoutWww())
        self.assertEqual(result, 'example.com')

        result = processlog._getDomain(self.getTestLogEntryDashedIpRemovedDomain())
        self.assertEqual(result, '')

    def test_isGzipFile(self):
        self.assertFalse(processlog._isGzipFile('.gz'))
        self.assertFalse(processlog._isGzipFile('bla.somegz'))
        self.assertTrue(processlog._isGzipFile('bla.gz'))
        self.assertTrue(processlog._isGzipFile('some.bla.gz'))
        self.assertTrue(processlog._isGzipFile('path/to/bla.gz'))

    def test_isRelevantLine(self):
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntry(), []))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntry(), ['www.example.com']))
        self.assertFalse(processlog._isRelevantLine(self.getTestLogEntry(), ['other-domain.com']))
        self.assertFalse(processlog._isRelevantLine(self.getTestLogEntry(), ['example.com']))
        self.assertFalse(processlog._isRelevantLine(self.getTestLogEntry(), ['sub.example.com']))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntry(), ['www.example.com', 'example.com']))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntry(), ['example.com', 'www.example.com']))

        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryDashedIp(), ['www.example.com']))
        self.assertFalse(processlog._isRelevantLine(self.getTestLogEntryDashedIp(), ['other-domain.com']))

        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryRemovedDomain(), []))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryRemovedDomain(), ['other-domain.com']))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryRemovedDomain(), ['www.example.com', 'example.com']))

        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryDashedIpRemovedDomain(), []))
        self.assertTrue(processlog._isRelevantLine(self.getTestLogEntryDashedIpRemovedDomain(), ['other-domain.com']))

    def test_openGzip(self):
        refFile = open(self.getTestUnzipedFilePath(), 'r')
        refContent = refFile.read()
        probeFile = processlog._openGzip(self.getTestUnzipedFilePath(), 'r')
        self.assertEqual(refContent, probeFile.read())

        gzipedLogFile = processlog._openGzip(self.getTestGzipedFilePath(), 'r')
        self.assertEqual(refContent, gzipedLogFile.read())

    def test_processLog(self):
        self.assertRaises(TypeError, processlog.processLog, self.getTestUnzipedFilePath())

        processlog.processLog(self.getTestUnzipedFilePath(), self.getTestTargetFilePath())
        self.assertTrue(os.path.isfile(self.getTestTargetFilePath()))
        targetFile = open(self.getTestTargetFilePath(), 'r')
        self.assertEqual(len(targetFile.read().splitlines()), 8)
        self.assertRaises(OSError, processlog.processLog, self.getTestUnzipedFilePath(), self.getTestTargetFilePath())
        os.remove(self.getTestTargetFilePath())

        processlog.processLog(self.getTestUnzipedFilePath(), self.getTestTargetFilePath(), [])
        targetFile = open(self.getTestTargetFilePath(), 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 8)
        self.assertFalse('www.example.com' in content)
        os.remove(self.getTestTargetFilePath())

        processlog.processLog(self.getTestUnzipedFilePath(), self.getTestTargetFilePath(), ['www.example.com'])
        targetFile = open(self.getTestTargetFilePath(), 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 5)
        self.assertFalse('207.46.13.88' in content)
        self.assertTrue('213.186.1.206' in content)
        os.remove(self.getTestTargetFilePath())

        processlog.processLog(self.getTestUnzipedFilePath(), self.getTestTargetFilePath(), [], True)
        targetFile = open(self.getTestTargetFilePath(), 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 8)
        self.assertFalse('207.46.13.88' in content)
        self.assertFalse('213.186.1.206' in content)
        os.remove(self.getTestTargetFilePath())

        processlog.processLog(self.getTestGzipedFilePath(), self.getTestTargetFilePath())
        self.assertTrue(os.path.isfile(self.getTestTargetFilePath()))
        targetFile = open(self.getTestTargetFilePath(), 'r')
        self.assertEqual(len(targetFile.read().splitlines()), 8)
        self.assertRaises(OSError, processlog.processLog, self.getTestGzipedFilePath(), self.getTestTargetFilePath())
        os.remove(self.getTestTargetFilePath())
