# Export events to a CSV file

import csv
from database.queries import fetch_all_events

def export_events_to_csv(path="event_report.csv"):
    events = fetch_all_events()
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Event ID", "Name", "Date", "Location", "Organizer"])
        for e in events:
            writer.writerow(e)
    return path