import yaml
from dataclasses import dataclass, field

@dataclass
class Node:
    id: str  # Unique identifier for the node
    type: str  # Type of the node (e.g., 'Path', 'Operation', 'Schema', etc.)
    data: dict = field(default_factory=dict)  # Additional metadata
    source_path: list[str] = field(default_factory=list)  # Add this field to track the JSON path

@dataclass
class Edge:
    source: str  # Source node ID
    target: str  # Target node ID
    relationship: str  # Type of relationship

class OpenAPIGraph:
    def __init__(self):
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.node_map: dict[str, Node] = {}

    def add_node(self, node_id: str, node_type: str, data=None, source_path=None):
        if node_id not in self.node_map:
            node = Node(
                id=node_id,
                type=node_type,
                data=data or {},
                source_path=source_path or []
            )
            self.nodes.append(node)
            self.node_map[node_id] = node

    def add_edge(self, source: str, target: str, relationship: str):
        self.edges.append(Edge(source=source, target=target, relationship=relationship))

    def parse_openapi_spec(self, spec: dict):
        # Add servers as nodes
        for i, server in enumerate(spec.get("servers", [])):
            self.add_node(
                node_id=f"server_{i}",
                node_type="Server",
                data=server,
                source_path=['servers', str(i)]
            )

        # Add paths and operations as nodes and connect them
        for path, path_item in spec.get("paths", {}).items():
            path_id = f"path_{path}"
            self.add_node(
                node_id=path_id,
                node_type="Path",
                data={"path": path},
                source_path=['paths', path]
            )

            for operation, operation_data in path_item.items():
                if operation in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    operation_id = f"operation_{path}_{operation}"
                    self.add_node(
                        node_id=operation_id,
                        node_type="Operation",
                        data=operation_data,
                        source_path=['paths', path, operation]
                    )
                    self.add_edge(source=path_id, target=operation_id, relationship="has_operation")

                    # Add parameters
                    for param in operation_data.get("parameters", []):
                        param_id = f"parameter_{path}_{operation}_{param['name']}"
                        self.add_node(node_id=param_id, node_type="Parameter", data=param)
                        self.add_edge(source=operation_id, target=param_id, relationship="has_parameter")

                    # Add requestBody
                    if "requestBody" in operation_data:
                        request_body = operation_data["requestBody"]
                        request_body_id = f"requestBody_{path}_{operation}"
                        self.add_node(node_id=request_body_id, node_type="RequestBody", data=request_body)
                        self.add_edge(source=operation_id, target=request_body_id, relationship="has_requestBody")

                    # Add responses
                    for status_code, response in operation_data.get("responses", {}).items():
                        response_id = f"response_{path}_{operation}_{status_code}"
                        self.add_node(node_id=response_id, node_type="Response", data=response)
                        self.add_edge(source=operation_id, target=response_id, relationship="produces_response")

        # Add components (schemas)
        for schema_name, schema in spec.get("components", {}).get("schemas", {}).items():
            schema_id = f"schema_{schema_name}"
            self.add_node(node_id=schema_id, node_type="Schema", data=schema)

    def display_graph(self):
        print("Nodes:")
        for node in self.nodes:
            path_str = " -> ".join(node.source_path) if node.source_path else "root"
            print(f"- {node.id} [{node.type}] (Source: {path_str}) {node.data}")
        print("\nEdges:")
        for edge in self.edges:
            print(f"- {edge.source} -> {edge.target} [{edge.relationship}]")

    def get_spec_chunk(self, node_id: str, spec: dict) -> dict:
        """
        Retrieve the original spec chunk for a given node.
        
        Args:
            node_id: The ID of the node to look up
            spec: The original OpenAPI specification
            
        Returns:
            The portion of the spec that the node was created from
        """
        if node_id not in self.node_map:
            raise KeyError(f"Node {node_id} not found in graph")
        
        node = self.node_map[node_id]
        current = spec
        
        # Navigate through the spec using the source path
        for path_part in node.source_path:
            current = current[path_part]
        
        return current

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
    graph.display_graph()

    # Example: Get the spec chunk for the GET operation
    operation_node_id = "operation_/users_get"
    original_spec_chunk = graph.get_spec_chunk(operation_node_id, spec)
    print("\nOriginal spec chunk for /users GET operation:")
    print(yaml.dump(original_spec_chunk))
