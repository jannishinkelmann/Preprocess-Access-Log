# Preprocess-Access-Log
Preprocessing web server access.log files to have them compatible to standard format. Removes domain names and filters for specified domains e.g. when different sites are hosted on the same webserver.

Input logfile example:
```
91.156.15.9 www.example.com - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
207.46.13.155 www.other-site.com - - [06/Nov/2018:14:25:17 +0100] "GET / HTTP/1.0" 200 7818 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
91.156.15.9 analytics.example.com - - [06/Nov/2018:16:30:37 +0100] "POST /index.php?date=yesterday&filter_limit=-1&format=JSON2&idSite=1&method=API.getReportPagesMetadata&module=API&period=day HTTP/1.0" 200 36681 "https://analytics.example.com/index.php?module=CoreHome&action=index&idSite=1&period=day&date=yesterday" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```

Output logfile example:
```
91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
207.46.13.155 - - [06/Nov/2018:14:25:17 +0100] "GET / HTTP/1.0" 200 7818 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
91.156.15.9 - - [06/Nov/2018:16:30:37 +0100] "POST /index.php?date=yesterday&filter_limit=-1&format=JSON2&idSite=1&method=API.getReportPagesMetadata&module=API&period=day HTTP/1.0" 200 36681 "https://analytics.example.com/index.php?module=CoreHome&action=index&idSite=1&period=day&date=yesterday" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
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
Read all lines from access_log.example, remove domain names and write to access_log_cleared. Output format as showed in example above.
```
$ python processLog.py access_log.example access_log_cleared
```
### 2. Gzip compressed files:
Files with extention .gz will be decompressed automatically and then parsed. Output format as showed in example above.
```
$ python processLog.py access_log_2018_w45-1.gz access_log_cleared
```
### 3. Remove client IP addresses
Use option -a to also remove the IP addresses of clients from log entries and replace them with '-'.
```
$ python processLog.py -a access_log.example access_log_cleared
```
With the input log file from first example this will result in the following output in access_log_cleared:
```
- - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
- - - [06/Nov/2018:14:25:17 +0100] "GET / HTTP/1.0" 200 7818 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
- - - [06/Nov/2018:16:30:37 +0100] "POST /index.php?date=yesterday&filter_limit=-1&format=JSON2&idSite=1&method=API.getReportPagesMetadata&module=API&period=day HTTP/1.0" 200 36681 "https://analytics.example.com/index.php?module=CoreHome&action=index&idSite=1&period=day&date=yesterday" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```
### 4. Filter for specific domains
Add domain names to filter log entries. access_log_cleared will now just include entries for these specific domains.
```
$ python processLog.py access_log.example access_log_cleared example.com www.example.com
```
With the input log file from first example this will result in the following output in access_log_cleared:
```
91.156.15.9 - - [06/Nov/2018:13:40:45 +0100] "GET / HTTP/1.0" 200 8108 "http://google.de" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15"
```
Notice that the third entry will not be included although analytics is a subdomain of example.com.

## Matomo integration
The output format then may be imported to your Matomo server (https://matomo.org) via matomo-log-analytics (https://github.com/matomo-org/matomo-log-analytics, https://matomo.org/log-analytics/).

