"""Conservative directed hazard reachability, not fracture/CFD/FEA physics.

Rates/delays are declared scenario parameters. A shut barrier blocks its edge.
"""

import heapq
from .numeric import scalar

KINDS = {"crack", "leak", "load", "thermal"}


def trace_hazards(nodes, edges, origin, *, horizon_s, closed_barriers=()):
    if len(set(nodes)) != len(nodes) or origin not in nodes:
        raise ValueError("invalid hazard nodes/origin")
    horizon = scalar(horizon_s, lower=0)
    adjacency = {n: [] for n in nodes}
    for e in edges:
        if (
            set(e) != {"from", "to", "kind", "delay_s", "barrier"}
            or e["from"] not in adjacency
            or e["to"] not in adjacency
            or e["kind"] not in KINDS
        ):
            raise ValueError("invalid hazard edge")
        delay = scalar(e["delay_s"], lower=1e-12)
        if e["barrier"] not in closed_barriers:
            adjacency[e["from"]].append((e["to"], delay, e["kind"]))
    best = {origin: 0.0}
    parent = {}
    queue = [(0.0, origin)]
    while queue:
        t, n = heapq.heappop(queue)
        if t != best[n]:
            continue
        for dest, delay, kind in adjacency[n]:
            nxt = t + delay
            if nxt <= horizon and nxt < best.get(dest, float("inf")):
                best[dest] = nxt
                parent[dest] = {"from": n, "kind": kind}
                heapq.heappush(queue, (nxt, dest))
    return {
        "reachable": [
            {"node": n, "earliest_s": t, "via": parent.get(n)}
            for n, t in sorted(best.items(), key=lambda x: (x[1], x[0]))
        ],
        "scope": "DECLARED_GRAPH_REACHABILITY__NOT_PHYSICAL_PROPAGATION",
    }
