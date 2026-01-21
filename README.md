# TOPSIS Assignment Solution

This repository contains the solution for the TOPSIS assignment, divided into three parts.

## Project Structure
- `topsis.py`: The command-line interface (CLI) implementation (Part 1).
- `Topsis-Keshav-102303502/`: The source code for the published Python package (Part 2).
- `web_service/`: The Flask web application (Part 3).
- `data.csv`: Sample input data for testing.

---

## Part 1: TOPSIS CLI Tool
A Python script to perform TOPSIS analysis from the command line.

**Usage:**
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

**Example:**
```bash
python topsis.py data.csv "1,1,1,1,1" "+,+,+,+,+" result.csv
```

---

## Part 2: Python Package
The TOPSIS logic is packaged and published on PyPI as `Topsis-Keshav-102303502`.

**PyPI Link:** [https://pypi.org/project/Topsis-Keshav-102303502/](https://pypi.org/project/Topsis-Keshav-102303502/)

**Installation:**
```bash
pip install Topsis-Keshav-102303502
```

**Usage in Python:**
```python
from topsis.topsis import topsis
topsis('data.csv', [1,1,1], ['+','-','+'], 'result.csv')
```

---

## Part 3: Web Service
A web interface to upload CSV files and get TOPSIS results via email.

**Setup & Run:**
1.  Navigate to the `web_service` directory.
2.  Install dependencies: `pip install flask Topsis-Keshav-102303502`
3.  Run the app:
    ```bash
    python app.py
    ```
4.  Open `http://localhost:5000` in your browser.
5.  Enter your sender credentials (for testing) and recipient email to receive the results.

---

## License
MIT License
