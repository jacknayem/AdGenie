import pandas as pd
import os

# ROOT SETUP
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def precomputed_user_interest():
    """
    DATA PIPELINE: Ingests raw clickstream data, calculates the most viewed 
    categories for each user over different timeframes, and caches the results.
    """
    # 1. INGEST & CLEAN
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'Users_browsing_history_2019-Nov.csv')
    df = pd.read_csv(
        DATA_PATH,
        usecols=['event_time', 'event_type', 'category_code', 'user_id'],
        dtype={'user_id': 'int32','category_code': 'category'},
        parse_dates=['event_time']
        )
    df = df[df['event_type'] == 'view']
    df = df.dropna(subset=['category_code'])
    df = df.drop_duplicates()

    # 2. AGGREGATOR ENGINE
    def get_user_interests(dataframe, time_frequency):
        print(f'Computing {time_frequency} interests...')
        grouped = dataframe.groupby(['user_id', pd.Grouper(key='event_time', freq=time_frequency)])
        top_categories = grouped['category_code'].agg(
            lambda x: x.value_counts().index[0] if len(x) > 0 else None
        )
        return top_categories.reset_index()
    
    # 3. COMPUTE & CACHE
    monthly_interests = get_user_interests(df, 'ME')
    weekly_interests = get_user_interests(df, 'W')
    threeday_interests = get_user_interests(df, '3D')
    daily_interests = get_user_interests(df, '1D')

    monthly_interests.to_csv(os.path.join(BASE_DIR,'data','monthly_interests.csv'), index=False)
    weekly_interests.to_csv(os.path.join(BASE_DIR,'data','weekly_interests.csv'), index=False)
    threeday_interests.to_csv(os.path.join(BASE_DIR,'data','threeday_interests.csv'), index=False)
    daily_interests.to_csv(os.path.join(BASE_DIR,'data','daily_interests.csv'), index=False)
    print('Successfully Data Save')


def retive_user_interest(time_frequency):
    """
    SIMULATOR: Acts as the live Ad-Server cache. It loads a precomputed timeframe 
    and randomly selects a user's most recent interest to feed into the AdGenie prompt.
    """
    # 1. CACHE LOOKUP
    USER_DATA_PATH = os.path.join(BASE_DIR, 'data')
    if time_frequency == 'ME':
        df = pd.read_csv(os.path.join(USER_DATA_PATH, 'monthly_interests.csv'))
    elif time_frequency == 'W':
        df = pd.read_csv(os.path.join(USER_DATA_PATH, 'weekly_interests.csv'))
    elif time_frequency == '3D':
        df = pd.read_csv(os.path.join(USER_DATA_PATH, 'threeday_interests.csv'))
    elif time_frequency == '1D':
        df = pd.read_csv(os.path.join(USER_DATA_PATH, 'daily_interests.csv'))
    else:
        raise ValueError("Invalid time frequency provided.")
    
    # 2. USER INFERENCE
    random_user_id = df['user_id'].drop_duplicates().sample(1).iloc[0]
    pick_user_info = df[df['user_id'] == random_user_id].sort_values(by='event_time', ascending=False).iloc[0]
    
    return pick_user_info

# SCRIPT ENTRY POINT
if __name__ == '__main__':
    precomputed_user_interest()