import yaml
import igraph as ig
from pathlib import Path
from frozendict import frozendict
import json
import pdb

primitive = str | int | float | bool | None


def freeze(data: dict | list | primitive) -> frozendict | tuple | primitive:
    if isinstance(data, list):
        return tuple(freeze(item) for item in data)
    elif isinstance(data, dict):
        return frozendict({k: freeze(v) for k, v in data.items()})
    else:
        return data


class OpenAPIGraph:
    def __init__(self):
        self.graph = ig.Graph(directed=True)
        self.node_map: dict[str, int] = {}  # node_id -> node_index
        self.content_map: dict[frozendict, str] = {}  # frozendict(data) -> node_id

    def add_node(self, node_id: str, node_type: str, data: frozendict | tuple | primitive):
        if node_id not in self.node_map:
            node = self.graph.add_vertex(node_id)
            node["type"] = node_type
            node["data"] = data
            self.node_map[node_id] = node.index
            self.content_map[data] = node_id

    def add_edge(self, source: str, target: str, relationship: str):
        if not self.graph.are_adjacent(self.node_map[source], self.node_map[target]):
            edge = self.graph.add_edge(self.node_map[source], self.node_map[target])
            edge["relationship"] = relationship

    def parameter_hash(self, parameter: frozendict) -> str:
        """Generate a unique hash for a parameter to deduplicate them."""
        return hash((
            parameter.get("name"),
            parameter.get("in"),
            parameter.get("schema", frozendict()),
            parameter.get("description", "")
        ))

    def add_parameter(self, parameter: frozendict, operation_id: str):
        """Add a parameter as a node, deduplicating if necessary."""
        param_hash = self.parameter_hash(parameter)
        if param_hash in self.content_map:
            param_node_id = self.content_map[param_hash]
        else:
            param_node_id = f"parameter_{parameter['name']}_{parameter['in']}"
            self.add_node(param_node_id, "Parameter", parameter)
            self.content_map[param_hash] = param_node_id
        self.add_edge(operation_id, param_node_id, "has_parameter")

    def parse_openapi_spec(self, spec: dict):
        # Add servers as nodes
        for i, server in enumerate(spec.get("servers", [])):
            self.add_node(f"server_{i}", "Server", freeze(server))

        # Add paths, operations, and related components
        for path, path_item in spec.get("paths", {}).items():
            self.add_node(path, "Path", freeze(path_item))
            for operation, operation_data in path_item.items():
                if operation not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    continue

                # Add operation node
                operation_data = freeze(operation_data)
                operation_id = f"{path}:{operation}"
                self.add_node(operation_id, "Operation", operation_data)
                self.add_edge(path, operation_id, "operation")

                # Add parameters
                for param in operation_data.get("parameters", []):
                    self.add_parameter(freeze(param), operation_id)

                # Add requestBody
                if "requestBody" in operation_data:
                    request_body = freeze(operation_data["requestBody"])
                    request_body_id = f"{operation_id}:requestBody"
                    self.add_node(request_body_id, "RequestBody", request_body)
                    self.add_edge(operation_id, request_body_id, "has_requestBody")

                # Add responses
                for status_code, response in operation_data.get("responses", {}).items():
                    response = freeze(response)
                    response_id = f"{operation_id}:response:{status_code}"
                    self.add_node(response_id, "Response", response)
                    self.add_edge(operation_id, response_id, "produces_response")

    def plot_graph(self):
        p = ig.plot(self.graph)
        p.save("output_graph.png")

    # def save_graph(self, output_path: Path):
    #     """Save the graph as a JSON file."""
    #     graph_data = {
    #         "nodes": [
    #             {"id": v.index, "type": v["type"], "data": v["data"]}
    #             for v in self.graph.vs
    #         ],
    #         "edges": [
    #             {
    #                 "source": self.graph.vs[e.source]["name"],
    #                 "target": self.graph.vs[e.target]["name"],
    #                 "relationship": e["relationship"],
    #             }
    #             for e in self.graph.es
    #         ],
    #     }
    #     with open(output_path, "w") as f:
    #         json.dump(graph_data, f, indent=2)


# Example usage
if __name__ == "__main__":
    openapi_spec_yaml = """
    openapi: 3.0.0
    info:
      title: Sample API
      version: 1.0.0
    servers:
      - url: https://api.example.com
    paths:
      /users:
        get:
          summary: List users
          parameters:
            - name: page
              in: query
              required: false
              schema:
                type: integer
          responses:
            200:
              description: A list of users
    components:
      schemas:
        User:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
    """

    spec = yaml.safe_load(openapi_spec_yaml)
    graph = OpenAPIGraph()
    graph.parse_openapi_spec(spec)
    # graph.save_graph(Path("output_graph.json"))
    graph.plot_graph()
