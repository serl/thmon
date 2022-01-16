# thmon


## Installation

On a Raspberry Pi:

```sh
# Install system dependencies
sudo apt-get install libgpiod2

# Use prepare and load the venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
CFLAGS="-fcommon" pip install -r requirements.txt
```


## Usage

Activate the venv with `source .venv/bin/activate`, then run `python dht22_read.py`.
It wîll try to read the values from the sensor, gives 'TEMP HUMIDITY' on stdout and some debug data on stderr.


## Pushing to ThingSpeak

You need a ThingSpeak account. First create a channel, then copy/rename the file `config.sample.py` to `config.py` and fill it with the API key of your channel.
The script `read_and_push.sh` will read the current values and put them in the `cache` directory for later upload.
It'll try to upload them immediately, and in case of errors, it'll try again at the next call.
Useful for crontab.
