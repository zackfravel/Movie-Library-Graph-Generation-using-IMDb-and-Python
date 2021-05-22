# Zack Fravel
# ECE508 - Python Workshop
# Spring 2021
# Final Project
#
# filename: functions.py
#
# description: Contains functions written for the IMDb graph program.
#
#   create_movie_list() - returns a list of Movie objects (IMDb metadata) from directory structure
#   count_folders() - returns the number of folders in a given directory
#   addNodes() - function that takes a graph and list of movies and adds the nodes with labels and cover art
#   addEdges() - function that takes a graph and list of movies and adds the edges based on the specified filter
#   analyzeGraph() - Prints to the console a number of interesting built-in networkx functions on the graph
#   visualizeGraph() - Exports and launches an HTML file that contains a pyviz visualization of the graph
#
# library references:
#   https://docs.python.org/3/library/os.html
#   https://github.com/tqdm/tqdm
#   https://networkx.org/documentation/stable/tutorial.html
#   https://networkx.org/documentation/stable/reference/index.html
#   https://pyvis.readthedocs.io/en/latest/tutorial.html
#   https://pyvis.readthedocs.io/en/latest/documentation.html
#

# Import OS to iterate through directory
import os

# Import NetworkX
import networkx as nx

# Import Movie class
import movie


# Function that initializes the movies[] list for networkx to use
def create_movie_list(path):
    # Import console progress bar library
    from tqdm import tqdm
    # Store list of movies
    userMedia = []
    # Wrap processes in progress bar context, set the total as the folder count
    with tqdm(total=count_folders(path)) as progress_bar:
        # Iterate through folders in directory
        for entry in os.listdir(path):
            # Add instance of Movie class to movies list
            # This generates all IMDB information for the movie and stores it.
            userMedia.append(movie.Movie(entry))
            # Iterate progress bar
            progress_bar.update(1)
    return userMedia


# Function that counts the total number of folders in a filepath
def count_folders(path):
    numFolders = 0
    for _ in os.listdir(path):
        numFolders += 1
    return numFolders


# Function to add nodes to the graph from the movie list
def addNodes(graph, movieList):
    count = 0
    for film in movieList:
        # Label for the graph is name and year
        filmLabel = film.name() + " (" + str(film.year())+")"
        # Nodes themselves are indexed using the count variable, that way they are easily referenced using
        # the same indexing as movies[]. Node is set to an image type and gets the coverURL.
        graph.add_node(count, label=filmLabel, shape='image', image=film.getCoverURL(), title=filmLabel, size=200)
        count += 1
    pass


