import argparse

from ctypes import Structure, windll, c_uint, sizeof, byref
import keyboard
import time
import sched

event_schedule = sched.scheduler(time.time, time.sleep)

CHECK_DELAY = 63


class LASTINPUTINFO(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("dwTime", c_uint),
    ]


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def _press_keys(delay=0.5):
    keyboard.press_and_release("capslock")
    time.sleep(delay)
    keyboard.press_and_release("capslock")


def main():
    if get_idle_duration() >= CHECK_DELAY:
        _press_keys(delay=0.5)
    event_schedule.enter(10, 1, main, ())


def create_parser():
    parser = argparse.ArgumentParser(description="Never let the windows system sleep")
    return parser


def cli():
    "Never let the windows system sleep"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    print("Your system will not sleep. Please keep this open.")
    event_schedule.enter(10, 1, main, ())
    event_schedule.run()
