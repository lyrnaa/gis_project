from flask import Flask, render_template, request
from collections import defaultdict, deque
import ast
import os

app = Flask(__name__)

def check_binary_tree(edges):
    if not edges:
        return True, ""  

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    parent = dict()
    root = edges[0][0]

    queue = deque([root])
    visited.add(root)
    parent[root] = None

    while queue:
        node = queue.popleft()
        children_count = 0

        for neighbor in graph[node]:
            if neighbor == parent.get(node):
                continue
            if neighbor in visited:
                return False, "Graf zawiera cykl."
            visited.add(neighbor)
            parent[neighbor] = node
            queue.append(neighbor)
            children_count += 1

        if children_count > 2:
            return False, f"Wierzchołek {node} ma więcej niż 2 dzieci ({children_count})."

    all_nodes = set(graph.keys())
    if visited != all_nodes:
        return False, "Graf nie jest spójny."

    return True, ""


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    edges_input = None
    if request.method == 'POST':
        try:
            raw_input = request.form['edges']
            edges = ast.literal_eval(raw_input)
            
            if len(edges) == 0:
                result = "⚠️ Wprowadź dane wejściowe (lista krawędzi)."
            else:
                edges_input = raw_input
                is_tree, reason = check_binary_tree(edges)
                if is_tree:
                    result = "✅ Graf jest drzewem binarnym."
                else:
                    result = f"❌ Graf nie jest drzewem binarnym: {reason}"
        except Exception as e:
            result = f"Niepoprawny format wprowadzonych danych!"

    return render_template('index.html', result=result, edges_input=edges_input)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
