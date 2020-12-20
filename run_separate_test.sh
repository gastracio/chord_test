#!/bin/sh

test_report_dir=test_report_$(date +%s)
echo "Creating dir $test_report_dir"
mkdir "$test_report_dir"
touch "$test_report_dir/test.log"

export DISPLAY=:0.0
xhost +

echo Running tests
sudo venv/bin/pytest --log-file="$test_report_dir/test.log" --html="$test_report_dir/test_report.html" \
-p no:dependency \
chord_test.py::test_bios_interrupt_catching \
chord_test.py::test_setup_in_first_boot \
"$1"

