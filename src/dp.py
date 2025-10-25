from typing import Dict, List, Tuple, Optional

from graph import Graph

INF = float('inf')


def read_time_budget(path) -> Optional[float]:
	"""Lê tempo_total de dados_iniciais.csv (se existir)."""
	import csv
	try:
		with open(path, newline='', encoding='utf-8') as f:
			rdr = csv.DictReader(f)
			for row in rdr:
				# formatos suportados: 'tempo_total' ou segunda coluna
				if 'tempo_total' in row and row['tempo_total'] not in (None, ''):
					try:
						return float(row['tempo_total'])
					except Exception:
						pass
				vals = list(row.values())
				if len(vals) >= 2 and vals[1] not in (None, ''):
					try:
						return float(vals[1])
					except Exception:
						pass
	except FileNotFoundError:
		return None
	return None


def build_distance_lookup(all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]], nodes: List[int]) -> Dict[Tuple[int, int], float]:
	dist: Dict[Tuple[int, int], float] = {}
	for u in nodes:
		for v in nodes:
			if u == v:
				dist[(u, v)] = 0.0
			else:
				d = all_paths.get((u, v), (INF, []))[0]
				dist[(u, v)] = d if d is not None else INF
	return dist


def maximize_priority_dp(g: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]], hospital_id: int, time_budget: float):
	"""
	DP exato (por subconjuntos) para maximizar soma de prioridades quando cada atendimento é uma viagem redonda:
	hospital -> paciente -> hospital, custando: d(h,p) + serviço(p) + d(p,h).
	Retorna (route_node_ids, total_priority, total_time, is_optimal=True), onde route_node_ids = [hospital] + [paciente1, paciente2, ...].
	"""
	# candidatos válidos: pacientes alcançáveis de ida e volta com prioridade > 0
	pacientes_raw = [
		(nid, n)
		for nid, n in g.nodes.items()
		if getattr(n, 'tipo', '') == 'paciente'
		and (n.prioridade or 0) > 0
		and not getattr(n, 'resgatado', False)
	]
	candidates = []  # (nid, prio, svc, cost_roundtrip)
	for nid, node in pacientes_raw:
		d_hp = all_paths.get((hospital_id, nid), (INF, []))[0]
		d_ph = all_paths.get((nid, hospital_id), (INF, []))[0]
		if d_hp == INF or d_ph == INF:
			continue
		svc = node.tempo_cuidados_minimos or 0.0
		cost = d_hp + svc + d_ph
		candidates.append((nid, node.prioridade or 0, svc, cost))

	n = len(candidates)
	if n == 0:
		return [hospital_id], 0, 0.0, True

	idx_to_nid = [c[0] for c in candidates]
	prioridades = [c[1] for c in candidates]
	costs = [c[3] for c in candidates]

	# Subset DP: escolhe subconjunto com custo total <= budget e prioridade máxima
	MAX_MASK = 1 << n
	# Guardamos o custo total por máscara (INF se inviável)
	cost_mask = [INF] * MAX_MASK
	cost_mask[0] = 0.0
	# prioridade acumulada da máscara
	prio_mask = [0] * MAX_MASK
	# parent para reconstruir
	parent = [(-1, -1)] * MAX_MASK  # (prev_mask, added_idx)

	for m in range(MAX_MASK):
		if cost_mask[m] == INF:
			continue
		# tenta adicionar um item k não presente
		for k in range(n):
			if m & (1 << k):
				continue
			new_m = m | (1 << k)
			new_cost = cost_mask[m] + costs[k]
			if new_cost > time_budget:
				continue
			new_prio = prio_mask[m] + prioridades[k]
			# melhora se maior prioridade; empate por menor custo
			if new_prio > prio_mask[new_m] or (new_prio == prio_mask[new_m] and new_cost < cost_mask[new_m]):
				prio_mask[new_m] = new_prio
				cost_mask[new_m] = new_cost
				parent[new_m] = (m, k)

	# escolhe melhor máscara
	best_m = 0
	best_prio = 0
	best_cost = 0.0
	for m in range(MAX_MASK):
		if cost_mask[m] == INF:
			continue
		if prio_mask[m] > best_prio or (prio_mask[m] == best_prio and cost_mask[m] < best_cost):
			best_prio = prio_mask[m]
			best_cost = cost_mask[m]
			best_m = m

	if best_prio == 0:
		return [hospital_id], 0, 0.0, True

	# reconstrói conjunto de pacientes
	sel_idx: List[int] = []
	m = best_m
	while m != 0:
		pm, k = parent[m]
		if pm == -1 or k == -1:
			break
		sel_idx.append(k)
		m = pm
	sel_idx.reverse()

	route = [hospital_id] + [idx_to_nid[i] for i in sel_idx]
	return route, best_prio, best_cost, True


def greedy_maximize_priority(g: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]], hospital_id: int, time_budget: float):
	"""
	Heurística gananciosa: escolhe próximo paciente pelo maior quociente prioridade / (d(h,p) + svc + d(p,h)),
	acumulando enquanto houver budget. Retorna (route, total_prio, total_time, False).
	"""
	pacientes_raw = [
		(nid, n)
		for nid, n in g.nodes.items()
		if getattr(n, 'tipo', '') == 'paciente'
		and (n.prioridade or 0) > 0
		and not getattr(n, 'resgatado', False)
	]
	items = []  # (nid, cost_roundtrip, prio)
	for nid, node in pacientes_raw:
		d_hp = all_paths.get((hospital_id, nid), (INF, []))[0]
		d_ph = all_paths.get((nid, hospital_id), (INF, []))[0]
		if d_hp == INF or d_ph == INF:
			continue
		svc = node.tempo_cuidados_minimos or 0.0
		cost = d_hp + svc + d_ph
		items.append((nid, cost, node.prioridade or 0))

	remaining = set(nid for nid, _, _ in items)
	total_time = 0.0
	total_prio = 0
	route = [hospital_id]

	while remaining:
		best = None
		best_score = -1.0
		for nid in list(remaining):
			cost = next(c for (x, c, _) in items if x == nid)
			prio = next(p for (x, _, p) in items if x == nid)
			if total_time + cost > time_budget:
				continue
			score = prio / cost if cost > 0 else prio * 1000.0
			if score > best_score:
				best_score = score
				best = (nid, cost, prio)
		if best is None:
			break
		nid, cost, prio = best
		route.append(nid)
		total_time += cost
		total_prio += prio
		remaining.remove(nid)

	return route, total_prio, total_time, False

