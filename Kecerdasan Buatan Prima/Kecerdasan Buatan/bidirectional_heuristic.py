import heapq

def bidirectional_a_star(graph, reverse_graph, weights, heuristics, start, goal):
    """
    Bidirectional A* implementation with simulation.

    Args:
    graph (dict): Adjacency list from start to goal.
    reverse_graph (dict): Adjacency list from goal to start.
    weights (dict): Weights for edges, e.g., {(u,v): weight}.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    def reconstruct_path(forward_parent, backward_parent, intersection, start, goal):
        path = []
        current = intersection
        while current != start:
            path.append(current)
            current = forward_parent[current]
        path.append(start)
        path.reverse()
        current = intersection
        while current != goal:
            current = backward_parent[current]
            path.append(current)
        return path

    if start == goal:
        return [start]

    forward_open = [(heuristics[start], start)]
    backward_open = [(heuristics[goal], goal)]
    forward_closed = set()
    backward_closed = set()
    forward_parent = {start: None}
    backward_parent = {goal: None}
    forward_g = {start: 0}
    backward_g = {goal: 0}

    print(f"Starting Bidirectional A* from {start} to {goal}")
    print(f"Heuristics: {heuristics}")
    print()

    while forward_open and backward_open:
        # Forward search
        f_f, current_f = heapq.heappop(forward_open)
        if current_f in forward_closed:
            continue
        forward_closed.add(current_f)
        print(f"Forward expand: {current_f} (f: {f_f})")

        if current_f in backward_closed:
            print(f"Intersection at {current_f}")
            return reconstruct_path(forward_parent, backward_parent, current_f, start, goal)

        for neighbor in graph.get(current_f, []):
            if neighbor in forward_closed:
                continue
            edge_weight = weights.get((current_f, neighbor), 1)
            tentative_g = forward_g[current_f] + edge_weight
            if neighbor not in forward_g or tentative_g < forward_g[neighbor]:
                forward_g[neighbor] = tentative_g
                f = tentative_g + heuristics[neighbor]
                heapq.heappush(forward_open, (f, neighbor))
                forward_parent[neighbor] = current_f
                print(f"  Forward enqueue: {neighbor} (g: {tentative_g}, h: {heuristics[neighbor]}, f: {f})")

        # Backward search
        f_b, current_b = heapq.heappop(backward_open)
        if current_b in backward_closed:
            continue
        backward_closed.add(current_b)
        print(f"Backward expand: {current_b} (f: {f_b})")

        if current_b in forward_closed:
            print(f"Intersection at {current_b}")
            return reconstruct_path(forward_parent, backward_parent, current_b, start, goal)

        for neighbor in reverse_graph.get(current_b, []):
            if neighbor in backward_closed:
                continue
            edge_weight = weights.get((neighbor, current_b), 1)  # Reverse edge
            tentative_g = backward_g[current_b] + edge_weight
            if neighbor not in backward_g or tentative_g < backward_g[neighbor]:
                backward_g[neighbor] = tentative_g
                f = tentative_g + heuristics[neighbor]
                heapq.heappush(backward_open, (f, neighbor))
                backward_parent[neighbor] = current_b
                print(f"  Backward enqueue: {neighbor} (g: {tentative_g}, h: {heuristics[neighbor]}, f: {f})")

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

    # Reverse graph for backward search
    reverse_graph = {
        'E': ['C', 'D'],
        'D': ['B'],
        'C': ['A'],
        'B': ['A'],
        'A': []
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

    path = bidirectional_a_star(graph, reverse_graph, weights, heuristics, 'A', 'E')
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
