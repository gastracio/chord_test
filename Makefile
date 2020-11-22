pi_user=pi
pi_ip=192.168.0.5

all: deploy_main

deploy_main:
	rsync -av -e ssh --exclude='venv/' --exclude='*.log' --exclude='*cache*/' --exclude='.*/' . pi@192.168.0.5:~/chord_test

deploy:
	rsync -avzhe ssh . $(pi_user)@$(pi_ip):~/chord_test

run:
	sudo venv/bin/pytest

power_on:
	venv/bin/python power.py power

power_off:
	venv/bin/python power.py reboot
	sleep 1
	venv/bin/python power.py power


reboot:
	venv/bin/python power.py reboot

dis_keys:
	venv/bin/python interrupter.py disconnect
