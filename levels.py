import random

def generate_grid_level(n):
    nodes = {}
    graph = {}

    spacing_x = 180
    spacing_y = 130
    start_x = 150
    start_y = 100

    labels = []
    for i in range(n*n):
        labels.append(str(i))

    # assign positions
    index = 0
    for row in range(n):
        for col in range(n):
            label = labels[index]
            nodes[label] = (
                start_x + col * spacing_x,
                start_y + row * spacing_y
            )
            index += 1

    # create edges
    for row in range(n):
        for col in range(n):
            idx = row*n + col
            label = labels[idx]
            graph[label] = []

            # right
            if col < n-1:
                right = labels[idx+1]
                weight = random.randint(1, 9)
                graph[label].append((right, weight))

            # down
            if row < n-1:
                down = labels[idx+n]
                weight = random.randint(1, 9)
                graph[label].append((down, weight))

    # add reverse edges
    for node in list(graph.keys()):
        for neighbor, weight in graph[node]:
            if neighbor not in graph:
                graph[neighbor] = []
            if (node, weight) not in graph[neighbor]:
                graph[neighbor].append((node, weight))

    return {
        "name": f"{n}x{n} Grid",
        "nodes": nodes,
        "graph": graph,
        "start": "0",
        "end": str(n*n - 1)
    }


levels = [
    generate_grid_level(2),
    generate_grid_level(3),
    generate_grid_level(4),
    generate_grid_level(5),
]