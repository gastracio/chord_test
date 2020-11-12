import time
from testing_hardware import TestingHardware
import sys


pc = TestingHardware()

if sys.argv[1] == "reboot":
    print("Reboot")
    pc.reboot()
    exit(0)

if sys.argv[1] == "power":
    print("Power switch")
    pc.reboot()
    exit(0)


print("Power on")
pc.power_switch()
time.sleep(45)
print("Reboot")
pc.reboot()
time.sleep(45)
print("Power off")
pc.power_switch()
