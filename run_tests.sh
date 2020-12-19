#!/bin/sh


test_report_dir=test_report_$(date +%s)
echo "Creating dir $test_report_dir"
mkdir "$test_report_dir"
touch "$test_report_dir/test.log"

#echo Configuring lxterminal
#export DISPLAY=:0.0
#xhost +
#lxterminal --title=test_logs --geometry=113x65 --command tail -F "$test_report_dir/test.log" &
#logs_pid=$!

echo Running tests
sudo venv/bin/pytest --log-file="$test_report_dir/test.log" --html="$test_report_dir/test_report.html"

#echo Closing test logs
#kill "$logs_pid"