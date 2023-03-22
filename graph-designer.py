#!/usr/bin/python3
import sys
import networkx

colors = ['#0000FF', '#00FF00', '#FF0000', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF']
values = []

num_nodes = int(sys.argv[2])
num_colors = int(sys.argv[3])


def get_node_possibilities(node):
    return values[node * num_colors: (node + 1) * num_colors]


def get_color_hex_from_sublist(sublist):
    for i in range(num_colors):
        if sublist[i] > 0:
            return colors[i]


def paint_nodes(A):
    for i in range(num_nodes):
        A.get_node(i).attr['fillcolor'] = get_color_hex_from_sublist(get_node_possibilities(i))


def draw_graph(A):
    A.layout()
    A.draw("out.png", format='png')


def print_graph(graph):
    A = networkx.nx_agraph.to_agraph(graph)
    A.node_attr['style'] = 'filled'
    A.node_attr['width'] = '0.4'
    A.node_attr['height'] = '0.4'
    A.edge_attr['color'] = '#000000'
    paint_nodes(A)
    draw_graph(A)


def node_generation():
    graph = networkx.Graph()
    for i in range(num_nodes):
        graph.add_node(i)
    return graph


def read_file():
    global values
    try:
        with open(f"{sys.argv[1]}", "r") as file:
            for line in file:
                if line.startswith("v"):
                    values = line[1:].split()
                    for i in range(len(values)):
                        values[i] = int(values[i])
                    break
        file.close()
    except IOError:
        exit(1)


if __name__ == '__main__':
    read_file()
    print_graph(node_generation())
