# Preprocess-Access-Log
Preprocessing web server access.log files to have them compatible to standard format. Removes domain names and filters for specified domains e.g. when different sites are hosted on the same webserver.

Input logfile format:
```
91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```

Output logfile format:
```
91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```

## Usage:
```
$ python processLog.py [-h] [-a]
                     srcFilePath dstFilePath [domainName [domainName ...]]

positional arguments:
  srcFilePath        log file to read and parse
  dstFilePath        output file, write target
  domainName         domain(s) for which entries are filtered

optional arguments:
  -h, --help         show this help message and exit
  -a, --anonymizeIp  skip client's IP address
```
## Matomo integration
The output format then may be imported to your Matomo server (https://matomo.org) via matomo-log-analytics (https://github.com/matomo-org/matomo-log-analytics, https://matomo.org/log-analytics/).

