from collections import deque

def bidirectional_search(graph, start, goal):
    """
    Bidirectional Search implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    start: Starting node.
    goal: Goal node.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    if start == goal:
        return [start]

    # Forward search from start
    forward_queue = deque([start])
    forward_visited = set([start])
    forward_parent = {start: None}

    # Backward search from goal
    backward_queue = deque([goal])
    backward_visited = set([goal])
    backward_parent = {goal: None}

    print(f"Starting Bidirectional Search from {start} to {goal}")
    print(f"Initial forward queue: {list(forward_queue)}")
    print(f"Initial backward queue: {list(backward_queue)}")
    print()

    while forward_queue and backward_queue:
        # Forward expansion
        current_forward = forward_queue.popleft()
        print(f"Expanding forward from: {current_forward}")
        for neighbor in graph.get(current_forward, []):
            if neighbor not in forward_visited:
                forward_visited.add(neighbor)
                forward_queue.append(neighbor)
                forward_parent[neighbor] = current_forward
                print(f"Forward: Added {neighbor} to queue, parent {current_forward}")
                if neighbor in backward_visited:
                    print(f"Intersection found at {neighbor}!")
                    return reconstruct_path(forward_parent, backward_parent, neighbor, start, goal)

        # Backward expansion
        current_backward = backward_queue.popleft()
        print(f"Expanding backward from: {current_backward}")
        for neighbor in graph.get(current_backward, []):
            if neighbor not in backward_visited:
                backward_visited.add(neighbor)
                backward_queue.append(neighbor)
                backward_parent[neighbor] = current_backward
                print(f"Backward: Added {neighbor} to queue, parent {current_backward}")
                if neighbor in forward_visited:
                    print(f"Intersection found at {neighbor}!")
                    return reconstruct_path(forward_parent, backward_parent, neighbor, start, goal)

        print(f"Forward queue: {list(forward_queue)}")
        print(f"Backward queue: {list(backward_queue)}")
        print("---")

    print("No path found")
    return None

def reconstruct_path(forward_parent, backward_parent, intersection, start, goal):
    # Path from start to intersection
    path = []
    current = intersection
    while current is not None:
        path.append(current)
        current = forward_parent[current]
    path.reverse()

    # Path from intersection to goal (excluding intersection)
    current = backward_parent[intersection]
    while current is not None:
        path.append(current)
        current = backward_parent[current]

    return path

# Example usage
if __name__ == "__main__":
    # Undirected graph: A <-> B, C; B <-> D; C <-> E; D <-> E
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'E'],
        'D': ['B', 'E'],
        'E': ['C', 'D']
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print()

    path = bidirectional_search(graph, 'A', 'E')
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
