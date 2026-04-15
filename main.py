from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import pandas as pd
from data_loader import load_and_clean_data, get_unique_topics
from analytics import find_top_diseases, search_disease, get_state_data_for_topic
from report import generate_bar_chart, generate_csv_report

dataset = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Загрузка даних у пам'ять...")
    try:
        dataset['df'] = load_and_clean_data('U.S._Chronic_Disease_Indicators.csv')
        print(f"Дані загружені! {len(dataset['df'])} рядків")
    except Exception as e:
        print(f"Помилка загрузки даних: {e}")
    yield
    dataset.clear()

app = FastAPI(
    title="CDI Data API",
    description="API для анализу даних хронічних захворювань. Замість консольного меню.",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {"message": "Ласкаво просимо до API. Перейдіть на /docs для перегляду інтерактивного меню"}

@app.get("/topics", tags=["Аналітика"])
def get_all_topics():
    df = dataset.get('df')
    if df is None:
        raise HTTPException(status_code=500, detail="Дані не завантажено")
    return {"total": len(get_unique_topics(df)), "topics": get_unique_topics(df)}

@app.get("/top-diseases", tags=["Аналітика"])
def top_diseases(limit: int = 5):
    df = dataset.get('df')
    top_list = find_top_diseases(df, limit)
    return {"top_diseases": [{"topic": t[0], "percentage": t[1]} for t in top_list]}

@app.get("/search", tags=["Аналітика"])
def search(keyword: str):
    df = dataset.get('df')
    return search_disease(df, keyword)

@app.get("/plot/states/{topic}", tags=["Візуалізація"])
def plot_top_states(topic: str):
    df = dataset.get('df')
    states_df = get_state_data_for_topic(df, topic)
    
    if states_df.empty:
        raise HTTPException(status_code=404, detail="Немає числових даних для цієї хвороби.")
        
    img_buf = generate_bar_chart(states_df, topic)
    return StreamingResponse(img_buf, media_type="image/png")

@app.get("/export/csv/{keyword}", tags=["Експорт"])
def export_search_results(keyword: str):
    df = dataset.get('df')
    csv_buf = generate_csv_report(df, keyword)

    return StreamingResponse(
        csv_buf, 
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=report_{keyword}.csv"}
    )
