from reader import load_connection_graph
from dijkstra import dijkstra
from methods import print_travel_schedule
from astar import astar, astar_plus


def main():
    travel_schedule, calculating_time, _ = dijkstra("Budziszyńska", "KOZANÓW", "15:30:00")
    print_travel_schedule(travel_schedule)
    print()
    print(f"Czas obliczen: {calculating_time}")
    print()
    print()
    travel_schedule, calculating_time,_ = astar("Budziszyńska", "KOZANÓW", "t", "15:30:00")
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