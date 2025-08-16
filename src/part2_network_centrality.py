'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
import os
import datetime
import itertools


def run():
    """build actor graph and calculate centrality metrics"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    json_path = os.path.join(data_dir, "imdb_movies.json") 

    #reload movies csv
    df = pd.read_csv(json_path)
    # Build the graph
    g = nx.Graph()

    #go through actors 
    for index, row in df.iterrows():
        try:
            actors = json.loads(row['actors'].replace("'", '"'))
        except Exception:
            continue

        #add edges for all actor pairs in this movie
        for (a1_id, a1_name), (a2_id, a2_name) in itertools.combinations(actors, 2):
            if g.has_edge(a1_id, a2_id):
                g[a1_id][a2_id]['weight'] += 1
            else:
                g.add_edge(a1_id, a2_id, weight=1)
            
            # Add actor names as node attributes
            g.nodes[a1_id]['name'] = a1_name
            g.nodes[a2_id]['name'] = a2_name
        
    print (f"[Centrality] Nodes: {len(g.nodes)}, Edges: {len(g.edges)}")

    # Calculate centrality metrics
    degree_cent = nx.degree_centrality(g)
    top10 = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:10]
    print("[Centrality] Top 10 most central actors by degree centrality:")
    for actor_id, score in top10:
        print(f"{g.nodes[actor_id]['name']} (ID: {actor_id}): {score:.4f}")

    #save results as dataframe 
    df_edges = nx.to_pandas_edgelist(g)
    df_edges.rename(columns={'source': 'left_actor_id', 'target': 'right_actor_id'}, inplace=True)

    #timestamped filename 
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(data_dir, f'network_centrality_{ts}.csv')
    df_edges.to_csv(out_path, index=False)
    print(f"[Centrality] Edge list saved to {out_path}")

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'


"""with open() as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
        # add the actor to the graph    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
        i = 0 #counter
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                # Get the current weight, if it exists
                
                
                # Add an edge for these actors
                
                


# Print the info below
print("Nodes:", len(g.nodes))

#Print the 10 the most central nodes


# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`

"""