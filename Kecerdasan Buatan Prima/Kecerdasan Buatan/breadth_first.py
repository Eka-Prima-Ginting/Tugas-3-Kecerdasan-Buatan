from collections import deque

def breadth_first_search(graph, start):
    """
    Breadth First Search (BFS) implementation with simulation.

    Args:
    graph (dict): Adjacency list representation of the graph.
    start: Starting node.

    Returns:
    list: List of visited nodes in BFS order.
    """
    visited = set()
    queue = deque([start])
    visited.add(start)
    bfs_order = []

    print(f"Starting BFS from node: {start}")
    print(f"Initial queue: {list(queue)}")
    print(f"Initial visited: {list(visited)}")
    print()

    while queue:
        current = queue.popleft()
        bfs_order.append(current)
        print(f"Dequeued: {current}")
        print(f"Current BFS order: {bfs_order}")

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                print(f"Enqueued neighbor: {neighbor}")
                print(f"Queue now: {list(queue)}")
                print(f"Visited now: {list(visited)}")
        print("---")

    print(f"\nFinal BFS traversal order: {bfs_order}")
    return bfs_order

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

    breadth_first_search(graph, 'A')
