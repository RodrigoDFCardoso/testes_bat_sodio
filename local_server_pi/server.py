from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "database": "bms",
    "user": "bms_user",
    "password": "testebms2026"
}


class BatteryData(BaseModel):
    timestamp: float
    channel: str
    temp: float
    voltage: float
    current: float
    power: float


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.get("/")
def root():
    return {"status": "BMS server online"}


@app.post("/data")
def receive_data(data: BatteryData):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO battery_data
        (timestamp, channel, temperature, voltage, current_ma, power_mw)
        VALUES (
            to_timestamp(%s),
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        data.timestamp,
        data.channel,
        data.temp,
        data.voltage,
        data.current,
        data.power
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "status": "ok"
    }