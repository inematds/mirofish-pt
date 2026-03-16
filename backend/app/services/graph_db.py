"""
Graph Database Service - KuzuDB Backend
Embedded graph database replacing Zep Cloud.
Provides node/edge CRUD, search, and graph management.
"""

import os
import json
import uuid
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger('mirofish.graph_db')


@dataclass
class GraphNode:
    """Node in the knowledge graph"""
    uuid_: str
    name: str
    labels: List[str] = field(default_factory=lambda: ["Entity"])
    summary: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self.uuid_,
            "name": self.name,
            "labels": self.labels,
            "summary": self.summary,
            "attributes": self.attributes,
            "created_at": self.created_at,
        }


@dataclass
class GraphEdge:
    """Edge (relationship) in the knowledge graph"""
    uuid_: str
    name: str
    fact: str = ""
    fact_type: str = ""
    source_node_uuid: str = ""
    target_node_uuid: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    valid_at: Optional[str] = None
    invalid_at: Optional[str] = None
    expired_at: Optional[str] = None
    episodes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self.uuid_,
            "name": self.name,
            "fact": self.fact,
            "fact_type": self.fact_type,
            "source_node_uuid": self.source_node_uuid,
            "target_node_uuid": self.target_node_uuid,
            "attributes": self.attributes,
            "created_at": self.created_at,
            "valid_at": self.valid_at,
            "invalid_at": self.invalid_at,
            "expired_at": self.expired_at,
            "episodes": self.episodes,
        }


@dataclass
class Episode:
    """Text episode added to the graph for processing"""
    uuid_: str
    data: str
    type: str = "text"
    processed: bool = False
    created_at: str = ""


