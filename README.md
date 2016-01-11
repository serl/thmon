# thmon

## values collector `read_value.sh`

Depends on `Adafruit_Python_DHT`; go and read readme to install.
It will (hopefully) read the value from the sensor and write it to a temporary file in the `cache` directory.
It won't write to stdout, check return value for success/failure.


## Login to Parse.com

Run `parse_login.py` and follow instructions. It will create a config.py file.
The possible exceptions are not handled, so errors are not so meaningful nor explicative.
