import heapq

def weighted_a_star(graph, weights, heuristics, start, goal, weight=1.5):
    """
    Weighted A* implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    weights (dict): Weights for edges, e.g., {(u,v): weight}.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.
    weight: Weight for heuristic, default 1.5.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    def reconstruct_path(parent, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    open_list = [(0, start)]  # (f, node)
    closed_list = set()
    parent = {start: None}
    g = {start: 0}

    print(f"Starting Weighted A* from {start} to {goal} with weight {weight}")
    print(f"Heuristics: {heuristics}")
    print()

    while open_list:
        f, current = heapq.heappop(open_list)
        if current in closed_list:
            continue
        closed_list.add(current)
        print(f"Expand: {current} (f: {f})")

        if current == goal:
            print(f"Goal {goal} reached!")
            return reconstruct_path(parent, goal)

        for neighbor in graph.get(current, []):
            if neighbor in closed_list:
                continue
            edge_weight = weights.get((current, neighbor), 1)
            tentative_g = g[current] + edge_weight
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                f = tentative_g + weight * heuristics[neighbor]
                heapq.heappush(open_list, (f, neighbor))
                parent[neighbor] = current
                print(f"  Enqueue: {neighbor} (g: {tentative_g}, h: {heuristics[neighbor]}, w*h: {weight * heuristics[neighbor]}, f: {f})")

        print("---")

    print("No path found")
    return None

# Example usage
if __name__ == "__main__":
    # Graph: A -> B(1), C(4); B -> D(2); C -> E(3); D -> E(1)
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': ['E'],
        'E': []
    }

    # Weights
    weights = {
        ('A', 'B'): 1,
        ('A', 'C'): 4,
        ('B', 'D'): 2,
        ('C', 'E'): 3,
        ('D', 'E'): 1
    }

    # Heuristics (e.g., straight-line distance to E)
    heuristics = {
        'A': 3,
        'B': 2,
        'C': 1,
        'D': 1,
        'E': 0
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print("Weights:")
    for edge, weight in weights.items():
        print(f"{edge}: {weight}")
    print()

    path = weighted_a_star(graph, weights, heuristics, 'A', 'E', weight=1.5)
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
