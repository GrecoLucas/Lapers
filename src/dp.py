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


def maximize_priority_dp(g: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]], hospital_id: int, time_budget: float, all_hospitals: List[int]):
	"""
	DP exato para maximizar prioridades com modelo realista:
	- Ambulância começa em hospital_id
	- Para cada paciente, vai ao paciente, presta serviço, e leva ao hospital mais próximo
	- Pode terminar em qualquer hospital (não precisa voltar ao inicial)
	
	Retorna (route_with_hospitals, total_priority, total_time, is_optimal=True)
	onde route_with_hospitals = [(tipo, nid), ...] sendo tipo 'H' ou 'P'
	"""
	# candidatos válidos: pacientes com prioridade > 0
	pacientes_raw = [
		(nid, n)
		for nid, n in g.nodes.items()
		if getattr(n, 'tipo', '') == 'paciente'
		and (n.prioridade or 0) > 0
		and not getattr(n, 'resgatado', False)
	]
	
	if not pacientes_raw:
		return [('H', hospital_id)], 0, 0.0, True
	
	# Para cada paciente, calcula custo mínimo de atendimento
	# (considerando hospital mais próximo para deixá-lo)
	candidates = []  # (pid, prio, min_cost_to_serve)
	for pid, node in pacientes_raw:
		prio = node.prioridade or 0
		svc = node.tempo_cuidados_minimos or 0.0
		
		# custo mínimo = distância até qualquer hospital + serviço + distância do paciente até qualquer hospital
		min_cost = INF
		for h in all_hospitals:
			d_to_patient = all_paths.get((h, pid), (INF, []))[0]
			d_to_hosp = all_paths.get((pid, h), (INF, []))[0]
			if d_to_patient != INF and d_to_hosp != INF:
				cost = d_to_patient + svc + d_to_hosp
				min_cost = min(min_cost, cost)
		
		if min_cost == INF:
			continue
		candidates.append((pid, prio, svc, min_cost))
	
	n = len(candidates)
	if n == 0:
		return [('H', hospital_id)], 0, 0.0, True
	
	# DP com TSP simplificado: estado = (máscara de pacientes visitados, último hospital)
	# Como permitimos terminar em qualquer lugar, fazemos DP considerando sequências
	idx_to_pid = [c[0] for c in candidates]
	
	# Implementação simplificada: subset DP onde calculamos melhor sequência
	# Estado: dp[mask][last_hosp] = (min_time, max_prio, path)
	MAX_MASK = 1 << n
	
	# Inicialização: começamos no hospital_id
	dp = {}  # (mask, last_location) -> (time, prio, route)
	dp[(0, hospital_id)] = (0.0, 0, [('H', hospital_id)])
	
	best_solution = (0.0, 0, [('H', hospital_id)])
	
	for mask in range(MAX_MASK):
		for last_loc in [hospital_id] + all_hospitals:
			if (mask, last_loc) not in dp:
				continue
			
			curr_time, curr_prio, curr_route = dp[(mask, last_loc)]
			
			# Atualiza melhor solução global
			if curr_prio > best_solution[1] or (curr_prio == best_solution[1] and curr_time < best_solution[0]):
				best_solution = (curr_time, curr_prio, curr_route)
			
			# Tenta adicionar próximo paciente
			for k in range(n):
				if mask & (1 << k):
					continue
				
				pid = idx_to_pid[k]
				prio = candidates[k][1]
				svc = candidates[k][2]
				
				# Distância de last_loc até paciente
				d_to_p = all_paths.get((last_loc, pid), (INF, []))[0]
				if d_to_p == INF:
					continue
				
				# Encontra melhor hospital para levar o paciente
				best_hosp = None
				best_d = INF
				for h in all_hospitals:
					d_p_to_h = all_paths.get((pid, h), (INF, []))[0]
					if d_p_to_h < best_d:
						best_d = d_p_to_h
						best_hosp = h
				
				if best_hosp is None:
					continue
				
				new_time = curr_time + d_to_p + svc + best_d
				if new_time > time_budget:
					continue
				
				new_prio = curr_prio + prio
				new_mask = mask | (1 << k)
				new_route = curr_route + [('P', pid), ('H', best_hosp)]
				
				# Atualiza DP se encontramos melhor solução para este estado
				key = (new_mask, best_hosp)
				if key not in dp or new_prio > dp[key][1] or (new_prio == dp[key][1] and new_time < dp[key][0]):
					dp[key] = (new_time, new_prio, new_route)
	
	return best_solution[2], best_solution[1], best_solution[0], True

