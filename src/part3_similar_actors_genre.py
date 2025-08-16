'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below
import os
import pandas as pd
import json
import datetime
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_distances

def sag():
        """find similar actors by genre"""
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        csv_path = os.path.join(data_dir, "imdb_movies.csv")

        #reload movies csv
        df = pd.read_csv(csv_path)
        
        # Create a genre-actor matrix
        records = []
        for index, row in df.iterrows():
                try:
                        actors = json.loads(row['actors'].replace("'", '"'))
                        genres = json.loads(row['genres'].replace("'", '"'))
                except Exception:
                        continue

                for actor_id, actor_name in actors:
                        for genre in genres:
                                records.append({'actor_id': actor_id, 'actor_name': actor_name, 'genre': genre})
        df_records = pd.DataFrame(records)

        #actor-genre matrix
        actor_genre_matrix = (
                df_records
                .groupby(['actor_id', 'actor_name', 'genre'])
                .size()
                .reset_index(name='count')
                .pivot(index=['actor_id', 'actor_name'], columns='genre', values='count')
                .fillna(0)
        )

        #chris hemsworth as query
        query_id = "nm1165110"
        query_vec = actor_genre_matrix.loc[query_id].values.reshape(1, -1)

        #calculate cosine distances
        cos_dis = cosine_distances(actor_genre_matrix.values, query_vec).flatten()
        actor_genre_matrix['cosine_distance'] = cos_dis

        #euclidean distances
        dist = DistanceMetric.get_metric('euclidean')
        euc_dis = dist.pairwise(actor_genre_matrix.values[:, :-1], query_vec).flatten()
        actor_genre_matrix['euclidean_distance'] = euc_dis

        #top 10 similar actors by cosine distance
        top10 = actor_genre_matrix.sort_values('cosine_distance').head(11).iloc[1:11]  # exclude self

        #save
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(data_dir, f'similar_actors_genre_{ts}.csv')
        top10.to_csv(out_path)

        print("[Similar Actors by Genre] Top 10 actors similar to Chris Hemsworth (nm1165110) by cosine distance:")
        for ind, row in top10.iterrows():
                print(f"{ind[1]} ({ind[0]})")

        print(f"[Similar Actors by Genre] Results saved to {out_path}")
        print("[Similar Actors by Genre] Note: The list of similar actors may vary when using Euclidean distance due to the different ways these metrics capture similarity. Cosine distance focuses on the angle between vectors, making it sensitive to the distribution of genres, while Euclidean distance considers the absolute differences in genre counts, which can be influenced by the overall number of appearances.")