# thmon

## Installing

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

## Read values from the sensor

Run `read_value.sh`, it will (hopefully) read the value from the sensor and write it to a temporary file in the `cache` directory.


## Pushing to ThingSpeak

You need a ThingSpeak account. First create a channel, then copy/rename the file `config.py.sample` to `config.py` and fill it with the API key of your channel.
Run `thingspeak_push.py`, it will take care of everything, including wiping cache files at the end.


## Read value and push it

Run `read_and_push.sh`. Useful for crontab.
