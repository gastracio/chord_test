pi_user=pi
pi_ip=192.168.0.5

all: deploy_main

deploy_main:
	rsync -av -e ssh --exclude='venv/' --exclude='*.log' --exclude='*cache*/' --exclude='.*/' . pi@192.168.0.5:~/chord_test

deploy:
	scp -r ../chord_test $(pi_user)@$(pi_ip):~/

run:
	sudo venv/bin/pytest

power:
	venv/bin/python power.py power

reboot:
	venv/bin/python power.py reboot
