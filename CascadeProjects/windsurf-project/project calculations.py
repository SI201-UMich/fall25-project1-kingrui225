# Project Calculations

# Determine what is the average profit within the state of michigan for consumer segment companies?
# Within the second class ship model, what is the average number of sales within the furniture category?
# since we are determining the average number of sales, we need to use csv files to format

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


def filter_out(data, state, segment):
    """
    Filters all the dataset in csv file to only include the entries for the given state and segment
    
    Input: data (list of dict), state (str), segment (str)
    Output: filtered_data (list of dict) - filtered records
    """
    filtered_data = []
    for row in data:
        if row.get('State') == state and row.get('Segment') == segment:
            filtered_data.append(row)
    print(f"Filtered to {len(filtered_data)} records for {state}, {segment}")
    return filtered_data


def calculate_average(filtered_data):
    """
    Determines the average profit of the filtered out data
    
    Input: filtered_data (list of dict)
    Output: average_profit (float) - average profit value
    """
    if not filtered_data:
        print("No data to calculate average from")
        return 0.0
    
    total_profit = 0.0
    count = 0
    
    for row in filtered_data:
        try:
            profit = float(row.get('Profit', 0))
            total_profit += profit
            count += 1
        except ValueError:
            continue
    
    average_profit = total_profit / count if count > 0 else 0.0
    print(f"Calculated average profit: ${average_profit:.2f}")
    return average_profit


def generate_output(average_profit, output_file):
    """
    Writes the calculated average profit to an output file
    
    Input: average_profit (float), output_file (str)
    Output: None
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f"Average Profit Analysis\n")
            file.write(f"=======================\n")
            file.write(f"Average Profit: ${average_profit:.2f}\n")
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
    state = "Michigan"
    segment = "Consumer"
    output_file = "average_profit_output.txt"
    
    # Execute the workflow
    print("Starting profit analysis...")
    data = load_samplestores(csv_file)
    
    if data:
        filtered_data = filter_out(data, state, segment)
        average_profit = calculate_average(filtered_data)
        generate_output(average_profit, output_file)
        print("Analysis complete!")
    else:
        print("Failed to load data. Exiting.")


if __name__ == "__main__":
    main()
