import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
# pyrefly: ignore [missing-import]
import chromadb

from app.config import settings

logger = logging.getLogger("clyvo_ai.rag")

class RagService:
    """
    Serviço de RAG (Retrieval-Augmented Generation) com ChromaDB e base vetorial persistente.
    Segue PEP 8 com imports no topo e princípios SOLID.
    """

    def __init__(self):
        self.collection_name = "petguardian_vet_knowledge"
        self.chroma_client: Optional[chromadb.PersistentClient] = None
        self.collection = None
        self.documents_memory: List[Dict[str, Any]] = []
        self._is_initialized = False

    def initialize(self) -> None:
        """Carrega e indexa os documentos da base de conhecimento veterinário."""
        if self._is_initialized:
            return

        kb_dir = Path(settings.KNOWLEDGE_BASE_DIR)
        if not kb_dir.exists():
            logger.warning(f"Diretório da base de conhecimento não encontrado: {kb_dir}")
            return

        # 1. Leitura e Chunking dos arquivos Markdown
        chunks = self._load_and_chunk_documents(kb_dir)
        self.documents_memory = chunks

        # 2. Ingestão no ChromaDB (com persistência em disco)
        try:
            os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Base vetorial de conhecimento veterinário preventivo Clyvo"}
            )
            
            if chunks:
                self.collection.upsert(
                    ids=[c["id"] for c in chunks],
                    documents=[c["text"] for c in chunks],
                    metadatas=[c["metadata"] for c in chunks]
                )
            logger.info(f"RAG ChromaDB inicializado com sucesso: {len(chunks)} chunks indexados.")
        except Exception as e:
            logger.warning(f"Aviso na inicialização do ChromaDB (utilizando busca em memória): {e}")

        self._is_initialized = True

    def buscar_contexto_relevante(self, query: str, top_k: int = 3) -> List[str]:
        """Busca os trechos mais relevantes para a dúvida do tutor."""
        if not self._is_initialized:
            self.initialize()

        if not query.strip():
            return []

        # 1. Tentar busca semântica no ChromaDB
        if self.collection is not None:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=min(top_k, len(self.documents_memory)) if self.documents_memory else top_k
                )
                if results and results.get("documents") and len(results["documents"][0]) > 0:
                    return results["documents"][0]
            except Exception as e:
                logger.warning(f"Erro na busca vetorial ChromaDB, recorrendo ao fallback de texto: {e}")

        # 2. Fallback de busca semântica/léxica em memória (DRY)
        return self._search_memory(query, top_k)

    def get_total_documents_loaded(self) -> int:
        return len(self.documents_memory)

    @staticmethod
    def _load_and_chunk_documents(kb_dir: Path) -> List[Dict[str, Any]]:
        """Lê os arquivos Markdown e divide por seções temáticas."""
        chunks = []
        md_files = list(kb_dir.glob("*.md"))
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                sections = content.split("## ")
                doc_title = sections[0].replace("# ", "").strip()
                
                for idx, section in enumerate(sections[1:], start=1):
                    lines = section.split("\n", 1)
                    section_title = lines[0].strip()
                    section_body = lines[1].strip() if len(lines) > 1 else ""
                    
                    chunk_text = f"Fonte: {doc_title} | Seção: {section_title}\n{section_body}"
                    chunk_id = f"{file_path.stem}_sec_{idx}"
                    
                    chunks.append({
                        "id": chunk_id,
                        "text": chunk_text,
                        "metadata": {
                            "source_file": file_path.name,
                            "topic": doc_title,
                            "section": section_title
                        }
                    })
            except Exception as e:
                logger.error(f"Erro ao processar arquivo RAG {file_path}: {e}")

        return chunks

    def _search_memory(self, query: str, top_k: int) -> List[str]:
        """Busca léxica em memória com ranqueamento por similaridade de palavras-chave."""
        query_words = set(query.lower().split())
        scored_docs = []

        for doc in self.documents_memory:
            doc_text = doc["text"].lower()
            score = sum(1 for word in query_words if len(word) > 3 and word in doc_text)
            if score > 0:
                scored_docs.append((score, doc["text"]))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc[1] for doc in scored_docs[:top_k]]

rag_service = RagService()
