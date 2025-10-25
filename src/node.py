from typing import Optional

class Node:
    def __init__(
        self,
        id: int,
        tipo: str = "",
        nome: str = "",
        prioridade: Optional[int] = None,
        tempo_cuidados_minimos: Optional[float] = None,
        is_hospital: bool = False,
    ):
        self.id = id
        self.tipo = tipo
        self.nome = nome
        self.prioridade = prioridade
        self.tempo_cuidados_minimos = tempo_cuidados_minimos
        self.is_hospital = is_hospital

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nome": self.nome,
            "prioridade": self.prioridade,
            "tempo_cuidados_minimos": self.tempo_cuidados_minimos,
            "is_hospital": self.is_hospital,
        }

    def __repr__(self) -> str:
        return f"Node(id={self.id}, nome={self.nome!r}, tipo={self.tipo!r})"
