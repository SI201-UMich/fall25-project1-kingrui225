import csv
import os
from project_calculations import (
    load_samplestores,
    filter_out,
    calculate_average,
    generate_output
)


def test_load_samplestores():
    """Test cases for load_samplestores function"""
    print("\n--- Testing load_samplestores ---")
    
    # Test 1: General case - load valid CSV file
    print("\nTest 1 (General): Load valid CSV file")
    test_file_1 = "test_data_1.csv"
    with open(test_file_1, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'Segment', 'Profit'])
        writer.writerow(['Michigan', 'Consumer', '100'])
        writer.writerow(['Michigan', 'Consumer', '200'])
    result = load_samplestores(test_file_1)
    assert len(result) == 2, "Should load 2 records"
    assert result[0]['State'] == 'Michigan', "First record should have State=Michigan"
    print("✓ Passed")
    os.remove(test_file_1)
    
    # Test 2: General case - load CSV with multiple rows
    print("\nTest 2 (General): Load CSV with multiple rows and columns")
    test_file_2 = "test_data_2.csv"
    with open(test_file_2, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'Segment', 'Profit', 'Sales'])
        for i in range(5):
            writer.writerow(['Texas', 'Corporate', str(i*50), str(i*100)])
    result = load_samplestores(test_file_2)
    assert len(result) == 5, "Should load 5 records"
    print("✓ Passed")
    os.remove(test_file_2)
    
    # Test 3: Edge case - file does not exist
    print("\nTest 3 (Edge): File does not exist")
    result = load_samplestores("nonexistent_file.csv")
    assert result == [], "Should return empty list for nonexistent file"
    print("✓ Passed")
    
    # Test 4: Edge case - empty CSV file (only headers)
    print("\nTest 4 (Edge): Empty CSV file (only headers)")
    test_file_4 = "test_data_4.csv"
    with open(test_file_4, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['State', 'Segment', 'Profit'])
    result = load_samplestores(test_file_4)
    assert len(result) == 0, "Should load 0 records from empty CSV"
    print("✓ Passed")
    os.remove(test_file_4)


def test_filter_out():
    """Test cases for filter_out function"""
    print("\n--- Testing filter_out ---")
    
    # Test 1: General case - filter matching records
    print("\nTest 1 (General): Filter matching records")
    data = [
        {'State': 'Michigan', 'Segment': 'Consumer', 'Profit': '100'},
        {'State': 'Michigan', 'Segment': 'Consumer', 'Profit': '200'},
        {'State': 'Texas', 'Segment': 'Consumer', 'Profit': '150'},
    ]
    result = filter_out(data, 'Michigan', 'Consumer')
    assert len(result) == 2, "Should filter 2 records"
    assert all(r['State'] == 'Michigan' and r['Segment'] == 'Consumer' for r in result), "All records should match filter"
    print("✓ Passed")
    
    # Test 2: General case - filter with multiple states and segments
    print("\nTest 2 (General): Filter from mixed data")
    data = [
        {'State': 'Michigan', 'Segment': 'Consumer', 'Profit': '100'},
        {'State': 'Michigan', 'Segment': 'Corporate', 'Profit': '200'},
        {'State': 'Texas', 'Segment': 'Consumer', 'Profit': '150'},
        {'State': 'Texas', 'Segment': 'Corporate', 'Profit': '300'},
    ]
    result = filter_out(data, 'Texas', 'Corporate')
    assert len(result) == 1, "Should filter 1 record"
    assert result[0]['Profit'] == '300', "Filtered record should have Profit=300"
    print("✓ Passed")
    
    # Test 3: Edge case - no matching records
    print("\nTest 3 (Edge): No matching records")
    data = [
        {'State': 'Michigan', 'Segment': 'Consumer', 'Profit': '100'},
        {'State': 'Texas', 'Segment': 'Corporate', 'Profit': '200'},
    ]
    result = filter_out(data, 'California', 'Consumer')
    assert len(result) == 0, "Should return empty list when no records match"
    print("✓ Passed")
    
    # Test 4: Edge case - empty data list
    print("\nTest 4 (Edge): Empty data list")
    result = filter_out([], 'Michigan', 'Consumer')
    assert len(result) == 0, "Should return empty list for empty input"
    print("✓ Passed")


def test_calculate_average():
    """Test cases for calculate_average function"""
    print("\n--- Testing calculate_average ---")
    
    # Test 1: General case - calculate average of positive profits
    print("\nTest 1 (General): Calculate average of positive profits")
    data = [
        {'Profit': '100'},
        {'Profit': '200'},
        {'Profit': '300'},
    ]
    result = calculate_average(data)
    assert result == 200.0, "Average should be 200.0"
    print("✓ Passed")
    
    # Test 2: General case - calculate average with decimal values
    print("\nTest 2 (General): Calculate average with decimal values")
    data = [
        {'Profit': '50.5'},
        {'Profit': '100.5'},
        {'Profit': '149.0'},
    ]
    result = calculate_average(data)
    assert abs(result - 100.0) < 0.01, "Average should be approximately 100.0"
    print("✓ Passed")
    
    # Test 3: Edge case - empty data list
    print("\nTest 3 (Edge): Empty data list")
    result = calculate_average([])
    assert result == 0.0, "Should return 0.0 for empty list"
    print("✓ Passed")
    
    # Test 4: Edge case - data with negative and positive profits
    print("\nTest 4 (Edge): Data with negative and positive profits")
    data = [
        {'Profit': '-100'},
        {'Profit': '100'},
        {'Profit': '0'},
    ]
    result = calculate_average(data)
    assert result == 0.0, "Average of -100, 100, 0 should be 0.0"
    print("✓ Passed")


def test_generate_output():
    """Test cases for generate_output function"""
    print("\n--- Testing generate_output ---")
    
    # Test 1: General case - write output to file
    print("\nTest 1 (General): Write output to file")
    output_file = "test_output_1.txt"
    generate_output(150.75, output_file)
    assert os.path.exists(output_file), "Output file should be created"
    with open(output_file, 'r') as f:
        content = f.read()
        assert "150.75" in content, "Output should contain the profit value"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 2: General case - overwrite existing file
    print("\nTest 2 (General): Overwrite existing file")
    output_file = "test_output_2.txt"
    with open(output_file, 'w') as f:
        f.write("Old content")
    generate_output(250.50, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "Old content" not in content, "File should be overwritten"
        assert "250.50" in content, "Output should contain new profit value"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 3: Edge case - zero profit value
    print("\nTest 3 (Edge): Zero profit value")
    output_file = "test_output_3.txt"
    generate_output(0.0, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "0.00" in content, "Output should contain 0.00"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 4: Edge case - very large profit value
    print("\nTest 4 (Edge): Very large profit value")
    output_file = "test_output_4.txt"
    generate_output(999999.99, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "999999.99" in content, "Output should contain large profit value"
    print("✓ Passed")
    os.remove(output_file)


def run_all_tests():
    """Run all test cases"""
    print("=" * 50)
    print("RUNNING ALL TEST CASES")
    print("=" * 50)
    
    test_load_samplestores()
    test_filter_out()
    test_calculate_average()
    test_generate_output()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
