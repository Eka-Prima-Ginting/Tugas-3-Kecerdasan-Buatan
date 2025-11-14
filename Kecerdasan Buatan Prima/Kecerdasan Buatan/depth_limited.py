def depth_limited_search(graph, start, goal, limit):
    """
    Depth Limited Search (DLS) implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    start: Starting node.
    goal: Goal node.
    limit: Depth limit.

    Returns:
    list or None: Path to goal if found within limit, else None.
    """
    def dls_recursive(node, goal, limit, path, visited):
        print(f"Visiting node: {node} at depth {len(path)-1}")
        print(f"Current path: {path}")
        print(f"Visited: {list(visited)}")

        if node == goal:
            print(f"Goal {goal} found!")
            return path

        if len(path) - 1 >= limit:
            print(f"Depth limit {limit} reached at node {node}, cutting off")
            return None

        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result = dls_recursive(neighbor, goal, limit, path + [neighbor], visited)
                if result is not None:
                    return result

        visited.remove(node)  # Backtrack
        print(f"Backtracking from {node}")
        return None

    visited = set()
    print(f"Starting DLS from {start} to {goal} with depth limit {limit}")
    print()

    result = dls_recursive(start, goal, limit, [start], visited)

    if result:
        print(f"\nPath found: {result}")
    else:
        print(f"\nNo path found within depth limit {limit}")
    return result

# Example usage
if __name__ == "__main__":
    # Graph with depth exceeding limit: A -> B -> C -> D -> E
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D'],
        'D': ['E'],
        'E': []
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print()

    depth_limited_search(graph, 'A', 'E', 2)  # Limit 2, goal at depth 4
