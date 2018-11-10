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
$ python processLog.py [-h] [-a] srcFilePath dstFilePath [domainFilter [domainFilter ...]]

positional arguments:
  srcFilePath        log file to read and parse
  dstFilePath        output file, write target
  domainFilter       filter log entries for this domain name(s)

optional arguments:
  -h, --help         show this help message and exit
  -a, --anonymizeIp  skip client's IP address
```
## Examples:
### 1. Basic:
Read all lines from access_log.example, remove domain names and write to access_log_cleared.
```
$ python processLog.py access_log.example access_log_cleared
```
### 2. Gzip compressed files:
Files with extention .gz will be decompressed automatically and then parsed.
```
$ python processLog.py access_log_2018_w45-1.gz access_log_cleared
```
### 3. Remove client IP addresses
Use option -a to also remove the IP addresses of clients from log entries and replace them with '-'.
```
$ python processLog.py -a access_log.example access_log_cleared
```
This will result in the following output in access_log_cleared:
```
- - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```
## Matomo integration
The output format then may be imported to your Matomo server (https://matomo.org) via matomo-log-analytics (https://github.com/matomo-org/matomo-log-analytics, https://matomo.org/log-analytics/).

