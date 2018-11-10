import unittest
import processlog
import os


class TestProcessLog(unittest.TestCase):
    def test_anonymizeIp(self):
        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '- www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._anonymizeIp(logEntry)
        self.assertEqual(result, expected)

        logEntry = '- www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '- www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._anonymizeIp(logEntry)
        self.assertEqual(result, expected)

        logEntry = '0.0.0.0 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '- www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._anonymizeIp(logEntry)
        self.assertEqual(result, expected)

    def test_removeDomain(self):
        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._removeDomain(logEntry)
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._removeDomain(logEntry)
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._removeDomain(logEntry)
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._removeDomain(processlog._removeDomain(logEntry))
        self.assertEqual(result, expected)

    def test_removeDomain_anonymizeIp(self):
        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '- - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._removeDomain(processlog._anonymizeIp(logEntry))
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = '- - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        result = processlog._anonymizeIp(processlog._removeDomain(logEntry))
        self.assertEqual(result, expected)

    def test_isWatchAllSet(self):
        self.assertTrue(processlog._isWatchAllSet())
        self.assertTrue(processlog._isWatchAllSet([]))
        self.assertFalse(processlog._isWatchAllSet(['example.com']))

    def test_getDomain(self):
        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = 'www.example.com'
        result = processlog._getDomain(logEntry)
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = 'example.com'
        result = processlog._getDomain(logEntry)
        self.assertEqual(result, expected)

        logEntry = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        expected = ''
        result = processlog._getDomain(logEntry)
        self.assertEqual(result, expected)

    def test_isGzipFile(self):
        self.assertFalse(processlog._isGzipFile('.gz'))
        self.assertFalse(processlog._isGzipFile('bla.somegz'))
        self.assertTrue(processlog._isGzipFile('bla.gz'))
        self.assertTrue(processlog._isGzipFile('some.bla.gz'))
        self.assertTrue(processlog._isGzipFile('path/to/bla.gz'))

    def test_isRelevantLine(self):
        logEntry = '91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        self.assertTrue(processlog._isRelevantLine(logEntry, []))
        self.assertTrue(processlog._isRelevantLine(logEntry, ['www.example.com']))
        self.assertFalse(processlog._isRelevantLine(logEntry, ['other-domain.com']))
        self.assertFalse(processlog._isRelevantLine(logEntry, ['example.com']))
        self.assertFalse(processlog._isRelevantLine(logEntry, ['sub.example.com']))
        self.assertTrue(processlog._isRelevantLine(logEntry, ['www.example.com', 'example.com']))
        self.assertTrue(processlog._isRelevantLine(logEntry, ['example.com', 'www.example.com']))

        logEntry = '91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"'
        self.assertTrue(processlog._isRelevantLine(logEntry, []))
        self.assertTrue(processlog._isRelevantLine(logEntry, ['www.example.com']))
        self.assertTrue(processlog._isRelevantLine(logEntry, ['www.example.com', 'example.com']))

    def test_openGzip(self):
        basePath = os.path.dirname(__file__)
        unzipedFilePath = os.path.join(basePath, 'access_log.example')
        gzipedFilePath = os.path.join(basePath, 'access_log.example.gz')

        refFile = open(unzipedFilePath, 'r')
        probeFile = processlog._openGzip(unzipedFilePath, 'r')
        self.assertEqual(refFile.read(), probeFile.read())

        unzipedFilePath = os.path.join(os.path.dirname(__file__), 'access_log.example')
        gzipedFilePath = os.path.join(os.path.dirname(__file__), 'access_log.example.gz')
        refFile = open(unzipedFilePath, 'r')
        probeFile = processlog._openGzip(gzipedFilePath, 'r')
        self.assertEqual(refFile.read(), probeFile.read())

    def test_processLog(self):
        basePath = os.path.dirname(__file__)
        unzipedFilePath = os.path.join(basePath, 'access_log.example')
        gzipedFilePath = os.path.join(basePath, 'access_log.example.gz')
        targetFilePath = os.path.join(basePath, 'access_log_cleared')

        self.assertRaises(TypeError, processlog.processLog, unzipedFilePath)

        processlog.processLog(unzipedFilePath, targetFilePath)
        self.assertTrue(os.path.isfile(targetFilePath))
        targetFile = open(targetFilePath, 'r')
        self.assertEqual(len(targetFile.read().splitlines()), 8)
        self.assertRaises(OSError, processlog.processLog, unzipedFilePath, targetFilePath)
        os.remove(targetFilePath)

        processlog.processLog(unzipedFilePath, targetFilePath, [])
        targetFile = open(targetFilePath, 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 8)
        self.assertFalse('www.example.com' in content)
        os.remove(targetFilePath)

        processlog.processLog(unzipedFilePath, targetFilePath, ['www.example.com'])
        targetFile = open(targetFilePath, 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 5)
        self.assertFalse('207.46.13.88' in content)
        self.assertTrue('213.186.1.206' in content)
        os.remove(targetFilePath)

        processlog.processLog(unzipedFilePath, targetFilePath, [], True)
        targetFile = open(targetFilePath, 'r')
        content = targetFile.read()
        self.assertEqual(len(content.splitlines()), 8)
        self.assertFalse('207.46.13.88' in content)
        self.assertFalse('213.186.1.206' in content)
        os.remove(targetFilePath)

        processlog.processLog(gzipedFilePath, targetFilePath)
        self.assertTrue(os.path.isfile(targetFilePath))
        targetFile = open(targetFilePath, 'r')
        self.assertEqual(len(targetFile.read().splitlines()), 8)
        self.assertRaises(OSError, processlog.processLog, gzipedFilePath, targetFilePath)
        os.remove(targetFilePath)
