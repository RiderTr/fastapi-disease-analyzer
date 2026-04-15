import pandas as pd

def find_top_diseases(df: pd.DataFrame, top_n: int = 5) -> list:
    subset = df[df['DataValueUnit'] == '%']
    topic_avg = subset.groupby('Topic')['NumericValue'].mean().sort_values(ascending=False)
    
    results = []
    for topic, val in topic_avg.head(top_n).items():
        results.append((topic, round(val, 2)))
    return results

def search_disease(df: pd.DataFrame, keyword: str) -> dict:
    matches = df[df['Topic'].str.contains(keyword, case=False, na=False)]
    
    if matches.empty:
        return {"keyword": keyword, "found": False, "count": 0}
        
    unique_topics = list(matches['Topic'].unique())
    
    return {
        "keyword": keyword,
        "found": True,
        "count": len(matches),
        "topics_matched": unique_topics
    }

def get_state_data_for_topic(df: pd.DataFrame, topic: str, top_n: int = 10) -> pd.DataFrame:
    subset = df[(df['Topic'] == topic) & (df['DataValueType'] == 'Crude Prevalence')]
    if subset.empty:
        return pd.DataFrame()
        
    state_avg = subset.groupby(['LocationAbbr', 'StateFullName'])['NumericValue'].mean().reset_index()
    state_avg = state_avg[state_avg['LocationAbbr'] != 'US'] 
    
    return state_avg.sort_values(by='NumericValue', ascending=True).tail(top_n)