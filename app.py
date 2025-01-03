import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

# JSONデータをファイルからロード
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ファイルからデータ取得
data_file = 's31.json'
data = load_data(data_file)

# データフレームに変換
df = pd.DataFrame(data)

# UI
st.title('ポアソン過程シミュレーション')
search_string = st.text_input('検索文字列を入力:')

if search_string:
    # 検索文字列に基づいてフィルタリング
    matched_data = df[df['title'].str.contains(search_string) | df['content'].str.contains(search_string)]
    
    if not matched_data.empty:
        st.write('一致するデータ:', matched_data[['id', 'title']])
        
        # 日付の処理
        matched_data['date'] = pd.to_datetime(matched_data['date'])
        
        # イベント間隔（日数）を計算
        event_intervals = matched_data['date'].diff().dt.total_seconds().dropna() / (60 * 60 * 24)

        # 平均発生率 (λ) の計算
        lambda_value = 1.0 / event_intervals.mean()
        st.write(f'平均発生率 (λ): {lambda_value:.4f} イベント/日')

        # シミュレーション
        simulated_days = 30
        poisson_rv = poisson(lambda_value)
        future_events = poisson_rv.rvs(size=simulated_days)

        # 可視化
        st.subheader('ヒストグラム')
        plt.hist(future_events, bins=range(0, max(future_events)+1), align='left', rwidth=0.8)
        plt.xlabel('イベント数/日')
        plt.ylabel('頻度')
        plt.title('ポアソン分布によるシミュレーション結果')
        st.pyplot(plt)

        st.subheader('累積イベント数')
        cum_events = np.cumsum(future_events)
        plt.plot(cum_events)
        plt.xlabel('日数')
        plt.ylabel('累積イベント数')
        plt.title('累積イベント数の推移')
        st.pyplot(plt)

        st.subheader('タイムライン')
        timeline = matched_data[['date']].copy()
        timeline['event'] = 1
        timeline = timeline.set_index('date').resample('D').sum().fillna(0).cumsum()
        plt.plot(timeline.index, timeline['event'])
        plt.xlabel('日付')
        plt.ylabel('累積イベント数')
        plt.title('過去のイベントタイムライン')
        st.pyplot(plt)
    else:
        st.write('一致するデータがありません。')
