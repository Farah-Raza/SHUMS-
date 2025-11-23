# Smart Hostel Utility Management System (SHUMS)

SHUMS is a Python-based project designed to monitor and analyze hostel electricity and water consumption.  
It provides daily data entry, summary reports, abnormal usage detection using a simple moving average, and basic visualizations for decision support.

## Features

- Record daily electricity and water usage for each hostel block through a menu-driven CLI.
- Store data in CSV files for easy portability and reuse.
- Generate daily and block-wise summaries of electricity and water consumption.
- Detect abnormal spikes in electricity usage using a moving average and percentage threshold.
- Plot daily time-series and block-wise comparison graphs for electricity usage (if matplotlib is available).

## Technologies Used

- **Python 3.x** – Core implementation language.
- **csv module** – Reading and writing structured tabular data to CSV files.
- **pathlib** – Platform-independent file and path handling.
- **collections (defaultdict)** – Simple aggregation for summaries and analytics.
- **matplotlib** (optional) – Line and bar plots for visualizing usage trends.



You will see a text-based menu with options to:

- Enter daily usage
- View summaries
- Check abnormal usage
- See visualizations (if matplotlib is installed)
- Exit the system

## Usage Overview

1. **Enter Daily Usage**

   - Choose the “Enter daily usage” option.
   - Enter date (or leave blank for today), block name, electricity units, and water usage.
   - Data is appended to `data/electricity.csv` and `data/water.csv` with proper headers.

2. **View Summaries**

   - View total electricity and water consumption per day.
   - View total electricity and water consumption per block across all days.

3. **Check Abnormal Usage**

   - Run rule-based detection for abnormal electricity consumption.
   - The system computes a moving average over the last *N* days and flags days that exceed the average by a given percentage threshold.

4. **Visualizations (Optional)**

   - Plot daily electricity usage as a line graph.
   - Plot total electricity usage per block as a bar chart.

## Assumptions and Limitations

- Data is entered manually by hostel staff through the CLI.
- Date values are expected in `YYYY-MM-DD` format.
- Only positive numeric values are accepted for usage; invalid or negative inputs are rejected with an error message.
- Weekly and monthly summaries can be added as an extension using the existing CSV-based design.

## Future Enhancements

- GUI-based interface (Tkinter or web-based front-end).
- Role-based login for admin and staff users.
- Integration with real sensor data and IoT devices.
- Automated email or dashboard alerts to hostel administration.
- More advanced analytics (correlation with occupancy, weather, or semester schedule).

