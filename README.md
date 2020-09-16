# BackupJob
A python script [zipLogs.py](https://github.com/MarekPetr/BackupJob/blob/master/zipLogs.py) compresses regular files in the `/var/log` directory into gzip files.

### How it works?
    1. The script appends an ordinal number suffix (.#) to each file it compresses
    2. Each file is then compressed into a 'gzip' file with the same suffix and saved in the same directory 
    3. Original files are removed to preserve space

### About
* The script compresses regular files in every subdirectory in the root directory (e.g. `/var/log`)
* It suffixes a number regardless if the file already has one

### Usage
To compress files in the `/var/log` directory immediately:
```sh
$ python3 zipLogs.py
```
### Cron job
To run the script periodically, use `Cron Job` as follows:
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
│ │ │ │ │
│ │ │ │ │
* * * * *  command_to_execute
```


To run the script every month first edit current crontab:
```sh
$ crontab -e
```

Then append the following entry:
```
 12 1 \* \* \* zipLogs.py
```