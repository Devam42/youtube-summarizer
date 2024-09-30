from datetime import datetime
import csv

def log_gemini_usage(total_cost):
    with open("gemini_api_usage.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                         total_cost,
                         datetime.now().strftime("%m/%d/%Y")])
