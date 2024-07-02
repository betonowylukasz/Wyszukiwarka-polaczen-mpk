import matplotlib.pyplot as plt
from reader import load_connection_graph
from dijkstra import dijkstra
from astar import astar


def plot():
    plt.figure(figsize=(10, 8))

    connections = load_connection_graph('connection_graph.csv')

    # Utwórz set połączeń
    connections_set = set()
    for conn in connections:
        start_coords = (conn['start_stop_lon'], conn['start_stop_lat'])
        end_coords = (conn['end_stop_lon'], conn['end_stop_lat'])
        connections_set.add((start_coords, end_coords))

    # Rysuj połączenia
    for start_coords, end_coords in connections_set:
        plt.plot([start_coords[0], end_coords[0]], [start_coords[1], end_coords[1]], marker='.', linestyle='-')

    # Ustaw tytuł i etykiety osi
    plt.title('Mapa połączeń')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')

    # Zapisz wykres do pliku
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('mapa_polaczen.png')  # Zapisz jako obraz PNG
    plt.show()

def dijkstra_plot():
    plt.figure(figsize=(10, 8))

    _,_,apex_dict = dijkstra("Marchewkowa", "Tramwajowa",  "07:45:00")
    apexes = list(apex_dict.keys())


    for apex in apexes:
        edge = apex_dict[apex]['edge']
        if edge != '':
            start_coords = (edge['start_stop_lon'], edge['start_stop_lat'])
            end_coords = (edge['end_stop_lon'], edge['end_stop_lat'])
            plt.plot([start_coords[0], end_coords[0]], [start_coords[1], end_coords[1]], marker='.', linestyle='-')


    # Ustaw tytuł i etykiety osi
    plt.title('Mapa połączeń A*')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')

    # Zapisz wykres do pliku
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('mapa_polaczen_dijkstra.png')  # Zapisz jako obraz PNG
    plt.show()



if __name__ == '__main__':
    dijkstra_plot()