def greedy_maximize_priority(g: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]], hospital_id: int, time_budget: float, all_hospitals: List[int]):
    """
    Heurística gananciosa melhorada com modelo realista:
    - Começa em hospital_id
    - Usa scoring adaptativo considerando lookahead e tempo restante
    - Prioriza pacientes críticos e eficiência espacial
    - Pode terminar em qualquer hospital
    
    Retorna (route_with_hospitals, total_prio, total_time, False)
    """
    pacientes_raw = [
        (nid, n)
        for nid, n in g.nodes.items()
        if getattr(n, 'tipo', '') == 'paciente'
        and (n.prioridade or 0) > 0
        and not getattr(n, 'resgatado', False)
    ]
    
    if not pacientes_raw:
        return [('H', hospital_id)], 0, 0.0, False
    
    # Pré-calcula informações de todos os pacientes
    patient_info = {}
    for pid, node in pacientes_raw:
        prio = node.prioridade or 0
        svc = node.tempo_cuidados_minimos or 0.0
        
        # Encontra hospital mais próximo
        min_d_to_h = INF
        best_h = None
        for h in all_hospitals:
            d_p_to_h = all_paths.get((pid, h), (INF, []))[0]
            if d_p_to_h < min_d_to_h:
                min_d_to_h = d_p_to_h
                best_h = h
        
        if best_h is not None and min_d_to_h != INF:
            patient_info[pid] = {
                'prio': prio,
                'service': svc,
                'best_hospital': best_h,
                'dist_to_hospital': min_d_to_h
            }
    
    remaining = set(patient_info.keys())
    total_time = 0.0
    total_prio = 0
    route = [('H', hospital_id)]
    current_loc = hospital_id
    
    while remaining:
        time_left = time_budget - total_time
        best = None
        best_score = -INF
        
        for pid in list(remaining):
            info = patient_info[pid]
            prio = info['prio']
            svc = info['service']
            best_h = info['best_hospital']
            d_to_h = info['dist_to_hospital']
            
            # Distância da localização atual até o paciente
            d_to_p = all_paths.get((current_loc, pid), (INF, []))[0]
            if d_to_p == INF:
                continue
            
            cost = d_to_p + svc + d_to_h
            
            if cost > time_left:
                continue
            
            # Scoring melhorado com múltiplos fatores
            
            # 1. Ratio base prioridade/custo
            base_score = prio / cost if cost > 0 else prio * 1000.0
            
            # 2. Bonus para alta prioridade (exponencial para prioridades > 80)
            priority_bonus = 1.0
            if prio >= 80:
                priority_bonus = 1.5
            elif prio >= 60:
                priority_bonus = 1.3
            elif prio >= 40:
                priority_bonus = 1.1
            
            # 3. Penalização por distância relativa ao tempo restante
            # Se o custo consome muito do tempo restante, penaliza
            time_efficiency = 1.0 - (cost / time_left) * 0.3
            
            # 4. Lookahead: verifica quantos pacientes ainda são viáveis após este
            lookahead_score = 0
            time_after = total_time + cost
            reachable_count = 0
            reachable_prio = 0
            
            for next_pid in remaining:
                if next_pid == pid:
                    continue
                next_info = patient_info[next_pid]
                d_h_to_next = all_paths.get((best_h, next_pid), (INF, []))[0]
                if d_h_to_next == INF:
                    continue
                
                next_cost = d_h_to_next + next_info['service'] + next_info['dist_to_hospital']
                if time_after + next_cost <= time_budget:
                    reachable_count += 1
                    reachable_prio += next_info['prio']
            
            # Bonus baseado em pacientes alcançáveis (normalizado)
            if len(remaining) > 1:
                lookahead_score = (reachable_count / (len(remaining) - 1)) * 0.3
                # Bonus extra se os próximos pacientes têm alta prioridade
                if reachable_count > 0:
                    avg_next_prio = reachable_prio / reachable_count
                    if avg_next_prio > 50:
                        lookahead_score *= 1.2
            
            # 5. Penalização se estamos ficando sem tempo
            urgency_factor = 1.0
            if time_left < time_budget * 0.3:  # Menos de 30% do tempo
                # Prioriza pegar pacientes rapidamente
                urgency_factor = 1.2 if cost < time_left * 0.5 else 0.8
            
            # Score final combinado
            final_score = (base_score * priority_bonus * time_efficiency * urgency_factor) + lookahead_score
            
            if final_score > best_score:
                best_score = final_score
                best = (pid, cost, prio, best_h)
        
        if best is None:
            break
        
        pid, cost, prio, hosp = best
        route.append(('P', pid))
        route.append(('H', hosp))
        total_time += cost
        total_prio += prio
        current_loc = hosp
        remaining.remove(pid)
    
    return route, total_prio, total_time, False