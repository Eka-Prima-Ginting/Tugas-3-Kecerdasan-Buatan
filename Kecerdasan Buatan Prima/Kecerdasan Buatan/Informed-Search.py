#!/usr/bin/env python3
"""
compare_informed_romania.py

Compare informed search algorithms on the Romania map (Arad -> Bucharest).

Algorithms:
- Greedy Best-First
- A*
- Weighted A*
- IDA* (Iterative Deepening A*)
- SMA* (simplified memory-bounded A*)
- Bidirectional A* (simple meet-in-the-middle)

Outputs: path, cost, nodes expanded, elapsed time (ms)
"""

import heapq
import time
from collections import deque

# -------------------------
# Romania graph (undirected)
# -------------------------
GRAPH = {
    "Arad": {"Zerind":75, "Sibiu":140, "Timisoara":118},
    "Zerind": {"Arad":75, "Oradea":71},
    "Oradea": {"Zerind":71, "Sibiu":151},
    "Sibiu": {"Arad":140, "Oradea":151, "Fagaras":99, "Rimnicu Vilcea":80},
    "Fagaras": {"Sibiu":99, "Bucharest":211},
    "Rimnicu Vilcea": {"Sibiu":80, "Pitesti":97, "Craiova":146},
    "Timisoara": {"Arad":118, "Lugoj":111},
    "Lugoj": {"Timisoara":111, "Mehadia":70},
    "Mehadia": {"Lugoj":70, "Drobeta":75},
    "Drobeta": {"Mehadia":75, "Craiova":120},
    "Craiova": {"Drobeta":120, "Rimnicu Vilcea":146, "Pitesti":138},
    "Pitesti": {"Rimnicu Vilcea":97, "Craiova":138, "Bucharest":101},
    "Bucharest": {"Fagaras":211, "Pitesti":101, "Giurgiu":90, "Urziceni":85},
    "Giurgiu": {"Bucharest":90},
    "Urziceni": {"Bucharest":85, "Hirsova":98, "Vaslui":142},
    "Hirsova": {"Urziceni":98, "Eforie":86},
    "Eforie": {"Hirsova":86},
    "Vaslui": {"Urziceni":142, "Iasi":92},
    "Iasi": {"Vaslui":92, "Neamt":87},
    "Neamt": {"Iasi":87}
}

# Straight-line distances (heuristic) to Bucharest
H = {
    "Arad":366, "Bucharest":0, "Craiova":160, "Drobeta":242, "Eforie":161,
    "Fagaras":176, "Giurgiu":77, "Hirsova":151, "Iasi":226, "Lugoj":244,
    "Mehadia":241, "Neamt":234, "Oradea":380, "Pitesti":100, "Rimnicu Vilcea":193,
    "Sibiu":253, "Timisoara":329, "Urziceni":80, "Vaslui":199, "Zerind":374
}

START = "Arad"
GOAL = "Bucharest"

# -------------------------
# Helpers
# -------------------------
def reconstruct_from_parent(parent, node):
    if node not in parent:
        return None
    path = [node]
    while parent[node] is not None:
        node = parent[node]
        path.append(node)
    path.reverse()
    return path

def path_cost(graph, path):
    if not path:
        return float('inf')
    cost = 0
    for i in range(len(path)-1):
        cost += graph[path[i]][path[i+1]]
    return cost

# -------------------------
# Greedy Best-First Search
# -------------------------
def greedy_best_first(graph, h, start, goal):
    t0 = time.time()
    open_pq = []
    heapq.heappush(open_pq, (h[start], start))
    parent = {start: None}
    closed = set()
    nodes_expanded = 0

    while open_pq:
        _, node = heapq.heappop(open_pq)
        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1
        if node == goal:
            path = reconstruct_from_parent(parent, node)
            return path, path_cost(graph, path), nodes_expanded, (time.time()-t0)*1000
        for nbr in graph.get(node, {}):
            if nbr not in closed:
                # set parent only first time to preserve simple path
                if nbr not in parent:
                    parent[nbr] = node
                heapq.heappush(open_pq, (h.get(nbr, 0), nbr))
    return None, float('inf'), nodes_expanded, (time.time()-t0)*1000

