import unittest
import importlog
import os


class TestImportLog(unittest.TestCase):
    def test_readConfigFile(self):
        self.assertEqual(importlog.getProcessScriptPath(), './processlog.py')
        self.assertEqual(importlog.getImportScriptPath(), './matomo/misc/log-analytics/import_logs.py')
        self.assertEqual(importlog.getDomainListFromString('example.com    www.example.com '), ['example.com', 'www.example.com'])
        self.assertEqual(importlog.getDomains(), ['example.com', 'www.example.com'])
        self.assertTrue(importlog.getAnonymizeIp())
        self.assertEqual(importlog.getTempFileName(), 'access_log_tmp')
        self.assertEqual(importlog.getMatomoUrl(), 'https://analytics.example.com')
        self.assertEqual(importlog.getMatomoUser(), 'matomo_admin')
        self.assertEqual(importlog.getMatomoPass(), 'secret')
        self.assertEqual(importlog.getMatomoSiteId(), '1')
        self.assertEqual(importlog.getMatomoOptions(), '--enable-http-errors --enable-http-redirects --enable-static --enable-bots')

    def test_checkIfTmpFileExists(self):
        existingFilePath = os.path.join(os.path.dirname(__file__), 'access_log.example')
        notExistingFilePath = os.path.join(os.path.dirname(__file__), 'access_log_tmp.example')

        self.assertFalse(os.path.isfile(notExistingFilePath))
        self.assertFalse(importlog.checkIfTmpFileExists(notExistingFilePath))

        self.assertTrue(os.path.isfile(existingFilePath))
        self.assertRaises(OSError, importlog.checkIfTmpFileExists, existingFilePath)
