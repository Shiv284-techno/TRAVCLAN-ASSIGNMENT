import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    return result.stdout, result.returncode

def test_hotel_analysis_streamlined():
    output, returncode = run_script('hotel_analysis_streamlined.py')
    assert returncode == 0
    assert "expected_output" in output

def test_quick_viz_test():
    output, returncode = run_script('quick_viz_test.py')
    assert returncode == 0
    assert "expected_output" in output

def test_hotel_booking_analysis():
    output, returncode = run_script('hotel_booking_analysis.py')
    assert returncode == 0
    assert "expected_output" in output