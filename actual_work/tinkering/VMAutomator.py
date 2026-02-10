#!/usr/bin/python3
import sys
import subprocess

arg = sys.argv[1]

power_on = 'VBoxManage startvm "' + arg + '" --type headless' #headless means no GUI
power_off = 'VBoxManage controlvm "' + arg + '" poweroff'

# power on the machine
on_result = subprocess.run(power_on,shell=True, capture_output=True)
#power off the machine
off_result = subprocess.run(power_off, shell=True, capture_output=True)


print(on_result.stdout)
print('errors')
print(on_result.stderr)

print('attempting to power off')
print(off_result.stdout)
print(off_result.stderr)


