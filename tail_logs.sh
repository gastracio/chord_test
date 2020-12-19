#!/bin/sh


test_report_dir=$1

echo Configuring lxterminal
export DISPLAY=:0.0
xhost +
lxterminal --title=test_logs --geometry=113x65 --command tail -F "$test_report_dir/test.log"