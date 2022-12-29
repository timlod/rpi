import logging
import sys
import time

import RPi.GPIO as GPIO
import typer

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("power.log", mode="a"),
    ],
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def shutdown():
    GPIO.output(40, True)
    time.sleep(10)
    GPIO.output(40, False)


def boot():
    GPIO.output(40, True)
    time.sleep(0.5)
    GPIO.output(40, False)


def main(off: bool=False, switch: bool=False):
    try:
        if switch:
            print("Switch operation (manual).")
            press = False
            while True:
                if GPIO.input(10) == GPIO.HIGH:
                    if not press:
                        logging.info("Button pressed.")
                    press = True
                    GPIO.output(40, press)
                else:
                    if press:
                        logging.info("Button released.")
                    press = False
                    GPIO.output(40, press)
                time.sleep(0.1)
        if off:
            logging.info("Shutting down.")
            shutdown()
        else:
            logging.info("Booting.")
            boot()
    except KeyboardInterrupt as e:
        logging.warning("Interrupted.")
    except Exception as e:
        logging.error(e)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    typer.run(main)
