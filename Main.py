import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

DATA_DIR = Path("data")
ELECTRICITY_FILE = DATA_DIR / "electricity.csv"
WATER_FILE = DATA_DIR / "water.csv"


def ensure_data_files_exist():
    DATA_DIR.mkdir(exist_ok=True)
    if not ELECTRICITY_FILE.exists():
        with ELECTRICITY_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "block_name", "units_used"])
    if not WATER_FILE.exists():
        with WATER_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "block_name", "litres_used"])


def add_daily_usage():
    ensure_data_files_exist()
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")

    block_name = input("Enter block name (e.g., A-Block): ").strip()
    if not block_name:
        print("Block name cannot be empty.")
        return

    try:
        elec_units = float(input("Enter electricity units used (kWh): ").strip())
        water_litres = float(input("Enter water used (litres): ").strip())
    except ValueError:
        print("Invalid input: Please enter numeric values.")
        return

    if elec_units < 0 or water_litres < 0:
        print("Values cannot be negative.")
        return

    with ELECTRICITY_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, block_name, elec_units])

    with WATER_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, block_name, water_litres])

    print("Daily usage recorded successfully.")


def load_csv(file_path):
    records = []
    if not file_path.exists():
        return records
    with file_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def show_daily_summary():
    elec = load_csv(ELECTRICITY_FILE)
    water = load_csv(WATER_FILE)

    daily_elec = defaultdict(float)
    daily_water = defaultdict(float)

    for row in elec:
        daily_elec[row["date"]] += float(row["units_used"])
    for row in water:
        daily_water[row["date"]] += float(row["litres_used"])

    dates = sorted(set(daily_elec.keys()) | set(daily_water.keys()))
    print("\nDate        | Elec (kWh) | Water (L)")
    print("----------------------------------------")
    for date in dates:
        e = daily_elec.get(date, 0.0)
        w = daily_water.get(date, 0.0)
        print(f"{date} | {e:10.2f} | {w:9.2f}")


def show_block_totals():
    elec = load_csv(ELECTRICITY_FILE)
    water = load_csv(WATER_FILE)

    block_elec = defaultdict(float)
    block_water = defaultdict(float)

    for row in elec:
        block_elec[row["block_name"]] += float(row["units_used"])
    for row in water:
        block_water[row["block_name"]] += float(row["litres_used"])

    blocks = sorted(set(block_elec.keys()) | set(block_water.keys()))
    print("\nBlock       | Elec (kWh) | Water (L)")
    print("----------------------------------------")
    for block in blocks:
        e = block_elec.get(block, 0.0)
        w = block_water.get(block, 0.0)
        print(f"{block:10} | {e:10.2f} | {w:9.2f}")


def detect_abnormal_usage(threshold_percent=20.0, window=7):
    if not ELECTRICITY_FILE.exists():
        print("Electricity data not found.")
        return

    elec_records = load_csv(ELECTRICITY_FILE)
    if not elec_records:
        print("No electricity records to analyze.")
        return

    daily_usage = defaultdict(float)
    for row in elec_records:
        daily_usage[row["date"]] += float(row["units_used"])

    dates = sorted(daily_usage.keys())
    if len(dates) <= window:
        print(f"Not enough data for spike detection; need more than {window} days.")
        return

    abnormal_days = []
    for i in range(window, len(dates)):
        current_date = dates[i]
        current_usage = daily_usage[current_date]
        prev_window_dates = dates[i - window:i]
        avg_usage = sum(daily_usage[d] for d in prev_window_dates) / window
        if avg_usage > 0:
            increase_percent = ((current_usage - avg_usage) / avg_usage) * 100
            if increase_percent >= threshold_percent:
                abnormal_days.append((current_date, current_usage, increase_percent))

    if not abnormal_days:
        print("No abnormal usage detected.")
    else:
        print("\nAbnormal Usage Days:")
        print("Date        | Usage (kWh) | % Above Avg")
        print("----------------------------------------")
        for date, usage, percent in abnormal_days:
            print(f"{date} | {usage:10.2f} | {percent:11.2f}")


def plot_daily_usage():
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib not installed; visualization unavailable.")
        return
    elec_records = load_csv(ELECTRICITY_FILE)
    if not elec_records:
        print("No electricity data to plot.")
        return
    daily_elec = defaultdict(float)
    for row in elec_records:
        daily_elec[row["date"]] += float(row["units_used"])
    dates = sorted(daily_elec.keys())
    values = [daily_elec[d] for d in dates]
    plt.figure()
    plt.plot(dates, values, marker='o')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Date")
    plt.ylabel("Electricity Usage (kWh)")
    plt.title("Daily Electricity Usage")
    plt.tight_layout()
    plt.show()


def plot_block_comparison():
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib not installed; visualization unavailable.")
        return
    elec_records = load_csv(ELECTRICITY_FILE)
    if not elec_records:
        print("No electricity data to plot.")
        return
    block_totals = defaultdict(float)
    for row in elec_records:
        block_totals[row["block_name"]] += float(row["units_used"])
    blocks = list(block_totals.keys())
    usage_values = [block_totals[b] for b in blocks]
    plt.figure()
    plt.bar(blocks, usage_values)
    plt.xlabel("Block")
    plt.ylabel("Electricity Usage (kWh)")
    plt.title("Block-wise Electricity Usage (Total)")
    plt.tight_layout()
    plt.show()


def main_menu():
    while True:
        print("\n=== SHUMS: Smart Hostel Utility Management System ===")
        print("1. Enter daily usage")
        print("2. View summaries")
        print("3. Check abnormal usage")
        print("4. Visualizations")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_daily_usage()
        elif choice == '2':
            print("\nSummary Options:")
            print("1. Daily summary")
            print("2. Block-wise totals")
            summary_choice = input("Choose summary type: ").strip()
            if summary_choice == '1':
                show_daily_summary()
            elif summary_choice == '2':
                show_block_totals()
            else:
                print("Invalid choice.")
        elif choice == '3':
            detect_abnormal_usage()
        elif choice == '4':
            if not MATPLOTLIB_AVAILABLE:
                print("Visualization module requires matplotlib. Please install it to use this feature.")
                continue
            print("\nVisualization Options:")
            print("1. Plot daily electricity usage")
            print("2. Plot block-wise electricity usage")
            viz_choice = input("Choose visualization type: ").strip()
            if viz_choice == '1':
                plot_daily_usage()
            elif viz_choice == '2':
                plot_block_comparison()
            else:
                print("Invalid choice.")
        elif choice == '5':
            print("Exiting SHUMS. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
