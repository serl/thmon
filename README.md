# thmon

## Read values from the sensor

Run `read_value.sh`, it will (hopefully) read the value from the sensor and write it to a temporary file in the `cache` directory.

Depends on `Adafruit_Python_DHT`; go and read readme to install (hint: `sudo apt install python-pip && sudo pip install Adafruit_DHT`).

It won't write to stdout, check return value for success/failure.


## Pushing to ThingSpeak

You need a ThingSpeak account. First create a channel, then copy/rename the file `config.py.sample` to `config.py` and fill it with the API key of your channel.
Run `thingspeak_push.py`, it will take care of everything, including wiping cache files at the end.


## Read value and push it

Run `read_and_push.sh`. Useful for crontab.
