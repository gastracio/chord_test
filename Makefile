#!/bin/dash
pi_user=pi
pi_ip=192.168.0.5
test_report_dir_name=test_report_$(date +%s)

all: deploy

deploy:
	rsync -av -e ssh --exclude='venv/' --exclude='test_report_*' --exclude='*.log' --exclude='*cache*/' --exclude='.*/' \
	. $(pi_user)@$(pi_ip):~/chord_test

get_logs:
	rsync -av -e ssh --exclude='venv/' --exclude='*cache*/' --exclude='.*/' \
	$(pi_user)@$(pi_ip):~/chord_test/test_report_* .

install:
#	libs for OpenCV
	sudo apt-get update
	sudo apt install python3-matplotlib
	sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libjasper-dev
	sudo apt-get install -y libqtgui4 libqt4-test
#	matplotlib
	#sudo apt-get install -y tcl-dev tk-dev python-tk python3-tk
#TODO: Install matplotlib from rep: git clone https://github.com/matplotlib/matplotlib.git
#	Virtual Enviroment
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

disable_interrupters:
	venv/bin/python tools.py all_interrupters_disconnect

enable_interrupters:
	venv/bin/python tools.py all_interrupters_connect

interrupter_list:
	venv/bin/python tools.py interrupters_list

interrupter_list_verbose:
	sudo timeout 4 sudo pcsc_scan

clean:
	sudo rm -rf .idea .pytest_cache __pycache__ test_report_*

run:
	$(eval timestamp := $(shell date +%s))
	mkdir test_report_$(timestamp)
	sudo venv/bin/pytest --log-file=test.log --log-file=test.log
	cp test.log test_report_$(timestamp)/test.log

check_hardware:
	# TODO: Make pytest hardware test run