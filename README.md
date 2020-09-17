# BackupJob
A python script [ziplogs.py](https://github.com/MarekPetr/BackupJob/blob/master/src/ziplogs.py) compresses regular files into gzip files.

### How it works
1. The script appends an ordinal number suffix (.#) to files or uses the existing one
2. Each file is then compressed into a `gzip` file with the same suffix and saved in the same directory
3. Original files are removed to free up drive space

### Usage
```
usage: ziplogs.py [-h] [-d LOG_DIR] [-s] [-nr]

optional arguments:
  -h, --help                  show this help message and exit
  -d LOG_DIR, --dir LOG_DIR   directory path of log files
  -s, --stats                 print statistics to stdout
  -nr, --non_recursive        do not compress files in subdirectories
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
* * * * *  ziplogs.py
```


To run the script first day of each month at 12:00, edit current crontab:
```sh
$ crontab -e
```

Then append the following entry:
```
 0 12 1 * * ziplogs.py
```

Save and close the file.