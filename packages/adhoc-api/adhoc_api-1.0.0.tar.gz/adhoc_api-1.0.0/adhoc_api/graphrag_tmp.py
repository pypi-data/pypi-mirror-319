import yaml
import igraph as ig
from pathlib import Path
import json
from frozendict import frozendict
import pdb


"""
extra requirements:
[normal]
- igraph
- leidenalg
- frozendict
[dev]
- pycairo
- matplotlib

"""

primitive = str|int|float|bool|None
def freeze(data: dict|list|primitive) -> frozendict|tuple|primitive:
    if isinstance(data, list):
        return tuple(freeze(item) for item in data)
    elif isinstance(data, dict):
        return frozendict({k: freeze(v) for k, v in data.items()})
    else:
        return data

class OpenAPIGraph:
    def __init__(self):
        self.graph = ig.Graph()
        self.node_map: dict[str, int] = {} # node_id -> node_index
        self.content_map: dict[frozendict, str] = {} # frozendict(data) -> node_id

    def add_node(self, node_id: str, node_type: str, data: frozendict|tuple|primitive):
        node = self.graph.add_vertex(node_id)
        node["type"] = node_type
        node["data"] = data
        self.node_map[node_id] = node.index
        self.content_map[data] = node_id

    
    def add_edge(self, source: str, target: str, relationship: str):
        source_index = self.node_map[source]
        target_index = self.node_map[target]
        edge = self.graph.add_edge(source_index, target_index)
        edge["relationship"] = relationship


    def parse_openapi_spec(self, spec: dict):
        # Add servers as nodes
        for i, server in enumerate(spec.get("servers", [])):
            self.add_node(f"server_{i}", "Server", freeze(server))
        
        for path, path_item in spec.get("paths", {}).items():
            self.add_node(path, 'Path', freeze(path_item))
            for operation, operation_data in path_item.items():
                operation_data = freeze(operation_data)
                if operation not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    pdb.set_trace()
                    continue
                
                # Add operation node
                operation_id = f"{path}:{operation}"
                assert operation_id not in self.node_map, f"Operation {operation_id} already exists"
                self.add_node(operation_id, "Operation", operation_data)
                self.add_edge(path, operation_id, "operation")

                # Add parameters as nodes
                for param in operation_data.get("parameters", []):
                    pdb.set_trace()
                    if not self.content_map.get(param):
                        pdb.set_trace()
                        self.add_node(param_id, "Parameter", param)
                    self.add_edge(operation_id, param_id, "has_parameter")


if __name__ == "__main__":
    here = Path(__file__).parent
    spec_path = here / '../examples/cbioportal/cbioportal.json'
    spec: dict = json.loads(spec_path.read_text())
    graph = OpenAPIGraph()
    graph.parse_openapi_spec(spec)
    graph.plot()
