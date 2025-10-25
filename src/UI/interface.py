
"""UI helpers: draw the project's Graph using NetworkX and Matplotlib.

Provides a convenience function `draw_graph(graph, show=True, save_path=None)`
that converts the project's Graph to a networkx.Graph and renders it.

Notes:
- This module imports networkx and matplotlib when used. If they are not
  installed the import will raise ImportError; install via `pip install networkx matplotlib`.
"""
from typing import Optional, Tuple, Dict

try:
	import networkx as nx
	import matplotlib.pyplot as plt
except Exception as e:
	# Defer import errors until the function is used; keep module importable for non-UI runs.
	nx = None  # type: ignore
	plt = None  # type: ignore


def _ensure_nx():
	if nx is None or plt is None:
		raise ImportError("NetworkX and Matplotlib are required for drawing. Install with: pip install networkx matplotlib")


def draw_graph(graph, show: bool = True, save_path: Optional[str] = None) -> Tuple[Dict[int, Tuple[float, float]], 'nx.Graph']:
	"""Draw the given `Graph` instance using NetworkX.

	Returns (pos, nx_graph) where pos is the layout positions used and nx_graph
	is the created networkx.Graph object. Colors hospitals differently and
	scales patient nodes by priority when available.

	Parameters
	- graph: the project's Graph instance (see `src/graph.py`).
	- show: whether to call `plt.show()`.
	- save_path: if provided, save the figure to this path instead of/in addition to showing.
	"""
	_ensure_nx()

	nx_g = nx.Graph()

	# Add nodes with attributes
	for nid, node in getattr(graph, "nodes", {}).items():
		attrs = {
			"label": getattr(node, "nome", str(nid)) or str(nid),
			"tipo": getattr(node, "tipo", ""),
			"prioridade": getattr(node, "prioridade", None),
			"is_hospital": getattr(node, "is_hospital", False),
		}
		nx_g.add_node(nid, **attrs)

	# Add edges from adjacency
	adjacency = getattr(graph, "adjacency", {})
	for u, neighs in adjacency.items():
		for (v, w) in neighs:
			# avoid duplicate edges in undirected graph: add only when u <= v
			if nx_g.has_edge(u, v) or u == v:
				continue
			nx_g.add_edge(u, v, weight=float(w))

	# Layout - try spring layout; deterministic seed for reproducibility
	pos = nx.spring_layout(nx_g, seed=42)

	# Node styling
	node_colors = []
	node_sizes = []
	labels = {}
	for n, data in nx_g.nodes(data=True):
		is_h = data.get("is_hospital", False)
		prio = data.get("prioridade") or 1
		node_colors.append("tab:red" if is_h else "tab:blue")
		# size base 200; scale by prioridade if present
		try:
			size = 200 + (int(prio) * 100 if prio is not None else 0)
		except Exception:
			size = 200
		node_sizes.append(size)
		labels[n] = data.get("label", str(n))

	fig, ax = plt.subplots(figsize=(10, 7))
	nx.draw_networkx_nodes(nx_g, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
	nx.draw_networkx_edges(nx_g, pos, ax=ax, alpha=0.6)
	nx.draw_networkx_labels(nx_g, pos, labels=labels, font_size=8, ax=ax)

	# draw edge weights
	edge_labels = {(u, v): f"{d.get('weight', 1):.1f}" for u, v, d in nx_g.edges(data=True)}
	nx.draw_networkx_edge_labels(nx_g, pos, edge_labels=edge_labels, font_size=7, ax=ax)

	ax.set_title("Graph visualization")
	ax.axis("off")

	if save_path:
		fig.savefig(save_path, bbox_inches="tight")

	if show:
		plt.show()

	return pos, nx_g


__all__ = ["draw_graph"]
