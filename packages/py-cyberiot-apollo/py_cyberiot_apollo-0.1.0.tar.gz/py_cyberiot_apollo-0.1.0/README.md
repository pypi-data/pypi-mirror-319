# Project description
## py_cyberiot_apollo

A Python Library for reading data from the Cyberiot Apollo Household Energy Management System.

You can directly call the library for UUID registration, connectivity detection, and some configuration before receiving data, but you need to provide the serial number and host.


### Usage


```sh
from py_cyberiot_apollo import Apollo
import asyncio


async def test():
	# initialization
	apollo = Apollo(serial_number="Your serial number", host="device host")

	# Register a UUID.
	device_uuid = await apollo.register_uuid()

	# Sampling data synchronization settings
	sync_data_is_success = await apollo.sync_data(device_uuid) -> bool

	# Data transmission control
	data_ctrl_is_success = await apollo.data_ctrl(device_uuid) -> bool

	# Test connection.
	check_connection_is_success = await apollo.check_connection() -> bool


if __name__ == "__main__":
	asyncio.run(test())
```