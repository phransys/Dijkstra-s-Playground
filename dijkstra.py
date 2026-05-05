import heapq


def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    previous = {}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node]:
            dist = current_dist + weight

            if dist < distances[neighbor]:
                distances[neighbor] = dist
                previous[neighbor] = current_node
                heapq.heappush(pq, (dist, neighbor))

    return distances, previous


def reconstruct_path(previous, start, end):
    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()
    return path