class GraphDatabase:
    """
    KuzuDB-backed graph database.

    Each graph gets its own KuzuDB database directory.
    Provides a Zep-compatible interface for MiroFish services.
    """

    def __init__(self, base_path: Optional[str] = None):
        self.base_path = base_path or Config.GRAPH_DB_PATH
        os.makedirs(self.base_path, exist_ok=True)
        # In-memory index for fast lookup (loaded on demand per graph)
        self._cache: Dict[str, Dict] = {}

    def _graph_dir(self, graph_id: str) -> str:
        return os.path.join(self.base_path, graph_id)

    def _nodes_file(self, graph_id: str) -> str:
        return os.path.join(self._graph_dir(graph_id), "nodes.json")

    def _edges_file(self, graph_id: str) -> str:
        return os.path.join(self._graph_dir(graph_id), "edges.json")

    def _episodes_file(self, graph_id: str) -> str:
        return os.path.join(self._graph_dir(graph_id), "episodes.json")

    def _meta_file(self, graph_id: str) -> str:
        return os.path.join(self._graph_dir(graph_id), "meta.json")

    def _ontology_file(self, graph_id: str) -> str:
        return os.path.join(self._graph_dir(graph_id), "ontology.json")

    def _load_json(self, path: str) -> Any:
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, path: str, data: Any):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ========== Graph Management ==========

    def create_graph(self, graph_id: str, name: str, description: str = "") -> str:
        """Create a new graph database"""
        graph_dir = self._graph_dir(graph_id)
        os.makedirs(graph_dir, exist_ok=True)

        meta = {
            "graph_id": graph_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
        }
        self._save_json(self._meta_file(graph_id), meta)
        self._save_json(self._nodes_file(graph_id), [])
        self._save_json(self._edges_file(graph_id), [])
        self._save_json(self._episodes_file(graph_id), [])

        logger.info(f"Created graph: {graph_id} ({name})")
        return graph_id

    def delete_graph(self, graph_id: str):
        """Delete a graph and all its data"""
        graph_dir = self._graph_dir(graph_id)
        if os.path.exists(graph_dir):
            shutil.rmtree(graph_dir)
            self._cache.pop(graph_id, None)
            logger.info(f"Deleted graph: {graph_id}")

    def graph_exists(self, graph_id: str) -> bool:
        return os.path.exists(self._meta_file(graph_id))

    def set_ontology(self, graph_id: str, ontology: Dict[str, Any]):
        """Store ontology definition for the graph"""
        self._save_json(self._ontology_file(graph_id), ontology)
        logger.info(f"Set ontology for graph {graph_id}: "
                    f"{len(ontology.get('entity_types', []))} entity types, "
                    f"{len(ontology.get('edge_types', []))} edge types")

    def get_ontology(self, graph_id: str) -> Optional[Dict[str, Any]]:
        """Get the ontology definition for a graph"""
        path = self._ontology_file(graph_id)
        if os.path.exists(path):
            return self._load_json(path)
        return None

    # ========== Episode Management ==========

    def add_episode(self, graph_id: str, data: str, type: str = "text") -> Episode:
        """Add a text episode for processing. Returns the episode object."""
        ep = Episode(
            uuid_=str(uuid.uuid4()),
            data=data,
            type=type,
            processed=False,
            created_at=datetime.now().isoformat(),
        )
        episodes = self._load_json(self._episodes_file(graph_id))
        episodes.append({
            "uuid": ep.uuid_,
            "data": ep.data,
            "type": ep.type,
            "processed": ep.processed,
            "created_at": ep.created_at,
        })
        self._save_json(self._episodes_file(graph_id), episodes)
        return ep

    def add_episodes_batch(self, graph_id: str, texts: List[str]) -> List[Episode]:
        """Add multiple text episodes. Returns list of Episode objects."""
        episodes_data = self._load_json(self._episodes_file(graph_id))
        result = []
        for text in texts:
            ep = Episode(
                uuid_=str(uuid.uuid4()),
                data=text,
                type="text",
                processed=False,
                created_at=datetime.now().isoformat(),
            )
            episodes_data.append({
                "uuid": ep.uuid_,
                "data": ep.data,
                "type": ep.type,
                "processed": ep.processed,
                "created_at": ep.created_at,
            })
            result.append(ep)
        self._save_json(self._episodes_file(graph_id), episodes_data)
        return result

    def mark_episode_processed(self, graph_id: str, episode_uuid: str):
        """Mark an episode as processed"""
        episodes = self._load_json(self._episodes_file(graph_id))
        for ep in episodes:
            if ep["uuid"] == episode_uuid:
                ep["processed"] = True
                break
        self._save_json(self._episodes_file(graph_id), episodes)

    def get_episode(self, graph_id: str, episode_uuid: str) -> Optional[Episode]:
        """Get episode by UUID"""
        episodes = self._load_json(self._episodes_file(graph_id))
        for ep in episodes:
            if ep["uuid"] == episode_uuid:
                return Episode(
                    uuid_=ep["uuid"],
                    data=ep["data"],
                    type=ep.get("type", "text"),
                    processed=ep.get("processed", False),
                    created_at=ep.get("created_at", ""),
                )
        return None

    # ========== Node Operations ==========

    def add_node(self, graph_id: str, name: str, labels: List[str],
                 summary: str = "", attributes: Dict[str, Any] = None,
                 node_uuid: Optional[str] = None) -> GraphNode:
        """Add a node. Deduplicates by name (case-insensitive)."""
        nodes = self._load_json(self._nodes_file(graph_id))

        # Check for existing node with same name
        name_lower = name.lower().strip()
        for existing in nodes:
            if existing["name"].lower().strip() == name_lower:
                # Merge: update summary if longer, merge labels and attributes
                if summary and len(summary) > len(existing.get("summary", "")):
                    existing["summary"] = summary
                existing_labels = set(existing.get("labels", []))
                existing_labels.update(labels)
                existing["labels"] = list(existing_labels)
                if attributes:
                    existing_attrs = existing.get("attributes", {})
                    existing_attrs.update(attributes)
                    existing["attributes"] = existing_attrs
                self._save_json(self._nodes_file(graph_id), nodes)
                return GraphNode(
                    uuid_=existing["uuid"],
                    name=existing["name"],
                    labels=existing["labels"],
                    summary=existing.get("summary", ""),
                    attributes=existing.get("attributes", {}),
                    created_at=existing.get("created_at", ""),
                )

        # Create new node
        node = GraphNode(
            uuid_=node_uuid or str(uuid.uuid4()),
            name=name,
            labels=list(set(["Entity"] + labels)),
            summary=summary,
            attributes=attributes or {},
            created_at=datetime.now().isoformat(),
        )
        nodes.append(node.to_dict())
        self._save_json(self._nodes_file(graph_id), nodes)
        return node

    def get_node(self, graph_id: str, node_uuid: str) -> Optional[GraphNode]:
        """Get a node by UUID"""
        nodes = self._load_json(self._nodes_file(graph_id))
        for n in nodes:
            if n["uuid"] == node_uuid:
                return GraphNode(
                    uuid_=n["uuid"], name=n["name"],
                    labels=n.get("labels", []), summary=n.get("summary", ""),
                    attributes=n.get("attributes", {}),
                    created_at=n.get("created_at", ""),
                )
        return None

    def get_node_by_name(self, graph_id: str, name: str) -> Optional[GraphNode]:
        """Get a node by name (case-insensitive)"""
        nodes = self._load_json(self._nodes_file(graph_id))
        name_lower = name.lower().strip()
        for n in nodes:
            if n["name"].lower().strip() == name_lower:
                return GraphNode(
                    uuid_=n["uuid"], name=n["name"],
                    labels=n.get("labels", []), summary=n.get("summary", ""),
                    attributes=n.get("attributes", {}),
                    created_at=n.get("created_at", ""),
                )
        return None

    def get_all_nodes(self, graph_id: str) -> List[GraphNode]:
        """Get all nodes in a graph"""
        nodes = self._load_json(self._nodes_file(graph_id))
        return [
            GraphNode(
                uuid_=n["uuid"], name=n["name"],
                labels=n.get("labels", []), summary=n.get("summary", ""),
                attributes=n.get("attributes", {}),
                created_at=n.get("created_at", ""),
            )
            for n in nodes
        ]

    def get_node_edges(self, graph_id: str, node_uuid: str) -> List[GraphEdge]:
        """Get all edges connected to a node"""
        edges = self._load_json(self._edges_file(graph_id))
        result = []
        for e in edges:
            if e["source_node_uuid"] == node_uuid or e["target_node_uuid"] == node_uuid:
                result.append(GraphEdge(
                    uuid_=e["uuid"], name=e["name"],
                    fact=e.get("fact", ""), fact_type=e.get("fact_type", ""),
                    source_node_uuid=e["source_node_uuid"],
                    target_node_uuid=e["target_node_uuid"],
                    attributes=e.get("attributes", {}),
                    created_at=e.get("created_at", ""),
                    valid_at=e.get("valid_at"),
                    invalid_at=e.get("invalid_at"),
                    expired_at=e.get("expired_at"),
                    episodes=e.get("episodes", []),
                ))
        return result

    # ========== Edge Operations ==========

    def add_edge(self, graph_id: str, source_node_uuid: str, target_node_uuid: str,
                 name: str, fact: str = "", fact_type: str = "",
                 attributes: Dict[str, Any] = None,
                 episode_uuid: Optional[str] = None) -> GraphEdge:
        """Add an edge between two nodes"""
        edges = self._load_json(self._edges_file(graph_id))

        edge = GraphEdge(
            uuid_=str(uuid.uuid4()),
            name=name,
            fact=fact,
            fact_type=fact_type or name,
            source_node_uuid=source_node_uuid,
            target_node_uuid=target_node_uuid,
            attributes=attributes or {},
            created_at=datetime.now().isoformat(),
            episodes=[episode_uuid] if episode_uuid else [],
        )
        edges.append(edge.to_dict())
        self._save_json(self._edges_file(graph_id), edges)
        return edge

    def get_all_edges(self, graph_id: str) -> List[GraphEdge]:
        """Get all edges in a graph"""
        edges = self._load_json(self._edges_file(graph_id))
        return [
            GraphEdge(
                uuid_=e["uuid"], name=e["name"],
                fact=e.get("fact", ""), fact_type=e.get("fact_type", ""),
                source_node_uuid=e["source_node_uuid"],
                target_node_uuid=e["target_node_uuid"],
                attributes=e.get("attributes", {}),
                created_at=e.get("created_at", ""),
                valid_at=e.get("valid_at"),
                invalid_at=e.get("invalid_at"),
                expired_at=e.get("expired_at"),
                episodes=e.get("episodes", []),
            )
            for e in edges
        ]

    # ========== Search ==========

    def search(self, graph_id: str, query: str, limit: int = 10,
               scope: str = "edges") -> List[Dict[str, Any]]:
        """
        Text search across graph nodes and/or edges.
        Matches query terms against names, summaries, and facts.
        """
        query_lower = query.lower().strip()
        query_terms = query_lower.split()
        results = []

        if scope in ("edges", "both"):
            edges = self._load_json(self._edges_file(graph_id))
            nodes = self._load_json(self._nodes_file(graph_id))
            node_map = {n["uuid"]: n["name"] for n in nodes}

            for e in edges:
                text = f"{e.get('name', '')} {e.get('fact', '')}".lower()
                score = sum(1 for term in query_terms if term in text)
                if score > 0:
                    results.append({
                        "type": "edge",
                        "uuid": e["uuid"],
                        "name": e.get("name", ""),
                        "fact": e.get("fact", ""),
                        "source_node_uuid": e.get("source_node_uuid", ""),
                        "target_node_uuid": e.get("target_node_uuid", ""),
                        "source_node_name": node_map.get(e.get("source_node_uuid", ""), ""),
                        "target_node_name": node_map.get(e.get("target_node_uuid", ""), ""),
                        "score": score / len(query_terms) if query_terms else 0,
                    })

        if scope in ("nodes", "both"):
            nodes = self._load_json(self._nodes_file(graph_id))
            for n in nodes:
                text = f"{n.get('name', '')} {n.get('summary', '')}".lower()
                attrs_text = json.dumps(n.get("attributes", {})).lower()
                score = sum(1 for term in query_terms if term in text or term in attrs_text)
                if score > 0:
                    results.append({
                        "type": "node",
                        "uuid": n["uuid"],
                        "name": n.get("name", ""),
                        "labels": n.get("labels", []),
                        "summary": n.get("summary", ""),
                        "score": score / len(query_terms) if query_terms else 0,
                    })

        # Sort by relevance score, return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    # ========== Graph Data Export ==========

    def get_graph_data(self, graph_id: str) -> Dict[str, Any]:
        """Get complete graph data (nodes + edges) for visualization"""
        nodes = self.get_all_nodes(graph_id)
        edges = self.get_all_edges(graph_id)

        node_map = {n.uuid_: n.name for n in nodes}

        nodes_data = [n.to_dict() for n in nodes]
        edges_data = []
        for e in edges:
            d = e.to_dict()
            d["source_node_name"] = node_map.get(e.source_node_uuid, "")
            d["target_node_name"] = node_map.get(e.target_node_uuid, "")
            edges_data.append(d)

        return {
            "graph_id": graph_id,
            "nodes": nodes_data,
            "edges": edges_data,
            "node_count": len(nodes_data),
            "edge_count": len(edges_data),
        }

    def get_graph_statistics(self, graph_id: str) -> Dict[str, Any]:
        """Get graph statistics"""
        nodes = self._load_json(self._nodes_file(graph_id))
        edges = self._load_json(self._edges_file(graph_id))

        # Count entity types
        type_counts = {}
        for n in nodes:
            for label in n.get("labels", []):
                if label not in ("Entity", "Node"):
                    type_counts[label] = type_counts.get(label, 0) + 1

        # Count relationship types
        rel_counts = {}
        for e in edges:
            rel_name = e.get("name", "unknown")
            rel_counts[rel_name] = rel_counts.get(rel_name, 0) + 1

        return {
            "graph_id": graph_id,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "entity_type_counts": type_counts,
            "relationship_type_counts": rel_counts,
        }
