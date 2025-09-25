# core/assignment_engine.py
import hashlib
import random
from typing import Optional

class AssignmentEngine:
    def __init__(self, salt: str = "ab-test-salt"):
        self.salt = salt
    
    def assign_variant(self, user_id: str, experiment_id: str, variants: List) -> str:
        """
        Atribui consistentemente um usuário a uma variante usando hashing
        """
        # Criar hash consistente
        hash_input = f"{user_id}:{experiment_id}:{self.salt}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()
        hash_int = int(hash_value[:8], 16)
        
        # Atribuir baseado no hash
        variant_index = hash_int % len(variants)
        return variants[variant_index]['name']
    
    def get_assignment(self, user_id: str, experiment_id: str) -> Optional[str]:
        """Recupera a atribuição de um usuário"""
        # Verificar se já foi atribuído
        existing = self.get_existing_assignment(user_id, experiment_id)
        if existing:
            return existing
        
        # Nova atribuição
        return self.assign_variant(user_id, experiment_id)