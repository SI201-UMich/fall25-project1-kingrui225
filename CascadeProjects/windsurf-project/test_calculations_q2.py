import csv
import os


def load_samplestores(csv_file):
    """
    Read the superstore datasets from the CSV file and read it into a Python data structure
    
    Input: csv_file (str) - path to the CSV file
    Output: data (list of dict) - parsed CSV data
    """
    try:
        data = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f"Successfully loaded {len(data)} records from {csv_file}")
        return data
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


def filter_out(data, ship_model, category):
    """
    Filters all the dataset in csv file to only include the entries for the given ship model and category
    
    Input: data (list of dict), ship_model (str), category (str)
    Output: filtered_data (list of dict) - filtered records
    """
    filtered_data = []
    for row in data:
        if row.get('Ship Mode') == ship_model and row.get('Category') == category:
            filtered_data.append(row)
    print(f"Filtered to {len(filtered_data)} records for {ship_model}, {category}")
    return filtered_data


def calculate_average(filtered_data):
    """
    Determines the average number of sales of the filtered out data
    
    Input: filtered_data (list of dict)
    Output: average_sales (float) - average sales value
    """
    if not filtered_data:
        print("No data to calculate average from")
        return 0.0
    
    total_sales = 0.0
    count = 0
    
    for row in filtered_data:
        try:
            sales = float(row.get('Sales', 0))
            total_sales += sales
            count += 1
        except ValueError:
            continue
    
    average_sales = total_sales / count if count > 0 else 0.0
    print(f"Calculated average sales: ${average_sales:.2f}")
    return average_sales