# -------------------------
# A* Search
# -------------------------
def a_star(graph, h, start, goal):
    t0 = time.time()
    open_pq = []
    heapq.heappush(open_pq, (h[start], 0, start))  # (f, g, node)
    parent = {start: None}
    gscore = {start: 0}
    closed = set()
    nodes_expanded = 0

    while open_pq:
        f, g, node = heapq.heappop(open_pq)
        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1
        if node == goal:
            path = reconstruct_from_parent(parent, node)
            return path, gscore[node], nodes_expanded, (time.time()-t0)*1000
        for nbr, w in graph.get(node, {}).items():
            tentative_g = gscore[node] + w
            if nbr not in gscore or tentative_g < gscore[nbr]:
                gscore[nbr] = tentative_g
                parent[nbr] = node
                heapq.heappush(open_pq, (tentative_g + h.get(nbr,0), tentative_g, nbr))
    return None, float('inf'), nodes_expanded, (time.time()-t0)*1000

# -------------------------
# Weighted A* (g + w*h)
# -------------------------
def weighted_a_star(graph, h, start, goal, weight=1.5):
    t0 = time.time()
    open_pq = []
    heapq.heappush(open_pq, (weight*h[start], 0, start))
    parent = {start: None}
    gscore = {start: 0}
    closed = set()
    nodes_expanded = 0

    while open_pq:
        f, g, node = heapq.heappop(open_pq)
        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1
        if node == goal:
            path = reconstruct_from_parent(parent, node)
            return path, gscore[node], nodes_expanded, (time.time()-t0)*1000
        for nbr, wcost in graph.get(node, {}).items():
            tentative_g = gscore[node] + wcost
            if nbr not in gscore or tentative_g < gscore[nbr]:
                gscore[nbr] = tentative_g
                parent[nbr] = node
                heapq.heappush(open_pq, (tentative_g + weight*h.get(nbr,0), tentative_g, nbr))
    return None, float('inf'), nodes_expanded, (time.time()-t0)*1000

# -------------------------
# IDA* (Iterative Deepening A*)
# -------------------------
def ida_star(graph, h, start, goal):
    t0 = time.time()
    bound = h[start]
    nodes_expanded = 0

    def search(path, g, bound):
        nonlocal nodes_expanded
        node = path[-1]
        f = g + h.get(node, 0)
        if f > bound:
            return f, None
        if node == goal:
            return True, path.copy()
        min_threshold = float('inf')
        for nbr, w in graph.get(node, {}).items():
            if nbr in path:
                continue
            nodes_expanded += 1
            path.append(nbr)
            t, result = search(path, g + w, bound)
            if result:
                return True, result
            if t < min_threshold:
                min_threshold = t
            path.pop()
        return min_threshold, None

    while True:
        t, result = search([start], 0, bound)
        if result:
            return result, path_cost(graph, result), nodes_expanded, (time.time()-t0)*1000
        if t == float('inf'):
            return None, float('inf'), nodes_expanded, (time.time()-t0)*1000
        bound = t

# -------------------------
# Simplified SMA* (memory-bounded A*)
#   - This is a simple approximate SMA*:
#     keep frontier up to memory_limit best f-values, drop worst.
# -------------------------
def sma_star(graph, h, start, goal, memory_limit=8):
    t0 = time.time()
    frontier = [(h[start], 0, start, [start])]  # (f, g, node, path)
    nodes_expanded = 0

    while frontier:
        # pop best (smallest f)
        frontier.sort(key=lambda x: x[0])
        f, g, node, path = frontier.pop(0)
        nodes_expanded += 1
        if node == goal:
            return path, g, nodes_expanded, (time.time()-t0)*1000
        # expand
        for nbr, w in graph.get(node, {}).items():
            if nbr in path:  # avoid cycles in path
                continue
            new_g = g + w
            new_f = new_g + h.get(nbr,0)
            frontier.append((new_f, new_g, nbr, path + [nbr]))
        # enforce memory limit (drop worst f entries)
        if len(frontier) > memory_limit:
            frontier.sort(key=lambda x: x[0])  # smallest first
            # drop from end until size ok
            while len(frontier) > memory_limit:
                frontier.pop()
    return None, float('inf'), nodes_expanded, (time.time()-t0)*1000

