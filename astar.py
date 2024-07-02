from reader import load_connection_graph
from methods import final_edge_list, convert_to_datetime, print_travel_schedule
import datetime
import math

global connections
connections = load_connection_graph('connection_graph.csv')

def create_apex_dict(connection_graph):
    apex_dict={}
    start_list=[]
    end_list=[]
    for connection in connection_graph:
        if not connection['start_stop'] in apex_dict:
            apex_dict[connection['start_stop']] = {
                'edge': '',
                'timedelta': '',
                'edges': [],
                'time': datetime.timedelta(hours=0),
                'h': 0,
                'cost': 0,
                'swaps': 0,
                'x': connection['start_stop_lon'],
                'y': connection['start_stop_lat']
            }
        else:
            apex_dict[connection['start_stop']]['edges'].append(connection)
        if not connection['end_stop'] in apex_dict:
            apex_dict[connection['end_stop']] = {
                'edge': '',
                'timedelta': '',
                'edges': [],
                'time': datetime.timedelta(hours=0),
                'h': 0,
                'cost': 0,
                'swaps': 0,
                'x': connection['start_stop_lon'],
                'y': connection['start_stop_lat']
            }
        start_list.append(connection['start_stop'])
        end_list.append(connection['end_stop'])
    start_list = list(dict.fromkeys(start_list))
    end_list = list(dict.fromkeys(end_list))
    return apex_dict, start_list, end_list


def manhattan(curr, next):
    return abs(curr['x'] - next['x']) + abs(curr['y'] - next['y'])

def euclides(curr, next):
    return math.sqrt((curr['x']-next['x'])**2 + (curr['y']-next['y'])**2)


def astar(start, end, criterion, start_time):
    apex_dict, start_list, end_list = create_apex_dict(connections)
    time = convert_to_datetime(start_time)

    calculating_start = datetime.datetime.now()

    if start in start_list and end in end_list and time < datetime.timedelta(hours=24) and (criterion == 't' or criterion == 'p'):
        print(f"Start podrozy: {start_time}")
        apex_dict[start]['cost'] = 0
        apex_dict[start]['timedelta'] = time
        opened = [start]
        if criterion == 't': time_astar(apex_dict, end, opened)
        else: swap_astar(apex_dict, end, opened)
        return final_edge_list(apex_dict, end), (datetime.datetime.now() - calculating_start), apex_dict
    else:
        print("Bledne dane wejsciowe!")
        return None, None, None


def time_astar(apex_dict, end, opened):
    closed = []
    while opened:
        min_cost = float('inf')
        for apex in opened:
            if apex_dict[apex]['cost'] < min_cost:
                min_cost = apex_dict[apex]['cost']
                curr = apex
        if curr == end: break
        opened.remove(curr)
        closed.append(curr)
        for connection in apex_dict[curr]['edges']:
            neighbour = connection['end_stop']
            neighbour_apex = apex_dict[neighbour]
            waiting_time = connection['start_time'] - apex_dict[curr]['timedelta']
            if waiting_time < datetime.timedelta(seconds=0): waiting_time = waiting_time + datetime.timedelta(
                hours=24)
            time = waiting_time + apex_dict[curr]['time'] + connection['time']
            if neighbour not in opened and neighbour not in closed:
                opened.append(neighbour)
                h = euclides(apex_dict[neighbour], apex_dict[end])
                neighbour_apex['time'] = time
                neighbour_apex['h'] = h
                neighbour_apex['cost'] = int(time.seconds) / 60 + h
                neighbour_apex['timedelta'] = connection['end_time']
                neighbour_apex['edge'] = connection
            else:
                if time < neighbour_apex['time']:
                    neighbour_apex['time'] = time
                    neighbour_apex['cost'] = int(time.seconds) / 60 + neighbour_apex['h']
                    neighbour_apex['timedelta'] = connection['end_time']
                    neighbour_apex['edge'] = connection
                    if neighbour in closed:
                        opened.append(neighbour)
                        closed.remove(neighbour)

    print(f"Czas podrozy: {apex_dict[end]['time']}")


def swap_astar(apex_dict, end, opened):
    closed = []
    while opened:
        min_cost = float('inf')
        for apex in opened:
            if apex_dict[apex]['cost'] < min_cost:
                min_cost = apex_dict[apex]['cost']
                curr = apex
        if curr == end: break
        opened.remove(curr)
        closed.append(curr)
        for connection in apex_dict[curr]['edges']:
            neighbour = connection['end_stop']
            neighbour_apex = apex_dict[neighbour]
            swaps = apex_dict[curr]['swaps']
            if apex_dict[curr]['edge'] != '':
                if apex_dict[curr]['edge']['line'] != connection['line'] or not (
                        datetime.timedelta(seconds=0) <= (connection['start_time'] - apex_dict[curr]['edge']['end_time']) <= datetime.timedelta(minutes=3)): swaps = swaps + 1
            if neighbour not in opened and neighbour not in closed:
                opened.append(neighbour)
                h = euclides(apex_dict[neighbour], apex_dict[end])
                neighbour_apex['swaps'] = swaps
                neighbour_apex['h'] = h
                neighbour_apex['cost'] = swaps + h
                neighbour_apex['timedelta'] = connection['end_time']
                neighbour_apex['edge'] = connection
            else:
                if swaps < neighbour_apex['swaps']:
                    neighbour_apex['swaps'] = swaps
                    neighbour_apex['cost'] = swaps + neighbour_apex['h']
                    neighbour_apex['timedelta'] = connection['end_time']
                    neighbour_apex['edge'] = connection
                    if neighbour in closed:
                        opened.append(neighbour)
                        closed.remove(neighbour)

    print(f"Liczba przesiadek: {apex_dict[end]['swaps']}")

