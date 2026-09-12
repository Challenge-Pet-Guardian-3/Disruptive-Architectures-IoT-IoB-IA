"""
Repositório de Persistência do Chat e Auditoria de Triagens
"""
import logging
from typing import Optional, List, Dict, Any
from src.database.connection import get_db_connection

logger = logging.getLogger("GuardianAI.ChatRepository")

class ChatRepository:
    """
    Encapsula todas as operações de banco de dados para mensagens de chat
    e auditoria de triagens clínicas, garantindo SRP e isolamento de SQL.
    """

    @staticmethod
    def salvar_mensagem(
        session_id: str,
        sender: str,
        text: str,
        pet_id: Optional[int] = None
    ) -> bool:
        """
        Registra uma mensagem individual no histórico do SQLite.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO mensagens_chat (session_id, pet_id, sender, text)
                    VALUES (?, ?, ?, ?)
                """, (session_id, pet_id, sender, text))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erro ao salvar mensagem no SQLite: {e}")
            return False

    @staticmethod
    def salvar_auditoria(
        session_id: str,
        pergunta: str,
        resposta: str,
        categoria: str,
        urgencia: str,
        origem_resposta: str,
        pet_id: Optional[int] = None,
        nome_pet: Optional[str] = None
    ) -> bool:
        """
        Registra o parecer e metadados da triagem clínica na tabela de auditoria.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO auditoria_triagens (
                        session_id, pet_id, nome_pet, pergunta, resposta,
                        categoria, urgencia, origem_resposta
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, pet_id, nome_pet, pergunta, resposta,
                    categoria, urgencia, origem_resposta
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erro ao registrar auditoria no SQLite: {e}")
            return False

    @staticmethod
    def buscar_historico(
        session_id: Optional[str] = None,
        pet_id: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Recupera as mensagens filtradas por session_id ou pet_id em ordem cronológica.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                if session_id and pet_id:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, sender, text, timestamp
                        FROM mensagens_chat
                        WHERE session_id = ? AND pet_id = ?
                        ORDER BY id ASC
                        LIMIT ?
                    """, (session_id, pet_id, limit))
                elif session_id:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, sender, text, timestamp
                        FROM mensagens_chat
                        WHERE session_id = ?
                        ORDER BY id ASC
                        LIMIT ?
                    """, (session_id, limit))
                elif pet_id:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, sender, text, timestamp
                        FROM mensagens_chat
                        WHERE pet_id = ?
                        ORDER BY id ASC
                        LIMIT ?
                    """, (pet_id, limit))
                else:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, sender, text, timestamp
                        FROM mensagens_chat
                        ORDER BY id DESC
                        LIMIT ?
                    """, (limit,))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao buscar histórico no SQLite: {e}")
            return []

    @staticmethod
    def listar_auditorias(
        pet_id: Optional[int] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Recupera os registros de auditoria clínica mais recentes.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                if pet_id:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, nome_pet, pergunta, resposta,
                               categoria, urgencia, origem_resposta, timestamp
                        FROM auditoria_triagens
                        WHERE pet_id = ?
                        ORDER BY id DESC
                        LIMIT ?
                    """, (pet_id, limit))
                else:
                    cursor.execute("""
                        SELECT id, session_id, pet_id, nome_pet, pergunta, resposta,
                               categoria, urgencia, origem_resposta, timestamp
                        FROM auditoria_triagens
                        ORDER BY id DESC
                        LIMIT ?
                    """, (limit,))

                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erro ao listar auditorias no SQLite: {e}")
            return []
