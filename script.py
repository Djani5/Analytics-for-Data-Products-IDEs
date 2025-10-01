import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

PATH = "toolwindow_data.csv"

def load_data(path):
    data = pd.read_csv(path, header=None, names=["timestamp","event","open_type","user_id"], dtype=str)
    data = data[data["timestamp"].str.isnumeric()]
    data["timestamp"] = data["timestamp"].astype(int)
    data["user_id"] = data["user_id"].astype(int)
    data = data.sort_values(["user_id","timestamp"]).reset_index(drop=True)
    return data

'''
To get a clear view of a single user's activity, this function randomly selects one
user from the dataset and saves all their records to a text file named "user_sample.txt". 
This allows for easy inspection of an individual user's interaction patterns.
We can see a pattern of pairs of open and close events for the tool window.
'''
def sample_data(data, n = None):
    if n is None:
        n = random.choice(data["user_id"].unique())

    user_data = data[data["user_id"] == n]
    with open("user_sample.txt", "w") as f:
        f.write(user_data.to_string(index=False))


def analyze_data(data):

    manual_open_pairs = []
    auto_open_pairs = []
    
    for _, user_data in data.groupby("user_id"):
        open_event = None
        for _, row in user_data.iterrows():
            if row["event"] == "opened":
                open_event = row
            elif row["event"] == "closed" and open_event is not None:
                duration = row["timestamp"] - open_event["timestamp"]
                if open_event["open_type"] == "manual":
                    manual_open_pairs.append([duration])
                elif open_event["open_type"] == "auto":
                    auto_open_pairs.append([duration])
                open_event = None
        
    print(f"Manual open pairs: {len(manual_open_pairs)}")
    print(f"Auto open pairs: {len(auto_open_pairs)}\n")
    return sorted(manual_open_pairs), sorted(auto_open_pairs)


def plot(auto_open_pairs, manual_open_pairs, bins=100):
    auto_durations = np.array([x[0] for x in auto_open_pairs])
    manual_durations = np.array([x[0] for x in manual_open_pairs])

    auto_log = np.log10(auto_durations + 1)
    manual_log = np.log10(manual_durations + 1)

    plt.figure(figsize=(10,6))
    plt.hist(auto_log, bins=bins, alpha=0.7, color='salmon', density=True, edgecolor=None, label="Auto")
    plt.hist(manual_log, bins=bins, alpha=0.7, color='skyblue', density=True, edgecolor=None, label="Manual")
    
    plt.xlabel("Log10(Duration + 1) [ms]")
    plt.ylabel("Density")
    plt.title("Overlayed Distribution of Tool Window Durations (log scale)")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

def generate_summary(manual_open_pairs, auto_open_pairs):

    def summarize(pairs):
        durations = np.array([x[0] for x in pairs])
        logs = np.log10(durations + 1)
        return {
            "count": len(durations),
            "mean_s": durations.mean()/1000,
            "median_s": np.median(durations)/1000,
            "std_s": durations.std()/1000,
            "log_mean": logs.mean(),
            "log_median": np.median(logs),
            "p5_s": np.percentile(durations, 5)/1000,
            "p95_s": np.percentile(durations, 95)/1000
        }
    
    manual_summary = summarize(manual_open_pairs)
    auto_summary = summarize(auto_open_pairs)

    summary_text = (
        f"Tool Window Usage Summary\n"
        f"{'-'*110}\n"
        f"{'Open Type':<10}{'Count':>10}{'Mean (s)':>12}{'Median (s)':>12}"
        f"{'Std Dev (s)':>14}{'Log Mean':>12}{'Log Median':>14}"
        f"{'P5 (s)':>12}{'P95 (s)':>12}\n"
        f"{'-'*110}\n"
        f"{'Manual':<10}{manual_summary['count']:>10}{manual_summary['mean_s']:>12.2f}"
        f"{manual_summary['median_s']:>12.2f}{manual_summary['std_s']:>14.2f}"
        f"{manual_summary['log_mean']:>12.2f}{manual_summary['log_median']:>14.2f}"
        f"{manual_summary['p5_s']:>12.2f}{manual_summary['p95_s']:>12.2f}\n"
        f"{'Auto':<10}{auto_summary['count']:>10}{auto_summary['mean_s']:>12.2f}"
        f"{auto_summary['median_s']:>12.2f}{auto_summary['std_s']:>14.2f}"
        f"{auto_summary['log_mean']:>12.2f}{auto_summary['log_median']:>14.2f}"
        f"{auto_summary['p5_s']:>12.2f}{auto_summary['p95_s']:>12.2f}\n"
    )

    print(summary_text)




data = load_data(PATH)
print(f"Length of data: {len(data)}\nUsers: {data['user_id'].nunique()}\n")

#sample_data(data)
manual_open_pairs, auto_open_pairs = analyze_data(data)


#print(manual_open_pairs)
#print(auto_open_pairs)

plot(auto_open_pairs,manual_open_pairs, bins=100)
generate_summary(manual_open_pairs, auto_open_pairs)
