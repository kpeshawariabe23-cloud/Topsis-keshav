import sys
import os
import pandas as pd
import numpy as np

def validate_inputs():
    if len(sys.argv) != 5:
        print("Error: Wrong number of parameters")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.exists(input_file):
        print("Error: File not found")
        sys.exit(1)

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error: Could not read file. {e}")
        sys.exit(1)

    if len(df.columns) < 3:
        print("Error: Input file must contain three or more columns")
        sys.exit(1)

    # Validate numeric values from 2nd text column (index 0 is 1st, so index 1 is 2nd... wait. 
    # Prompt says "From 2nd to last columns must contain numeric values only".
    # Assuming valid columns are indices 1 onwards (0-based indexing)
    
    # Check for non-numeric values
    try:
        data = df.iloc[:, 1:].values
        data = data.astype(float)
    except ValueError:
        print("Error: From 2nd to last columns must contain numeric values only")
        sys.exit(1)

    weights = weights_str.split(',')
    impacts = impacts_str.split(',')

    if len(weights) != len(impacts) or len(weights) != (len(df.columns) - 1):
        print("Error: Number of weights, impacts and columns must be the same")
        sys.exit(1)

    for i in impacts:
        if i not in ['+', '-']:
            print("Error: Impacts must be either +ve or -ve")
            sys.exit(1)
            
    try:
        weights = [float(w) for w in weights]
    except ValueError:
         print("Error: Weights must be numeric")
         sys.exit(1)

    return df, weights, impacts, output_file

def topsis(df, weights, impacts, output_file):
    # Extract data for processing
    dataset = df.iloc[:, 1:].values.astype(float)
    rows, cols = dataset.shape

    # 1. Normalize
    squared_sum = np.sqrt(np.sum(dataset**2, axis=0))
    normalized_dataset = dataset / squared_sum

    # 2. Weight Assignment
    weighted_normalized = normalized_dataset * weights

    # 3. Ideal Best and Ideal Worst
    ideal_best = []
    ideal_worst = []

    for i in range(cols):
        if impacts[i] == '+':
            ideal_best.append(np.max(weighted_normalized[:, i]))
            ideal_worst.append(np.min(weighted_normalized[:, i]))
        else:
            ideal_best.append(np.min(weighted_normalized[:, i]))
            ideal_worst.append(np.max(weighted_normalized[:, i]))

    # 4. Euclidean Distance
    distance_positive = np.sqrt(np.sum((weighted_normalized - ideal_best)**2, axis=1))
    distance_negative = np.sqrt(np.sum((weighted_normalized - ideal_worst)**2, axis=1))

    # 5. Topsis Score
    performance_score = distance_negative / (distance_positive + distance_negative)

    # 6. Rank
    df['Topsis Score'] = performance_score
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)
    print(f"Result saved to {output_file}")

if __name__ == "__main__":
    df, weights, impacts, output_file = validate_inputs()
    topsis(df, weights, impacts, output_file)
