import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def parse_text_file(file_path):
    G = nx.Graph()
    depots = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line == '':
            continue  # skip empty lines
        if line.startswith('NAME'):
            pass  # Skip the NAME line
        elif line.startswith('NUMBER OF VERTICES'):
            num_vertices = int(line.split(':')[1].strip())
            G.add_nodes_from(range(1, num_vertices + 1))
        elif line.startswith('LIST_REQUIRED_EDGES:'):
            current_section = 'required_edges'
        elif line.startswith('LIST_NON_REQUIRED_EDGES:'):
            current_section = 'non_required_edges'
        elif line.startswith('FAILURE_SCENARIO:'):
            current_section = 'failure_scenario'
        elif line.startswith('DEPOT:'):
            depots_line = line.split(':')[1].strip()
            depots = [int(node.strip()) for node in depots_line.split(',')]
        else:
            if current_section == 'required_edges':
                # Process required edge
                u_v, rest = line.split(') ', 1)
                u_v = u_v.strip('(')
                u, v = map(int, u_v.split(','))
                weight = extract_weight(rest)
                G.add_edge(u, v, weight=weight, required=True)
            elif current_section == 'non_required_edges':
                # Process non-required edge
                u_v, rest = line.split(') ', 1)
                u_v = u_v.strip('(')
                u, v = map(int, u_v.split(','))
                weight = extract_weight(rest)
                G.add_edge(u, v, weight=weight, required=False)
            elif current_section == 'failure_scenario':
                pass  # We can ignore failure scenario for graph building
    return G, depots

def extract_weight(text):
    # Extracts the weight from text like "edge weight {cost}"
    if 'edge weight' in text:
        weight_str = text.split('edge weight')[1].strip()
    elif 'cost' in text:
        weight_str = text.split('cost')[1].strip()
    else:
        weight_str = '1.0'  # Default weight
    try:
        weight = float(weight_str)
    except ValueError:
        weight = 1.0  # Default weight if parsing fails
    return weight

def visualize_graph(G, depots, instance_name, scenario_number):
    pos = nx.spring_layout(G, seed=42)  # Fixed layout for consistency

    # Prepare node colors
    node_colors = []
    for node in G.nodes():
        if node in depots:
            node_colors.append('darkgreen')
        else:
            node_colors.append('lightgreen')
    
    # Prepare edge colors and labels
    edge_colors = []
    edge_labels = {}
    for u, v in G.edges():
        weight = G[u][v]['weight']
        edge_labels[(u, v)] = f"{weight:.1f}"
        if G[u][v].get('required', False):
            edge_colors.append('red')
        else:
            edge_colors.append('black')
    
    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    
    # Draw the edges
    required_edges = [(u, v) for u, v in G.edges() if G[u][v].get('required', False)]
    non_required_edges = [(u, v) for u, v in G.edges() if not G[u][v].get('required', False)]
    
    nx.draw_networkx_edges(G, pos, edgelist=required_edges, edge_color='red', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=non_required_edges, edge_color='black')
    
    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
    
    # Create legend handles
    depot_patch = mpatches.Patch(color='darkgreen', label='Depot Nodes')
    node_patch = mpatches.Patch(color='lightgreen', label='Other Nodes')
    required_edge_line = mlines.Line2D([], [], color='red', label='Required Edges', linewidth=2)
    non_required_edge_line = mlines.Line2D([], [], color='black', label='Non-required Edges')

    # Add legend
    plt.legend(handles=[depot_patch, node_patch, required_edge_line, non_required_edge_line], loc='best')

    plt.title(f"Failure scenario {instance_name}.{scenario_number} visualization")
    plt.axis('off')
    plt.show()

def main():
    # Get user input
    while True:
        instance_name = input("Enter instance name (gdb, bccm, eglese): ").strip().lower()
        if instance_name not in ['gdb', 'bccm', 'eglese']:
            print('Invalid instance name: Choose from "gdb", "eglese" or "bccm"')
        else:
            break

    if instance_name == 'gdb':
        while True:
            scenario_number = input("Enter failure scenario number [1-37]: ").strip()
            if int(scenario_number) > 37 or int(scenario_number) < 1:
                print('Enter integers between 1 and 37') 
            else:
                break
    elif instance_name == 'bccm':
        while True:
            scenario_number = input("Enter failure scenario number [1-108]: ").strip()
            if int(scenario_number) > 108 or int(scenario_number) < 1:
                    print('Enter integers between 1 and 108') 
            else:
                break
    else:
        while True:
            scenario_number = input("Enter failure scenario number [1-112]: ").strip()
            if int(scenario_number) > 112 or int(scenario_number) < 1:
                    print('Enter integers between 1 and 112') 
            else:
                break
    
    
    # Validate inputs
    if instance_name not in ['gdb', 'bccm', 'eglese']:
        print("Invalid instance name. Must be 'gdb', 'bccm', or 'eglese'.")
        return
    try:
        scenario_number = int(scenario_number)
    except ValueError:
        print("Invalid scenario number. Must be an integer.")
        return
    
    # Set the folder path
    folder_name = f"Failure_Scenarios/{instance_name}_failure_scenarios"
    
    # Check if folder exists
    if not os.path.exists(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return
    
    # Set the file name
    file_name = f"{instance_name}.{scenario_number}.txt"
    file_path = os.path.join(folder_name, file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File '{file_name}' does not exist in folder '{folder_name}'.")
        return
    
    # Parse the text file and build the graph
    G, depots = parse_text_file(file_path)
    
    # Visualize the graph
    visualize_graph(G, depots, instance_name, scenario_number)

if __name__ == '__main__':
    main()
