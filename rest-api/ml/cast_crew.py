import os
import numpy as np
import pandas as pd

path = os.path.dirname(__file__)
######################## DIRECTORS
df_director = pd.read_csv(os.path.join(path, 'directors.csv'), index_col=0)

DIRECTOR_REVENUE_MEASURE = 'avg_revenue'
def get_director_revenue(name):
    '''Get revenue of movies the director has directed'''
    q = df_director[df_director['director'] == name]
    if q['director'].count() == 0:
        revenue = df_director.loc[1000000][DIRECTOR_REVENUE_MEASURE]
    else:
        idx = q.index[0]
        revenue = df_director.loc[idx][DIRECTOR_REVENUE_MEASURE]
    return revenue

######################### ACTORS
df_actors = pd.read_csv(os.path.join(path, 'actors.csv'), index_col=0)

ACTOR_REVENUE_MEASURE = 'avg_revenue'
def get_actor_revenue(actor):
    q = df_actors[df_actors['actor_name'] == actor]
    if q['actor_name'].count() == 0:
        revenue = df_actors.loc[1000000][ACTOR_REVENUE_MEASURE]
    else:
        idx = q.index[0]
        revenue = df_actors.loc[idx][ACTOR_REVENUE_MEASURE]
    return revenue

def get_actor_list_revenue(actor_list):
    '''Mean of top 5 revenues of actors'''
    try:
        if len(actor_list) == 0:
            return df_actors.loc[1000000][ACTOR_REVENUE_MEASURE]
        arr = sorted([get_actor_revenue(a) for a in actor_list.split('#')], reverse=True)[:5]
    except:
        return df_actors.loc[1000000][ACTOR_REVENUE_MEASURE]
    return int(np.array(arr).mean())
