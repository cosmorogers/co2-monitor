from flask import Flask, render_template
from smbus import SMBus
import time

EE895ADDRESS = 0x5E
I2CREGISTER = 0x00

app = Flask(__name__)
i2cbus = SMBus(1)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api")
def api():
    read_data = i2cbus.read_i2c_block_data(EE895ADDRESS, I2CREGISTER, 8)
    # read_data contains ints, which we need to convert to bytes and merge
    # see datasheet
    co2 = read_data[0].to_bytes(1, 'big') + read_data[1].to_bytes(1, 'big')
    temperature = read_data[2].to_bytes(1, 'big') + read_data[3].to_bytes(1, 'big')
    # reserved value - useful to check that the sensor is reading out correctly
    # this should be 0x8000
    resvd = read_data[4].to_bytes(1, 'big') + read_data[5].to_bytes(1, 'big')
    pressure = read_data[6].to_bytes(1, 'big') + read_data[7].to_bytes(1, 'big')
    return {
        "co2": (int.from_bytes(co2, "big")),
        "temperature": (int.from_bytes(temperature, "big") / 100),
        "pressure": (int.from_bytes(pressure, "big") / 10)
    }


