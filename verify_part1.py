import subprocess
import os
import pandas as pd
import sys

# Configuration
TOPSIS_SCRIPT = "topsis.py"
TEST_DIR = "test_artifacts"
os.makedirs(TEST_DIR, exist_ok=True)

# Helper to run command
def run_topsis(args):
    cmd = [sys.executable, TOPSIS_SCRIPT] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

# Create test files
def create_csv(filename, data):
    df = pd.DataFrame(data)
    path = os.path.join(TEST_DIR, filename)
    df.to_csv(path, index=False)
    return path

# Test Data
valid_data = {
    'Fund': ['M1', 'M2', 'M3'],
    'P1': [10, 20, 30],
    'P2': [0.5, 0.2, 0.1],
    'P3': [100, 200, 300]
} # 3 numeric cols, 1 text col = 4 cols total. Wait, logic says "From 2nd to last" (indices 1:).
# If input has 4 cols (0,1,2,3), indices 1,2,3 are numeric.
# Wait, "Input File: Fund Name, P1, P2...". So Col 0 is Name. P1.. are Col 1..
# So valid_data above has 4 columns. Col 0 is Fund. Col 1,2,3 are numeric.
# Weights needed: 3. Impacts needed: 3.

create_csv("valid.csv", valid_data)

few_cols_data = {
    'Fund': ['M1'],
    'P1': [10]
} # 2 cols
create_csv("few_cols.csv", few_cols_data)

text_in_numeric_data = {
    'Fund': ['M1', 'M2'],
    'P1': [10, 'text'],
    'P2': [0.5, 0.2]
}
create_csv("text_in_numeric.csv", text_in_numeric_data)

results = []

def log_test(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    results.append(f"| {name} | {status} | {detail} |")
    print(f"Test {name}: {status}")

# 1. Test Argument Count
res = run_topsis([])
log_test("Argument Count Check", res.returncode != 0 and "Wrong number of parameters" in res.stdout, "Exit code 1 on missing args")

# 2. Test File Not Found
res = run_topsis(["missing.csv", "1,1,1", "+,+,+", "out.csv"])
log_test("File Not Found Check", res.returncode != 0 and "File not found" in res.stdout, "Exit code 1 on missing file")

# 3. Test Column Count
res = run_topsis([os.path.join(TEST_DIR, "few_cols.csv"), "1", "+", "out.csv"])
log_test("Column Count Check", res.returncode != 0 and "three or more columns" in res.stdout, "Exit code 1 on <3 columns")

# 4. Test Non-Numeric
res = run_topsis([os.path.join(TEST_DIR, "text_in_numeric.csv"), "1,1", "+,+", "out.csv"])
log_test("Non-Numeric Check", res.returncode != 0 and "contain numeric values only" in res.stdout, "Exit code 1 on text in data")

# 5. Test Weights Mismatch
res = run_topsis([os.path.join(TEST_DIR, "valid.csv"), "1,1", "+,+,+", "out.csv"]) # 2 weights, 3 cols
log_test("Weights Mismatch Check", res.returncode != 0 and "Number of weights" in res.stdout, "Exit code 1 on weights mismatch")

# 6. Test Impacts Mismatch
res = run_topsis([os.path.join(TEST_DIR, "valid.csv"), "1,1,1", "+,+", "out.csv"]) # 3 weights, 2 impacts
log_test("Impacts Mismatch Check", res.returncode != 0 and "Number of weights" in res.stdout, "Exit code 1 on impacts mismatch")

# 7. Test Invalid Impacts
res = run_topsis([os.path.join(TEST_DIR, "valid.csv"), "1,1,1", "+,%,+", "out.csv"])
log_test("Invalid Impacts Check", res.returncode != 0 and "Impacts must be either +ve or -ve" in res.stdout, "Exit code 1 on '%' char")

# 8. Test Invalid Weights
res = run_topsis([os.path.join(TEST_DIR, "valid.csv"), "1,a,1", "+,+,+", "out.csv"])
log_test("Invalid Weights Check", res.returncode != 0 and "Weights must be numeric" in res.stdout, "Exit code 1 on 'a' in weights")

# 9. Test Valid Run
out_file = os.path.join(TEST_DIR, "result.csv")
res = run_topsis([os.path.join(TEST_DIR, "valid.csv"), "1,1,1", "+,-,+", out_file])
file_exists = os.path.exists(out_file)
content_ok = False
if file_exists:
    df = pd.read_csv(out_file)
    if 'Topsis Score' in df.columns and 'Rank' in df.columns:
        content_ok = True

log_test("Valid Run Check", res.returncode == 0 and file_exists and content_ok, "Exit code 0, file created with Score/Rank")

# Generate MarkDown Report
print("\nGenerating Report...")
with open("review_report.md", "w") as f:
    f.write("# TOPSIS CLI Part 1 Review Report\n\n")
    f.write("| Test Case | Status | Details |\n")
    f.write("|---|---|---|\n")
    for r in results:
        f.write(r + "\n")
