def ida_star(graph, weights, heuristics, start, goal):
    """
    IDA* (Iterative Deepening A*) implementation with simulation (Memory Bounded Search).

    Args:
    graph (dict): Adjacency list representation of the graph.
    weights (dict): Weights for edges, e.g., {(u,v): weight}.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    def search(path, g, bound):
        current = path[-1]
        f = g + heuristics[current]
        print(f"  Expanding: {current} (g: {g}, h: {heuristics[current]}, f: {f})")

        if f > bound:
            print(f"  f > bound ({bound}), cutoff")
            return f

        if current == goal:
            print(f"  Goal {goal} reached!")
            return 'FOUND'

        min_bound = float('inf')
        for neighbor in graph.get(current, []):
            if neighbor not in path:
                edge_weight = weights.get((current, neighbor), 1)
                new_g = g + edge_weight
                path.append(neighbor)
                result = search(path, new_g, bound)
                if result == 'FOUND':
                    return 'FOUND'
                if result < min_bound:
                    min_bound = result
                path.pop()

        return min_bound

    if start == goal:
        return [start]

    bound = heuristics[start]
    path = [start]

    print(f"Starting IDA* from {start} to {goal}")
    print(f"Heuristics: {heuristics}")
    print(f"Initial bound: {bound}")
    print()

    while True:
        print(f"Iteration with bound: {bound}")
        result = search(path, 0, bound)
        if result == 'FOUND':
            return path
        if result == float('inf'):
            print("No path found")
            return None
        bound = result
        print(f"New bound: {bound}")
        print("---")

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

    path = ida_star(graph, weights, heuristics, 'A', 'E')
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