# -------------------------
# Bidirectional A* (simple meet-in-the-middle)
# -------------------------
def bidirectional_a_star(graph, h, start, goal):
    t0 = time.time()
    # forward and backward structures
    open_f = [(h[start], 0, start)]
    open_b = [(h[goal], 0, goal)]
    g_f = {start: 0}
    g_b = {goal: 0}
    parent_f = {start: None}
    parent_b = {goal: None}
    closed_f = {}
    closed_b = {}
    nodes_expanded = 0
    best_cost = float('inf')
    meeting = None

    while open_f or open_b:
        # choose side to expand (smaller top f)
        top_f = open_f[0][0] if open_f else float('inf')
        top_b = open_b[0][0] if open_b else float('inf')
        side = 'f' if top_f <= top_b else 'b'

        if side == 'f' and open_f:
            f, g, node = heapq.heappop(open_f)
            if node in closed_f:
                continue
            closed_f[node] = g_f[node]
            nodes_expanded += 1
            if node in closed_b:
                total = g_f[node] + closed_b[node]
                if total < best_cost:
                    best_cost = total
                    meeting = node
            for nbr, w in graph.get(node, {}).items():
                tentative = g_f[node] + w
                if tentative < g_f.get(nbr, float('inf')) and tentative < best_cost:
                    g_f[nbr] = tentative
                    parent_f[nbr] = node
                    heapq.heappush(open_f, (tentative + h.get(nbr,0), tentative, nbr))
        elif side == 'b' and open_b:
            f, g, node = heapq.heappop(open_b)
            if node in closed_b:
                continue
            closed_b[node] = g_b[node]
            nodes_expanded += 1
            if node in closed_f:
                total = g_b[node] + closed_f[node]
                if total < best_cost:
                    best_cost = total
                    meeting = node
            for nbr, w in graph.get(node, {}).items():
                tentative = g_b[node] + w
                if tentative < g_b.get(nbr, float('inf')) and tentative < best_cost:
                    g_b[nbr] = tentative
                    parent_b[nbr] = node
                    heapq.heappush(open_b, (tentative + h.get(nbr,0), tentative, nbr))

        # termination condition: smallest f on both sides >= best_cost
        min_f_f = open_f[0][0] if open_f else float('inf')
        min_f_b = open_b[0][0] if open_b else float('inf')
        if min(min_f_f, min_f_b) >= best_cost and meeting is not None:
            # reconstruct path
            # forward path to meeting
            path_f = []
            n = meeting
            while n is not None:
                path_f.append(n)
                n = parent_f.get(n)
            path_f.reverse()
            # backward path to meeting
            path_b = []
            n = meeting
            while n is not None:
                path_b.append(n)
                n = parent_b.get(n)
            # path_b is meeting -> goal, we need to append tail excluding meeting
            full = path_f + path_b[1:]
            return full, path_cost(GRAPH, full), nodes_expanded, (time.time()-t0)*1000

    return None, float('inf'), nodes_expanded, (time.time()-t0)*1000

# -------------------------
# Comparison runner
# -------------------------
def compare_all(start=START, goal=GOAL):
    experiments = [
        ("Greedy Best-First", lambda: greedy_best_first(GRAPH, H, start, goal)),
        ("A*", lambda: a_star(GRAPH, H, start, goal)),
        ("Weighted A* (w=1.5)", lambda: weighted_a_star(GRAPH, H, start, goal, 1.5)),
        ("IDA*", lambda: ida_star(GRAPH, H, start, goal)),
        ("SMA* (mem=8)", lambda: sma_star(GRAPH, H, start, goal, memory_limit=8)),
        ("Bidirectional A*", lambda: bidirectional_a_star(GRAPH, H, start, goal)),
    ]

    print("\n=== Comparing Informed Search Algorithms (Arad -> Bucharest) ===\n")
    for name, func in experiments:
        t_start = time.time()
        result = func()
        # results have varying tuple formats, normalize:
        # most return (path, cost, nodes_expanded, ms)
        # greedy returns (path, cost, nodes_expanded, ms) as well
        if result is None:
            print(f"{name}: No result returned")
            continue
        path, cost, nodes, ms = result
        # If ms looks like seconds (float small), we already compute ms above
        print(f"{name}:")
        print(f"  Path: {path}")
        print(f"  Cost: {cost}")
        print(f"  Nodes expanded: {nodes}")
        print(f"  Time elapsed: {ms:.3f} ms\n")

if __name__ == "__main__":
    compare_all()