# Function to add edges to graph based on user selected filter
def addEdges(graph, viz, node, movieList, edgeFilter):
    # Set color of edge to be added
    if edgeFilter == 'directors':
        edgeColor = 'red'
    else:
        edgeColor = 'yellow'
    # Check against all other nodes
    for n in graph.nodes:
        # Don't check the same node (reduces execution time, redundant checks)
        if node != n:
            # Person Objects Condition
            if edgeFilter in ['actors', 'directors', 'writers', 'cinematographers', 'composers', 'producers']:
                # Check against all Person objects in the filter category
                for person in movieList[node].object()[edgeFilter]:
                    # Check if person is in another node's movie object, if so add an edge
                    for otherPerson in movieList[n].object()[edgeFilter]:
                        if person['name'] == otherPerson['name']:
                            # Don't add another edge if one already exists
                            if graph.has_edge(n, node):
                                pass
                            # Add the edge to both graphs
                            else:
                                try:
                                    # Add source and destination label to each edge
                                    graph.add_edge(node, n, label=person['name'], title=person['name']+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", color=edgeColor)
                                    viz.add_edge(node, n, label=person['name'], title=person['name']+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", color=edgeColor)
                                except:
                                    # This prevents the program crashing when IMDb returns an empty object for a Person
                                    pass
            # Year Condition
            elif edgeFilter in ['year']:
                # Check if current node year() returns the same as another node, if so add an edge
                if movieList[node].year() == movieList[n].year():
                    # Don't add another edge if one already exists
                    if graph.has_edge(n, node):
                        pass
                    # Add the edge to both graphs
                    else:
                        # Add source and destination label to each edge
                        graph.add_edge(node, n, title=movieList[n].year()+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", label=movieList[n].year())
                        viz.add_edge(node, n, title=movieList[n].year()+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", label=movieList[n].year())
            # Genres Condition
            elif edgeFilter in ['genres']:
                # Check against all genres
                for genre in movieList[node].genres():
                    # Check if genre is in another node's genre list, if so add an edge
                    if genre in movieList[n].genres():
                        # Don't add another edge if one already exists
                        if graph.has_edge(n, node):
                            pass
                        # Add the edge to both graphs
                        else:
                            # Add source and destination label to each edge
                            graph.add_edge(node, n, title=genre+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", label=genre)
                            viz.add_edge(node, n, title=genre+"<br><pre>   Src: " + movieList[node].name() + " (" \
                             + str(movieList[node].year())+")"+"<br><pre>   Dest : " + movieList[n].name() + " ("+ str(movieList[n].year())+")", label=genre)
                        pass
    pass


# Function to run built-in networkx analysis on generated graph
def analyzeGraph(nxGraph, movieList):
    # Generate lists keyed by the node for the respective network attribute
    # Connectivity - Pairwise or local node connectivity between two distinct and nonadjacent nodes is the minimum
    # number of nodes that must be removed (minimum separating cutset) to disconnect them.
    nodeConnectivityList = nx.all_pairs_node_connectivity(nxGraph)
    # Degree Centrality - The degree centrality for a node is the fraction of nodes connected to it.
    nodeDegreeCentralityList = nx.degree_centrality(nxGraph)
    # Closeness Centrality - The closeness of a node is the distance to all other nodes in the graph or in the case
    # that the graph is not connected to all other nodes in the connected component containing that node.
    nodeClosenessCentralityList = nx.closeness_centrality(nxGraph)
    print("\nAnalysis Report: \n")
    print("  Nodes: \n")
    for node in nxGraph.nodes():
        print("\t"+movieList[node].name() + " (" + str(movieList[node].year())+")\n")
        print("\t\tConnectivity: ")
        for key, value in nodeConnectivityList[node].items():
            if value == 0:
                continue
            else:
                print("\t\t\t", movieList[key].name(), ": ", value)
        print("\n\t\tDegree Centrality: ", nodeDegreeCentralityList[node])
        print("\n\t\tCloseness Centrality: ", nodeClosenessCentralityList[node], "\n")
    pass


# Function to visualize the graph using pyvis
def visualizeGraph(visualGraph, movieList):
    # Gather neighbors to display in each node's title (hover over)
    # NOTE: currently pyvis is only able to display multiple edges between nodes visually if the graph is a
    # directed graph. Our graph doesn't necessarily need to be directed, in fact, it would make more sense for it
    # to be undirected (bidirectional). However, this limitation is why only one of the neighbors will keep the neighbor
    # data. (i.e. the node where the arrow is coming out or the one that comes first in alphabetical order).
    neighbor_map = visualGraph.get_adj_list()
    # add neighbor data to node hover data
    for node in visualGraph.nodes:
        for neighbor in neighbor_map[node['id']]:
            node['title'] += "<br><pre>   Neighbor:" + movieList[neighbor].name() + " (" \
                             + str(movieList[neighbor].year())+")"
    # Set physics model
    visualGraph.barnes_hut()
    # g.show_buttons()  # used for testing and setting customized options
    # Sets a default option for how the graph will be organized on screen
    visualGraph.set_edge_smooth('dynamic')
    # Output the visualized graph to an HTML file and launch it
    visualGraph.show("visualized.html")
    pass
