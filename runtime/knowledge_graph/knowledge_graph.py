import json
import os


class KnowledgeGraph:

    def __init__(self, entity_path):

        self.entity_path = entity_path
        self.graph_path = f"{entity_path}/memory/knowledge_graph.json"

        if not os.path.exists(self.graph_path):
            self._create_graph()

    def _create_graph(self):

        graph = {
            "nodes": [],
            "edges": []
        }

        with open(self.graph_path, "w") as f:
            json.dump(graph, f, indent=4)

    def load_graph(self):

        with open(self.graph_path, "r") as f:
            return json.load(f)

    def save_graph(self, graph):

        with open(self.graph_path, "w") as f:
            json.dump(graph, f, indent=4)

    def add_node(self, node):

        graph = self.load_graph()

        if node not in graph["nodes"]:
            graph["nodes"].append(node)

        self.save_graph(graph)

    def add_edge(self, source, target, relation):

        graph = self.load_graph()

        edge = {
            "source": source,
            "target": target,
            "relation": relation
        }

        if edge not in graph["edges"]:
            graph["edges"].append(edge)

        self.save_graph(graph)

    def get_neighbors(self, node):

        graph = self.load_graph()

        neighbors = []

        for edge in graph["edges"]:
            if edge["source"] == node:
                neighbors.append(edge["target"])

        return neighbors
