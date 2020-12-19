import glob


def get_test_report_dir():
    return "test_report_" + str(max([int(report.split('_')[-1]) for report in glob.glob("test_report_*")]))

