import json
import os


class KnowledgeGraph:

    def __init__(self, graph_path="knowledge_graph/graph.json"):

        self.graph_path = graph_path

        # Ensure graph file exists
        if not os.path.exists(self.graph_path):
            self._create_empty_graph()

        with open(self.graph_path, "r") as f:
            self.graph = json.load(f)

    def _create_empty_graph(self):

        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)

        empty_graph = {
            "nodes": {},
            "edges": []
        }

        with open(self.graph_path, "w") as f:
            json.dump(empty_graph, f, indent=2)

    # -------------------------
    # Node Management
    # -------------------------

    def add_node(self, name, data=None):

        if name not in self.graph["nodes"]:
            self.graph["nodes"][name] = data or {}

            self._save()

    def get_node(self, name):

        return self.graph["nodes"].get(name)

    # -------------------------
    # Edge Management
    # -------------------------

    def add_edge(self, source, target, relation):

        edge = {
            "source": source,
            "target": target,
            "relation": relation
        }

        self.graph["edges"].append(edge)

        self._save()

    def get_edges(self, node):

        results = []

        for edge in self.graph["edges"]:
            if edge["source"] == node or edge["target"] == node:
                results.append(edge)

        return results

    # -------------------------
    # Save Graph
    # -------------------------

    def _save(self):

        with open(self.graph_path, "w") as f:
            json.dump(self.graph, f, indent=2)
