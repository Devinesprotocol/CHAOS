import json
import os


class KnowledgeGraph:

    def __init__(self, entity_path):

        self.graph_path = os.path.join(entity_path, "knowledge_graph.json")

        if not os.path.exists(self.graph_path):

            self.graph = {
                "nodes": [],
                "edges": []
            }

            self.save()

        else:

            with open(self.graph_path, "r") as f:
                self.graph = json.load(f)

    # -----------------------

    def add_node(self, concept):

        if concept not in self.graph["nodes"]:

            self.graph["nodes"].append(concept)

            self.save()

    # -----------------------

    def add_edge(self, source, target, relation):

        edge = {
            "source": source,
            "target": target,
            "relation": relation
        }

        self.graph["edges"].append(edge)

        self.save()

    # -----------------------

    def get_graph(self):

        return self.graph

    # -----------------------

    def save(self):

        with open(self.graph_path, "w") as f:
            json.dump(self.graph, f, indent=2)
