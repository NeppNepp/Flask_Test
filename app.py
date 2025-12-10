from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point, WriteOptions
import time
import os

app = Flask(__name__)

# -------------------------------
# ✅ INFLUXDB CONFIG (SET THESE)
# -------------------------------

INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "UuazYa64wWR-2ZuW4qm2JN-N8vYz2bN2vthBeqqARTDPHOFtLOvm2mPX64W21nTLOjnC07Ez-3w1g7bfSmU4xw=="
INFLUX_ORG = "Robotic-Labwork"
INFLUX_BUCKET = "unoq_sensor_data"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=WriteOptions(batch_size=1))

# -------------------------------
# ✅ ROUTES
# -------------------------------

@app.route("/", methods=["GET"])
def home():
    return "UNO Q + InfluxDB Server Running ✅"

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()

    ax = float(data["ax"])
    az = float(data["az"])
    gx = float(data["gx"])
    gz = float(data["gz"])
    ts = float(data.get("timestamp", time.time()))

    point = (
        Point("imu_data")
        .field("ax", ax)
        .field("az", az)
        .field("gx", gx)
        .field("gz", gz)
        .time(int(ts * 1e9))  # nanoseconds
    )

    write_api.write(bucket=INFLUX_BUCKET, record=point)

    print("✅ Stored in InfluxDB:", data)

    return jsonify({"status": "stored"})

# -------------------------------
# ✅ RENDER ENTRY POINT
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
