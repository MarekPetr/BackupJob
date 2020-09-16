# BackupJob
A python script 'zipLogs.py' compresses files in the '/var/log' directory into a gzip file.

### How it works?
    1. The script appends an ordinal number suffix (.#) to each file it compresses
    2. That file is then compressed into a 'gzip' file with the same suffix
    3. The original file is removed to preserve space

### About
* The script runs recursively for every subdirectory in the root directory (e.g. '/var/log')
* It suffixes a number regardless if the file already has one
* 

### Usage
To compress files in '/var/log' directory immediately:
```sh
python3 zipLogs.py'
```
### Cron job
Cron job syntax:
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
│ │ │ │ │                                       7 is also Sunday on some systems)
│ │ │ │ │
│ │ │ │ │
\* \* \* \* \*  command_to_execute


To run the script every month first edit current crontab:
```sh
crontab -e
```

Then append the following entry:
```
 12 1 \* \* \* zipLogs.py
```