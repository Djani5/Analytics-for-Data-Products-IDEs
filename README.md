# Tool Window Analysis

This project analyzes tool window session durations in an application, comparing **manual** vs **auto** opens.

---

## 1. Approach

**Goal:** Compare durations of tool window sessions between manual and auto opens.

**Method:**
- Load and clean data.
- Group events by `user_id`.
- Match open-close events and calculate durations.
- Separate by `open_type` (manual vs auto).
- Visualize distributions using **log-transformed histograms**.
- Compute summary statistics: count, mean, median, standard deviation, log-mean, log-median, and 5th/95th percentiles.

---

## 2. Assumptions and Data Cleaning

- Events are sorted by `user_id` and timestamp.
- Non-numeric timestamps are removed.
- Orphaned events handled:
  - Close events without prior open were ignored.
  - Open events without a later close before dataset end were ignored.
  - Only the first unmatched open in consecutive opens was considered.

*Optional:* For larger datasets, K-Means clustering could categorize durations into short, medium, and long usage groups.

---

## 3. Analysis

- **Data Loading:** CSV read with Pandas, timestamps cleaned and sorted.
- **Pair Matching:** Iterates per user to match opens and closes.
- **Visualization:** Overlayed log-scaled histograms normalize densities to compare manual vs auto opens.
- **Summary Statistics:** Count, mean, median, standard deviation, log-mean, log-median, 5th/95th percentiles.

---

## 4. Key Observations

- Auto opens tend to be **longer on average** and show higher variance.
- Log transformation reveals patterns across very short and very long durations.
- 5th–95th percentiles provide a measure of confidence in typical durations.
<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/34b22685-31b7-474d-bd8c-53030207eaff" />


## 5. Deliverables

- Python script: `toolwindow_analysis.py`
- Sorted duration outputs (optional): `auto_open_sorted.txt` / `manual_open_sorted.txt`
- Analysis summary: `analysis_summary.txt`
- Histogram plot comparing manual vs auto open durations

---

## 6. How to Run

**Install dependencies:**
```bash
pip install pandas matplotlib numpy
```
**Run script:**
```bash
py script.py
```
