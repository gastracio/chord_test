import glob
import subprocess


def get_test_report_dir():
    return "test_report_" + str(max([int(report.split('_')[-1]) for report in glob.glob("test_report_*")]))


def display_ping():
    command = [
        'xset',
        'dpms',
        'force',
        'on'
    ]
    subprocess.run(command)


