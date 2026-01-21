# TOPSIS CLI Part 1 Review Report

| Test Case | Status | Details |
|---|---|---|
| Argument Count Check | PASS | Exit code 1 on missing args |
| File Not Found Check | PASS | Exit code 1 on missing file |
| Column Count Check | PASS | Exit code 1 on <3 columns |
| Non-Numeric Check | PASS | Exit code 1 on text in data |
| Weights Mismatch Check | PASS | Exit code 1 on weights mismatch |
| Impacts Mismatch Check | PASS | Exit code 1 on impacts mismatch |
| Invalid Impacts Check | PASS | Exit code 1 on '%' char |
| Invalid Weights Check | PASS | Exit code 1 on 'a' in weights |
| Valid Run Check | PASS | Exit code 0, file created with Score/Rank |
