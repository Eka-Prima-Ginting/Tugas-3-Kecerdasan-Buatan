from collections import deque

def beam_search(graph, heuristics, start, goal, beam_width=2):
    """
    Beam Search implementation with simulation (assuming Search Contours as Beam Search).

    Args:
    graph (dict): Adjacency list representation of the graph.
    heuristics (dict): Heuristic values for each node.
    start: Starting node.
    goal: Goal node.
    beam_width (int): Number of best candidates to keep at each level.

    Returns:
    list or None: Path from start to goal if found, else None.
    """
    if start == goal:
        return [start]

    beam = [(heuristics[start], start)]  # (heuristic, node)
    parent = {start: None}

    print(f"Starting Beam Search from {start} to {goal} with beam width {beam_width}")
    print(f"Heuristics: {heuristics}")
    print(f"Initial beam: {beam}")
    print()

    while beam:
        print(f"Current beam: {beam}")
        next_beam = []

        for h, current in beam:
            print(f"Expanding: {current} (h: {h})")

            if current == goal:
                print(f"Goal {goal} reached!")
                return reconstruct_path(parent, goal)

            for neighbor in graph.get(current, []):
                if neighbor not in parent:  # Avoid revisiting
                    parent[neighbor] = current
                    next_beam.append((heuristics[neighbor], neighbor))
                    print(f"Added neighbor: {neighbor} (h: {heuristics[neighbor]})")

        # Sort by heuristic and select top beam_width
        next_beam.sort()
        beam = next_beam[:beam_width]
        print(f"Next beam (top {beam_width}): {beam}")
        print("---")

        if not beam:
            break

    print("No path found")
    return None

def reconstruct_path(parent, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# Example usage
if __name__ == "__main__":
    # Graph: A -> B, C; B -> D; C -> E; D -> E
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['E'],
        'D': ['E'],
        'E': []
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
    print()

    path = beam_search(graph, heuristics, 'A', 'E', beam_width=2)
    if path:
        print(f"\nPath found: {path}")
    else:
        print("\nNo path found")
