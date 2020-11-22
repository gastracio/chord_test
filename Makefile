pi_user=pi
pi_ip=192.168.0.5

all: deploy

deploy:
	rsync -av -e ssh --exclude='venv/' --exclude='*.log' --exclude='*cache*/' --exclude='.*/' . $(pi_user)@$(pi_ip):~/chord_test

run:
	sudo venv/bin/pytest

power_on:
	venv/bin/python power.py power

power_off:
	venv/bin/python power.py reboot
	sleep 2
	venv/bin/python power.py power

reboot:
	venv/bin/python power.py reboot

dis_keys:
	venv/bin/python interrupter.py disconnect

interrupter_list:
	venv/bin/python interrupter.py list

interrupter_list_verbose:
	sudo timeout 4 sudo pcsc_scan

install:
	python3 -m venv ./venv
	venv/bin/pip install -r requirements.txt

uninstall:
	rm -r venv