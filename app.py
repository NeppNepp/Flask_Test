from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point, WriteOptions
import time
import os

app = Flask(__name__)

# -------------------------------
# ✅ INFLUXDB CONFIG (SET THESE)
# -------------------------------

INFLUX_URL = os.environ["INFLUX_URL"]
INFLUX_TOKEN = os.environ["INFLUX_TOKEN"]
INFLUX_ORG = os.environ["INFLUX_ORG"]
INFLUX_BUCKET = os.environ["INFLUX_BUCKET"]

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
    ay = float(data["ay"])
    az = float(data["az"])
    gx = float(data["gx"])
    gy = float(data["gy"])
    gz = float(data["gz"])
    ts = float(data.get("timestamp", time.time()))

    point = (
        Point("imu_data")
        .field("ax", ax)
        .field("ay", ay)
        .field("az", az)
        .field("gx", gx)
        .field("gy", gy)
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
