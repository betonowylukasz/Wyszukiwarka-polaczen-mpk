from reader import load_connection_graph
from methods import final_edge_list, convert_to_datetime, print_travel_schedule
import datetime

global connections
connections = load_connection_graph('connection_graph.csv')

def create_apex_dict(connection_graph):
    apex_dict={}
    start_set=set()
    end_set=set()
    for connection in connection_graph:
        if not connection['start_stop'] in apex_dict:
            apex_dict[connection['start_stop']] = {
                'edge': '',
                'timedelta': '',
                'cost': datetime.timedelta(hours=100),
                'edges': []
            }
        else:
            apex_dict[connection['start_stop']]['edges'].append(connection)
        if not connection['end_stop'] in apex_dict:
            apex_dict[connection['end_stop']] = {
                'edge': '',
                'timedelta': '',
                'cost': datetime.timedelta(hours=100),
                'edges': []
            }
        start_set.add(connection['start_stop'])
        end_set.add(connection['end_stop'])
    return apex_dict, start_set, end_set

def dijkstra(start, end, start_time):
    time = convert_to_datetime(start_time)
    apex_dict, start_set, end_set = create_apex_dict(connections)

    calculating_start = datetime.datetime.now()

    if start in start_set and end in end_set and time < datetime.timedelta(hours=24):
        print(f"Start podrozy: {start_time}")
        q = end_set
        curr = start
        apex_dict[start]['cost'] = datetime.timedelta(seconds=0)
        apex_dict[start]['timedelta'] = time
        while len(q) > 0:
            if curr in q: q.remove(curr)
            for connection in apex_dict[curr]['edges']:
                waiting_time = connection['start_time'] - apex_dict[curr]['timedelta']
                if waiting_time < datetime.timedelta(0): waiting_time = waiting_time + datetime.timedelta(
                    hours=24)
                cost = waiting_time + apex_dict[curr]['cost'] + connection['time']
                end_apex = apex_dict[connection['end_stop']]
                if cost < end_apex['cost']:
                    end_apex['cost'] = cost
                    end_apex['timedelta'] = connection['end_time']
                    end_apex['edge'] = connection
            min_cost = datetime.timedelta(hours=200)
            for apex_key in q:
                if apex_dict[apex_key]['cost'] < min_cost:
                    min_cost = apex_dict[apex_key]['cost']
                    curr = apex_key
        print(f"Czas podrozy: {apex_dict[end]['cost']}")
        return final_edge_list(apex_dict, end), (datetime.datetime.now() - calculating_start), apex_dict
    else:
        print("Bledne dane wejsciowe!")

def main():
    travel_schedule, calculating_time, _= dijkstra("Budziszyńska", "KOZANÓW", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")


if __name__ == '__main__':
    main()
