from pyvis.network import Network

from efootprint.utils.graph_tools import WIDTH, HEIGHT, set_string_max_width

COLOR_MAP = {
    "Autoscaling": "red",
    "OnPremise": "red",
    "Serverless": "red",
    "Hardware": "red",
    "Storage": "red",
    "UsagePattern": "blue",
    "UserJourney": "dodgerblue",
    "UserJourneyStep": "deepskyblue",
    "Job": "palegoldenrod"
}

USAGE_PATTERN_VIEW_CLASSES_TO_IGNORE = ["System", "Network", "Hardware", "Country", "Job", "Storage"]
INFRA_VIEW_CLASSES_TO_IGNORE = [
    "UsagePattern", "Network", "Hardware", "System", "UserJourney", "UserJourneyStep"]


def build_object_relationships_graph(
        node, input_graph=None, visited=None, classes_to_ignore=None, width=WIDTH, height=HEIGHT, notebook=False):
    cdn_resources = "local"
    if notebook:
        cdn_resources = "in_line"
    if classes_to_ignore is None:
        classes_to_ignore = ["System"]
    if input_graph is None:
        input_graph = Network(notebook=notebook, width=width, height=height, cdn_resources=cdn_resources)
    if visited is None:
        visited = set()

    if node in visited:
        return input_graph

    node_type = type(node).__name__
    if node_type not in classes_to_ignore:
        input_graph.add_node(
            id(node), label=set_string_max_width(f"{node.name}", 20),
            title=set_string_max_width(str(node), 80),
            color=COLOR_MAP.get(node_type, "gray"))

    for mod_obj in node.mod_obj_attributes:
        mod_obj_type = type(mod_obj).__name__
        if mod_obj_type not in classes_to_ignore:
            input_graph.add_node(
                id(mod_obj), label=set_string_max_width(f"{mod_obj.name}", 20),
                title=set_string_max_width(str(mod_obj), 80),
                color=COLOR_MAP.get(mod_obj_type, "gray"))
            if node_type not in classes_to_ignore:
                input_graph.add_edge(id(node), id(mod_obj))
            else:
                recursively_create_link_with_latest_non_ignored_node(node, mod_obj, input_graph, classes_to_ignore)

        if mod_obj not in visited:
            visited.add(node)
            build_object_relationships_graph(mod_obj, input_graph, visited, classes_to_ignore, width, height)

    return input_graph


def recursively_create_link_with_latest_non_ignored_node(source_obj, new_obj_to_link, input_graph, classes_to_ignore):
    for mod_obj in source_obj.modeling_obj_containers:
        if type(mod_obj).__name__ not in classes_to_ignore:
            if id(mod_obj) != id(new_obj_to_link) and id(mod_obj) in input_graph.get_nodes():
                input_graph.add_edge(id(mod_obj), id(new_obj_to_link))
        else:
            recursively_create_link_with_latest_non_ignored_node(
                mod_obj, new_obj_to_link, input_graph, classes_to_ignore)
