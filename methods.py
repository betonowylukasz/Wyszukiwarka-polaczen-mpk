import datetime

def final_edge_list(apex_dict, end):
    edge = apex_dict[end]['edge']
    edge_list = []
    while edge != '':
        edge_list.append(edge)
        edge = apex_dict[edge['start_stop']]['edge']
    edge_list.reverse()
    return edge_list


def convert_to_datetime(time_str):
    hour, minute, second = map(int, time_str.split(':'))
    return datetime.timedelta(hours=hour, minutes=minute)

def print_travel_schedule(travel_schedule):
    prev_edge = travel_schedule[0]
    start_time = prev_edge['start_time']
    start_stop = prev_edge['start_stop']
    end_stop = prev_edge['end_time']
    end_time = prev_edge['end_stop']
    for connection in travel_schedule[1:]:
        if prev_edge['line'] != connection['line'] or not (
                datetime.timedelta(seconds=0) <= (connection['start_time'] - prev_edge['end_time']) <= datetime.timedelta(minutes=3)):
            print(f"Linia {prev_edge['line']}, z {start_stop} [{start_time}] do {end_stop} [{end_time}]")
            start_time = connection['start_time']
            start_stop = connection['start_stop']
            end_time = connection['end_time']
            end_stop = connection['end_stop']
        else:
            end_time = connection['end_time']
            end_stop = connection['end_stop']
        prev_edge = connection
    print(f"Linia {prev_edge['line']}, z {start_stop} [{start_time}] do {end_stop} [{end_time}]")
