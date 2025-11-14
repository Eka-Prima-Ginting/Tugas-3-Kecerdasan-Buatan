def depth_first_search(graph, start):
    """
    Depth First Search (DFS) implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    start: Starting node.

    Returns:
    list: List of visited nodes in DFS order.
    """
    visited = set()
    stack = [start]
    dfs_order = []

    print(f"Starting DFS from node: {start}")
    print(f"Initial stack: {stack}")
    print(f"Initial visited: {list(visited)}")
    print()

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            dfs_order.append(current)
            print(f"Popped and visited: {current}")
            print(f"Current DFS order: {dfs_order}")
            print(f"Visited now: {list(visited)}")

            # Push neighbors in reverse order to simulate depth-first
            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
                    print(f"Pushed neighbor: {neighbor}")
                    print(f"Stack now: {stack}")
        else:
            print(f"Skipped {current} (already visited)")
        print("---")

    print(f"\nFinal DFS traversal order: {dfs_order}")
    return dfs_order

# Example usage
if __name__ == "__main__":
    # Simple graph: A -> B, C; B -> D; C -> E
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': [],
        'E': []
    }

    print("Graph adjacency list:")
    for node, neighbors in graph.items():
        print(f"{node}: {neighbors}")
    print()

    depth_first_search(graph, 'A')
