from collections import deque
import heapq

# -----------------------------------------
# ROMANIA MAP GRAPH (Edges with cost)
# -----------------------------------------
romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# -------------------------------------------------------------------
# 1. BFS (Breadth-First Search)
# -------------------------------------------------------------------
def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    expanded = 0

    while queue:
        node, path = queue.popleft()
        expanded += 1

        if node == goal:
            return path, expanded

        visited.add(node)
        for neighbor in romania_map[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None, expanded


# -------------------------------------------------------------------
# 2. DFS (Depth-First Search)
# -------------------------------------------------------------------
def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    expanded = 0

    while stack:
        node, path = stack.pop()
        expanded += 1

        if node == goal:
            return path, expanded

        visited.add(node)
        for neighbor in romania_map[node]:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None, expanded


# -------------------------------------------------------------------
# 3. Uniform-Cost Search (Dijkstra)
# -------------------------------------------------------------------
def ucs(start, goal):
    pq = [(0, start, [start])]
    visited = {}
    expanded = 0

    while pq:
        cost, node, path = heapq.heappop(pq)
        expanded += 1

        if node == goal:
            return path, cost, expanded

        if node in visited and visited[node] <= cost:
            continue

        visited[node] = cost

        for neighbor, weight in romania_map[node].items():
            heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return None, None, expanded


# -------------------------------------------------------------------
# 4. Depth-Limited Search (DLS)
# -------------------------------------------------------------------
def dls(node, goal, limit, path, expanded):
    expanded[0] += 1

    if node == goal:
        return path

    if limit <= 0:
        return None

    for neighbor in romania_map[node]:
        result = dls(neighbor, goal, limit - 1, path + [neighbor], expanded)
        if result is not None:
            return result

    return None


# -------------------------------------------------------------------
# 5. Iterative Deepening Search (IDS)
# -------------------------------------------------------------------
def ids(start, goal, max_depth=20):
    for depth in range(max_depth):
        expanded = [0]
        result = dls(start, goal, depth, [start], expanded)
        if result is not None:
            return result, expanded[0], depth
    return None, None, None


# -------------------------------------------------------------------
# 6. Bidirectional Search (BFS-based)
# -------------------------------------------------------------------
def bidirectional_search(start, goal):
    front = {start: [start]}
    back = {goal: [goal]}

    front_queue = deque([start])
    back_queue = deque([goal])

    expanded = 0

    while front_queue and back_queue:
        # Expand front
        f = front_queue.popleft()
        expanded += 1

        for n in romania_map[f]:
            if n not in front:
                front[n] = front[f] + [n]
                front_queue.append(n)

                if n in back:
                    return front[n] + back[n][::-1][1:], expanded

        # Expand back
        b = back_queue.popleft()
        expanded += 1

        for n in romania_map[b]:
            if n not in back:
                back[n] = back[b] + [n]
                back_queue.append(n)

                if n in front:
                    return front[n] + back[n][::-1][1:], expanded

    return None, expanded


# -------------------------------------------------------------------
# COMPARISON FUNCTION
# -------------------------------------------------------------------
def compare_uninformed(start="Arad", goal="Bucharest"):
    print("\n===== COMPARING UNINFORMED SEARCH ALGORITHMS =====\n")

    # 1. BFS
    bfs_path, bfs_exp = bfs(start, goal)
    print(f"BFS Path: {bfs_path}  |  Nodes Expanded: {bfs_exp}")

    # 2. DFS
    dfs_path, dfs_exp = dfs(start, goal)
    print(f"DFS Path: {dfs_path}  |  Nodes Expanded: {dfs_exp}")

    # 3. UCS / Dijkstra
    ucs_path, ucs_cost, ucs_exp = ucs(start, goal)
    print(f"UCS Path: {ucs_path}  |  Cost: {ucs_cost}  |  Nodes Expanded: {ucs_exp}")

    # 4. DLS (limit=4)
    dls_exp = [0]
    dls_path = dls(start, goal, 4, [start], dls_exp)
    print(f"DLS Path (limit=4): {dls_path}  |  Nodes Expanded: {dls_exp[0]}")

    # 5. IDS
    ids_path, ids_exp, depth = ids(start, goal)
    print(f"IDS Path: {ids_path}  |  Depth Found: {depth}  |  Nodes Expanded: {ids_exp}")

    # 6. Bidirectional Search
    bi_path, bi_exp = bidirectional_search(start, goal)
    print(f"Bidirectional Path: {bi_path}  |  Nodes Expanded: {bi_exp}")


# -------------------------------------------------------------------
# RUN COMPARISON
# -------------------------------------------------------------------
if __name__ == "__main__":
    compare_uninformed()
