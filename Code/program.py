# Zack Fravel
# ECE508 - Python Workshop
# Spring 2021
# Final Project
#
# filename: program.py
#
# description: Top level module of the IMDb movie graph project. Implements a script
#   that imports the promptGUI and graphGUI and displays them in order of program execution.
#   The script then generates a list of Movie (class) objects from the folder selected by the user
#   as well as creating a graph from that list using the user's selected edge filter. Finally,
#   the graph (created with networkx) is visualized using pyvis along with an analysis function that
#   provides some interesting information about the user's library.
#
# library references:
#   https://docs.python.org/3/library/os.html
#   https://github.com/tqdm/tqdm
#   https://networkx.org/documentation/stable/tutorial.html
#   https://networkx.org/documentation/stable/reference/index.html
#   https://pyvis.readthedocs.io/en/latest/tutorial.html
#   https://pyvis.readthedocs.io/en/latest/documentation.html
#

# Import user defined functions from functions.py
import functions as func

# Import promptGUI.py
import promptGUI

# Launch promptGUI
promptGUI.promptRoot.mainloop()

# Initialize list of movies from directory given in GUI
movies = func.create_movie_list(promptGUI.selected_folder.get())

# Import graphGUI script
import graphGUI

# Launch graphGUI
graphGUI.graphRoot.mainloop()

# Set graph filter variable from field in GUI
graphFilter = graphGUI.selected_filter.get()
graphFilter = graphFilter.lower()

# Import NetworkX
import networkx as nx
# Import pyvis for visualization
from pyvis.network import Network

# Instantiate NetworkX Graph
G = nx.MultiDiGraph()
# Instantiate pyvis network with window size
vizGraph = Network(directed=True, height='100%', width='100%', bgcolor='#222222', font_color='white')

# Add nodes to graph from list of movies
func.addNodes(G, movies)

# Import network from networkx graph to the visual graph
vizGraph.from_nx(G)

# Import console progress bar library
from tqdm import tqdm
# Add edges to graph from filter and provide a progress bar (this can take time depending on the filter)
with tqdm(total=len(G.nodes)) as progress_bar:
    # Add edges to all nodes
    for N in G.nodes():
        # Special case included for actors in directors, check for that
        if graphFilter == 'actors and directors':
            filterBuffer = 'actors'
            func.addEdges(G, vizGraph, N, movies, filterBuffer)
            filterBuffer = 'directors'
            func.addEdges(G, vizGraph, N, movies, filterBuffer)
            progress_bar.update(1)
        else:
            func.addEdges(G, vizGraph, N, movies, graphFilter)
            # Update progress bar after each node finishes adding edges
            progress_bar.update(1)

# Run graph analysis
func.analyzeGraph(G, movies)

# Visualize graph
func.visualizeGraph(vizGraph, movies)