def astar_plus(start, end, criterion, start_time):
    apex_dict, start_list, end_list = create_apex_dict(connections)
    time = convert_to_datetime(start_time)

    calculating_start = datetime.datetime.now()

    if start in start_list and end in end_list and time < datetime.timedelta(hours=24) and (criterion == 't' or criterion == 'p'):
        print(f"Start podrozy: {start_time}")
        curr = start
        apex_dict[start]['cost'] = 0
        apex_dict[start]['timedelta'] = time
        opened = {start}
        if criterion == 't': time_astar_plus(apex_dict, end, opened)
        else: swap_astar_plus(apex_dict, end, opened)
        return final_edge_list(apex_dict, end), (datetime.datetime.now() - calculating_start), apex_dict
    else:
        print("Bledne dane wejsciowe!")


def time_astar_plus(apex_dict, end, opened):
    closed = set()
    while opened:
        min_cost = float('inf')
        for apex in opened:
            if apex_dict[apex]['cost'] < min_cost:
                min_cost = apex_dict[apex]['cost']
                curr = apex
        if curr == end: break
        opened.remove(curr)
        closed.add(curr)
        for connection in apex_dict[curr]['edges']:
            neighbour = connection['end_stop']
            neighbour_apex = apex_dict[neighbour]
            waiting_time = connection['start_time'] - apex_dict[curr]['timedelta']
            if waiting_time < datetime.timedelta(seconds=0):
                waiting_time += datetime.timedelta(hours=24)
            time = waiting_time + apex_dict[curr]['time'] + connection['time']
            if neighbour not in opened and neighbour not in closed and waiting_time < datetime.timedelta(hours=6):
                opened.add(neighbour)
                h = euclides(apex_dict[neighbour], apex_dict[end])
                neighbour_apex['time'] = time
                neighbour_apex['h'] = h
                neighbour_apex['cost'] = (time.total_seconds() / 3600) + h
                neighbour_apex['timedelta'] = connection['end_time']
                neighbour_apex['edge'] = connection
            else:
                if time < neighbour_apex['time'] or (
                        time == neighbour_apex['time'] and apex_dict[curr]['edge']!='' and apex_dict[curr]['edge']['line'] == connection['line']):
                    neighbour_apex['time'] = time
                    neighbour_apex['cost'] = (time.total_seconds() / 3600) + neighbour_apex['h']
                    neighbour_apex['timedelta'] = connection['end_time']
                    neighbour_apex['edge'] = connection
                    if neighbour in closed:
                        opened.add(neighbour)
                        closed.remove(neighbour)

    print(f"Czas podrozy: {apex_dict[end]['time']}")

def swap_astar_plus(apex_dict, end, opened):
    closed = set()
    while opened:
        min_cost = float('inf')
        curr = None
        for apex in opened:
            if apex_dict[apex]['cost'] < min_cost:
                min_cost = apex_dict[apex]['cost']
                curr = apex
        if curr == end: break
        opened.remove(curr)
        closed.add(curr)
        for connection in apex_dict[curr]['edges']:
            neighbour = connection['end_stop']
            neighbour_apex = apex_dict[neighbour]
            waiting_time = connection['start_time'] - apex_dict[curr]['timedelta']
            if waiting_time < datetime.timedelta(seconds=0): waiting_time = waiting_time + datetime.timedelta(
                hours=24)
            time = waiting_time + apex_dict[curr]['time'] + connection['time']
            swaps = apex_dict[curr]['swaps']
            if apex_dict[curr]['edge'] != '':
                if apex_dict[curr]['edge']['line'] != connection['line'] or not (
                        datetime.timedelta(seconds=0) <= (connection['start_time'] - apex_dict[curr]['edge']['end_time']) <= datetime.timedelta(minutes=3)): swaps = swaps + 1
            if neighbour not in opened and neighbour not in closed:
                opened.add(neighbour)
                h = euclides(apex_dict[neighbour], apex_dict[end])
                neighbour_apex['time'] = time
                neighbour_apex['swaps'] = swaps
                neighbour_apex['h'] = h
                neighbour_apex['cost'] = swaps/20 + h
                neighbour_apex['timedelta'] = connection['end_time']
                neighbour_apex['edge'] = connection
            else:
                if swaps < neighbour_apex['swaps'] or (
                        swaps == neighbour_apex['swaps'] and time < neighbour_apex['time']):
                    neighbour_apex['time'] = time
                    neighbour_apex['swaps'] = swaps
                    neighbour_apex['cost'] = swaps/20 + neighbour_apex['h']
                    neighbour_apex['timedelta'] = connection['end_time']
                    neighbour_apex['edge'] = connection
                    if neighbour in closed:
                        opened.add(neighbour)
                        closed.remove(neighbour)

    print(f"Liczba przesiadek: {apex_dict[end]['swaps']}")

def main():
    travel_schedule, calculating_time, _ = astar("Budziszyńska", "KOZANÓW", "t", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")
    print()
    print()
    travel_schedule, calculating_time, _ = astar("Budziszyńska", "KOZANÓW", "p", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")
    print()
    print()
    travel_schedule, calculating_time, _ = astar_plus("Budziszyńska", "KOZANÓW", "t", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")
    print()
    print()
    travel_schedule, calculating_time, _ = astar_plus("Budziszyńska", "KOZANÓW", "p", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")

if __name__ == '__main__':
    main()
