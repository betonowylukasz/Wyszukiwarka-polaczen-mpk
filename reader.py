import csv
import datetime
from methods import convert_to_datetime


def load_connection_graph(filename):
    connections = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = convert_to_datetime(row['departure_time'])
            end_time = convert_to_datetime(row['arrival_time'])
            time = end_time - start_time
            if start_time >= datetime.timedelta(hours=24): start_time = start_time - datetime.timedelta(hours=24)
            if end_time >= datetime.timedelta(hours=24): end_time = end_time - datetime.timedelta(hours=24)
            connection = {
                'company': row['company'],
                'line': str(row['line']),
                'start_time': start_time,
                'end_time': end_time,
                'time': time,
                'start_stop': row['start_stop'],
                'end_stop': row['end_stop'],
                'start_stop_lat': float(row['start_stop_lat']),
                'start_stop_lon': float(row['start_stop_lon']),
                'end_stop_lat': float(row['end_stop_lat']),
                'end_stop_lon': float(row['end_stop_lon'])
            }
            connections.append(connection)
    return connections




def main():
    filename = 'connection_graph.csv'
    connections = load_connection_graph(filename)
    print(connections)

if __name__ == '__main__': main()
