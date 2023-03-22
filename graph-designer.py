#!/usr/bin/python3
import subprocess
import sys
import networkx

colors = ['#0000FF', '#00FF00', '#FF0000', '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF']
default_output_name = "out.png"
values = []

num_nodes = 0
num_colors = 0


def get_node_possibilities(node):
    return values[node * num_colors: (node + 1) * num_colors]


def get_color_hex_from_sublist(sublist):
    for i in range(num_colors):
        if sublist[i] > 0:
            return colors[i]


def paint_nodes(A):
    for i in range(num_nodes):
        A.get_node(i).attr['fillcolor'] = get_color_hex_from_sublist(get_node_possibilities(i))


def save_graph(A):
    A.layout()
    if len(sys.argv) > 2:
        output_name = sys.argv[2]
    else:
        output_name = default_output_name
    A.draw(output_name, format='png')


def calculate_skipped_lines():
    tmp = 0
    for i in range(1, num_colors):
        tmp += i
    return 2 + tmp * num_nodes + num_nodes


def create_edges(A):
    try:
        cnf_file = open(sys.argv[1], "r")
        lines = cnf_file.readlines()
        cnf_file.close()
    except IOError:
        pass
    lines = lines[calculate_skipped_lines():]
    print(calculate_skipped_lines())
    num_edges = int(len(lines) / num_colors)
    for i in range(num_edges):
        edge = lines[i * num_colors]
        edge = edge.split()[:-1]
        for j in range(2):
            edge[j] = int(edge[j])
            edge[j] = abs(edge[j])
            edge[j] = int((edge[j] - 1) / num_colors)
        print(edge)
        A.add_edge(tuple(edge))


def print_graph(graph):
    A = networkx.nx_agraph.to_agraph(graph)
    A.node_attr['style'] = 'filled'
    A.node_attr['width'] = '0.4'
    A.node_attr['height'] = '0.4'
    A.edge_attr['color'] = '#000000'
    paint_nodes(A)
    create_edges(A)
    save_graph(A)


def node_generation():
    graph = networkx.Graph()
    for i in range(num_nodes):
        graph.add_node(i)
    return graph


def read_file():
    global values, num_nodes
    result = subprocess.run(["python3", "solver-pvp.py", f"{sys.argv[1]}"], capture_output=True, text=True)
    solver_output = result.stdout.split("\n")

    if solver_output[0] == "s SATISFIABLE":
        print("Satisfible solution")
        if solver_output[1].startswith("v"):
            values = solver_output[1].split()[1:]
            for i in range(len(values)):
                values[i] = int(values[i])
                if values[i] > 0:
                    num_nodes += 1


if __name__ == '__main__':
    read_file()
    num_colors = int(len(values) / num_nodes)
    print_graph(node_generation())