def generate_output(average_sales, output_file):
    """
    Writes the calculated average sales to an output file
    
    Input: average_sales (float), output_file (str)
    Output: None
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f"Average Sales Analysis\n")
            file.write(f"======================\n")
            file.write(f"Average Sales: ${average_sales:.2f}\n")
        print(f"Output written to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


# ============== TEST CASES ==============

def test_load_samplestores():
    """Test cases for load_samplestores function"""
    print("\n--- Testing load_samplestores ---")
    
    # Test 1: Normal case - load valid CSV file
    print("\nTest 1 (Normal): Load valid CSV file")
    test_file_1 = "test_q2_data_1.csv"
    with open(test_file_1, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ship Mode', 'Category', 'Sales'])
        writer.writerow(['Second Class', 'Furniture', '500'])
        writer.writerow(['Second Class', 'Furniture', '750'])
    result = load_samplestores(test_file_1)
    assert len(result) == 2, "Should load 2 records"
    assert result[0]['Ship Mode'] == 'Second Class', "First record should have Ship Mode=Second Class"
    print("✓ Passed")
    os.remove(test_file_1)
    
    # Test 2: Normal case - load CSV with multiple columns and rows
    print("\nTest 2 (Normal): Load CSV with multiple columns and rows")
    test_file_2 = "test_q2_data_2.csv"
    with open(test_file_2, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ship Mode', 'Category', 'Sales', 'Profit', 'Quantity'])
        for i in range(10):
            writer.writerow(['First Class', 'Office Supplies', str(i*100), str(i*20), str(i*5)])
    result = load_samplestores(test_file_2)
    assert len(result) == 10, "Should load 10 records"
    assert result[0]['Category'] == 'Office Supplies', "Records should contain Category column"
    print("✓ Passed")
    os.remove(test_file_2)
    
    # Test 3: Edge case - file does not exist
    print("\nTest 3 (Edge): File does not exist")
    result = load_samplestores("nonexistent_q2_file.csv")
    assert result == [], "Should return empty list for nonexistent file"
    print("✓ Passed")
    
    # Test 4: Edge case - empty CSV file (only headers)
    print("\nTest 4 (Edge): Empty CSV file (only headers)")
    test_file_4 = "test_q2_data_4.csv"
    with open(test_file_4, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ship Mode', 'Category', 'Sales'])
    result = load_samplestores(test_file_4)
    assert len(result) == 0, "Should load 0 records from empty CSV"
    print("✓ Passed")
    os.remove(test_file_4)


def test_filter_out():
    """Test cases for filter_out function"""
    print("\n--- Testing filter_out ---")
    
    # Test 1: Normal case - filter matching records
    print("\nTest 1 (Normal): Filter matching records")
    data = [
        {'Ship Mode': 'Second Class', 'Category': 'Furniture', 'Sales': '500'},
        {'Ship Mode': 'Second Class', 'Category': 'Furniture', 'Sales': '750'},
        {'Ship Mode': 'First Class', 'Category': 'Furniture', 'Sales': '600'},
    ]
    result = filter_out(data, 'Second Class', 'Furniture')
    assert len(result) == 2, "Should filter 2 records"
    assert all(r['Ship Mode'] == 'Second Class' and r['Category'] == 'Furniture' for r in result), "All records should match filter"
    print("✓ Passed")
    
    # Test 2: Normal case - filter from mixed data with multiple categories
    print("\nTest 2 (Normal): Filter from mixed data with multiple categories")
    data = [
        {'Ship Mode': 'Second Class', 'Category': 'Furniture', 'Sales': '500'},
        {'Ship Mode': 'Second Class', 'Category': 'Office Supplies', 'Sales': '300'},
        {'Ship Mode': 'First Class', 'Category': 'Furniture', 'Sales': '600'},
        {'Ship Mode': 'First Class', 'Category': 'Technology', 'Sales': '800'},
    ]
    result = filter_out(data, 'First Class', 'Technology')
    assert len(result) == 1, "Should filter 1 record"
    assert result[0]['Sales'] == '800', "Filtered record should have Sales=800"
    print("✓ Passed")
    
    # Test 3: Edge case - no matching records
    print("\nTest 3 (Edge): No matching records")
    data = [
        {'Ship Mode': 'Second Class', 'Category': 'Furniture', 'Sales': '500'},
        {'Ship Mode': 'First Class', 'Category': 'Office Supplies', 'Sales': '300'},
    ]
    result = filter_out(data, 'Same Day', 'Technology')
    assert len(result) == 0, "Should return empty list when no records match"
    print("✓ Passed")
    
    # Test 4: Edge case - empty data list
    print("\nTest 4 (Edge): Empty data list")
    result = filter_out([], 'Second Class', 'Furniture')
    assert len(result) == 0, "Should return empty list for empty input"
    print("✓ Passed")


def test_calculate_average():
    """Test cases for calculate_average function"""
    print("\n--- Testing calculate_average ---")
    
    # Test 1: Normal case - calculate average of sales values
    print("\nTest 1 (Normal): Calculate average of sales values")
    data = [
        {'Sales': '500'},
        {'Sales': '750'},
        {'Sales': '1000'},
    ]
    result = calculate_average(data)
    assert result == 750.0, "Average should be 750.0"
    print("✓ Passed")
    
    # Test 2: Normal case - calculate average with decimal values
    print("\nTest 2 (Normal): Calculate average with decimal values")
    data = [
        {'Sales': '100.50'},
        {'Sales': '200.75'},
        {'Sales': '298.75'},
    ]
    result = calculate_average(data)
    assert abs(result - 200.0) < 0.01, "Average should be approximately 200.0"
    print("✓ Passed")
    
    # Test 3: Edge case - empty data list
    print("\nTest 3 (Edge): Empty data list")
    result = calculate_average([])
    assert result == 0.0, "Should return 0.0 for empty list"
    print("✓ Passed")
    
    # Test 4: Edge case - data with very small and very large sales values
    print("\nTest 4 (Edge): Data with very small and very large sales values")
    data = [
        {'Sales': '0.01'},
        {'Sales': '10000'},
        {'Sales': '5000'},
    ]
    result = calculate_average(data)
    assert abs(result - 5000.0) < 1, "Average should be approximately 5000.0"
    print("✓ Passed")


def test_generate_output():
    """Test cases for generate_output function"""
    print("\n--- Testing generate_output ---")
    
    # Test 1: Normal case - write output to file
    print("\nTest 1 (Normal): Write output to file")
    output_file = "test_q2_output_1.txt"
    generate_output(725.50, output_file)
    assert os.path.exists(output_file), "Output file should be created"
    with open(output_file, 'r') as f:
        content = f.read()
        assert "725.50" in content, "Output should contain the sales value"
        assert "Average Sales" in content, "Output should contain header"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 2: Normal case - overwrite existing file with new data
    print("\nTest 2 (Normal): Overwrite existing file with new data")
    output_file = "test_q2_output_2.txt"
    with open(output_file, 'w') as f:
        f.write("Old data from previous run")
    generate_output(1250.75, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "Old data" not in content, "File should be overwritten"
        assert "1250.75" in content, "Output should contain new sales value"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 3: Edge case - zero sales value
    print("\nTest 3 (Edge): Zero sales value")
    output_file = "test_q2_output_3.txt"
    generate_output(0.0, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "0.00" in content, "Output should contain 0.00"
    print("✓ Passed")
    os.remove(output_file)
    
    # Test 4: Edge case - very large sales value
    print("\nTest 4 (Edge): Very large sales value")
    output_file = "test_q2_output_4.txt"
    generate_output(5000000.99, output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "5000000.99" in content, "Output should contain large sales value"
    print("✓ Passed")
    os.remove(output_file)


def run_all_tests():
    """Run all test cases"""
    print("=" * 50)
    print("RUNNING ALL TEST CASES (Question 2)")
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
