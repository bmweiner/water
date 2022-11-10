from datetime import datetime
import os
import asyncio
import sqlite3
import RPi.GPIO as GPIO

# config
DB_PATH = os.path.expanduser("~/util.db")

# init sqlite db
with sqlite3.connect(DB_PATH) as con:
    cur = con.cursor()
    cur.execute(
        """
        create table if not exists water (
        pulse timestamp not null
        );
        """
    )

# log pulse to sqlite
def log_pulse(channel):
    """Log water meter pulse to sqlite"""
    if GPIO.input(channel) == GPIO.HIGH:
        dt = datetime.now()
        print("Pulse: {}".format(dt))
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("insert into water VALUES(?)", (dt,))
            con.commit()

# main loop
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=log_pulse, bouncetime=500)

    loop = asyncio.get_event_loop()
    loop.run_forever()

except Exception as e:
    print(e)

finally:
    print('async loop closed')
    GPIO.cleanup()
    loop.close()
