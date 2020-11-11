pi_user=pi
pi_ip=192.168.0.5

all: deploy_main

deploy_main:
	scp -r chord_test.py $(pi_user)@$(pi_ip):~/chord_test/
	scp -r config.json $(pi_user)@$(pi_ip):~/chord_test/
	scp -r id_class.py $(pi_user)@$(pi_ip):~/chord_test/
	scp -r conftest.py $(pi_user)@$(pi_ip):~/chord_test/
	scp -r pytest.ini $(pi_user)@$(pi_ip):~/chord_test/
	scp -r testing_hardware.py $(pi_user)@$(pi_ip):~/chord_test/

deploy:
	scp -r ../chord_test $(pi_user)@$(pi_ip):~/

run:
	ssh $(pi_user)@$(pi_ip)
	sleep 1
	cd chord_test
	pytest
	exit
