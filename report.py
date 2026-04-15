import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import pandas as pd

def generate_bar_chart(states_df: pd.DataFrame, topic: str) -> io.BytesIO:
    plt.figure(figsize=(10, 6))
    
    plt.barh(states_df['StateFullName'], states_df['NumericValue'], color='teal')
    
    plt.title(f'Топ штатів за захворюванням: {topic}')
    plt.xlabel('Середнє значення (%)')
    plt.ylabel('Штат')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return buf

def generate_csv_report(df: pd.DataFrame, keyword: str) -> io.BytesIO:
    matches = df[df['Topic'].str.contains(keyword, case=False, na=False)]
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    matches.to_csv(buf, index=False)
    buf.seek(0)
    
    return buf