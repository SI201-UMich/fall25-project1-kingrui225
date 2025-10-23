# Project Calculations - Question 2

# Within the second class ship model, what is the average number of sales within the furniture category?

import csv


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


def main():
    """
    Runs the program and calls the functions in a logical sequence
    
    Input: none
    Output: none
    """
    # Configuration
    csv_file = "SampleSuperstore.csv"
    ship_model = "Second Class"
    category = "Furniture"
    output_file = "average_sales_output.txt"
    
    # Execute the workflow
    print("Starting sales analysis...")
    data = load_samplestores(csv_file)
    
    if data:
        filtered_data = filter_out(data, ship_model, category)
        average_sales = calculate_average(filtered_data)
        generate_output(average_sales, output_file)
        print("Analysis complete!")
    else:
        print("Failed to load data. Exiting.")


if __name__ == "__main__":
    main()
