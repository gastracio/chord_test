pi_user=pi
pi_ip=192.168.0.5

all: deploy

deploy:
	rsync -av -e ssh --exclude='venv/' --exclude='*.log' --exclude='*cache*/' --exclude='.*/' . $(pi_user)@$(pi_ip):~/chord_test

install:
	python3 -m venv ./venv
	venv/bin/pip install -r requirements.txt

uninstall:
	rm -r venv

power_on:
	venv/bin/python tools.py power_on

power_off:
	venv/bin/python tools.py power_off

reboot:
	venv/bin/python tools.py reboot

dis_keys:
	venv/bin/python tools.py all_interrupters_disconnect

interrupter_list:
	venv/bin/python tools.py interrupters_list

interrupter_list_verbose:
	sudo timeout 4 sudo pcsc_scan

clean:
	rm -rf .idea .pytest_cache __pycache__ test_report_*

run:
	sudo venv/bin/pytest

check_hardware:
	# TOOD: Make pytest hardware test run