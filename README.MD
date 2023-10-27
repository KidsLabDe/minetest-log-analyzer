# Minetest-Log-Analyzer & Telegram Bot

## How to install

### 1. Install the python libraries

```
pip install -r requirements.txt
```

### 2. Get a Telegram Bot and put it in config

Get the Bot-Token and the Chat-ID and put it in a config.py file (see config.py.sample)

### 3. set the logs dir.

Set it to the right dir in config.py

### (optional) Add it to your cron

```
* * * * * /usr/bin/python3 /opt/minetest/minetest-log-analyzer/log-analyzer.py --telegram
```

## Usage


### Normal usage

```
python3 log-analyzer.py
```

Output:

```
Log file: logs/22.log
+--------+------+--------+-------+
|  User  | Digs | Places | Total |
+--------+------+--------+-------+
| marita | 399  |  716   |  1115 |
|  Lene  | 319  |  2787  |  3106 |
| Luisa  | 2382 |  3227  |  5609 |
| Heidi  | 7077 | 12127  | 19204 |
+--------+------+--------+-------+
Chat messages:
<Heidi> Lene, schau dir mal den Eingang zum Bahnhof an
<Heidi> um was zu schreiben musst du auf t drücken
```

### Telegram-Mode

```
python3 log-analyzer.py --telegram
```


### Reset, parse again

```
python3 log-analyzer.py --reset
```

### Choose the logdir

You have many instances? 
Pick your logdir via CLI:

```
python3 log-analyzer.py --logdir /opt/minetest/logs
```



Have fun :-)

