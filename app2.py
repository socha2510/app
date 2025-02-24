import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import poisson
import matplotlib

# フォント設定 (日本語フォントがインストールされている前提)
matplotlib.rcParams['font.family'] = 'IPAGothic'

def load_data(file_path):
    """
    JSONファイルをロードして Pythonオブジェクトに変換する関数。
    テストで呼び出せるように分割。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 複数のファイルパス
file_paths = [
    's31.json',
    's30.json',
    's29.json',
    's28.json',
    's27.json',
    's26.json',
    's25.json',
    's24.json',
    's23.json',
]

def create_dataframe():
    """
    複数の JSONファイルを読み込み、DataFrameを合体して返す関数。
    こちらもテスト対象として分割。
    """
    dataframes = []
    for file_path in file_paths:
        data = load_data(file_path)
        df = pd.DataFrame(data)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# =====================================
# Streamlit UI ロジック
# =====================================

# メイン実行：DataFrameを用意
df = create_dataframe()

# Streamlit UI
st.title('にんたま予測ドットコム')
st.write('アニメ「忍たま乱太郎」の登場キャラクターが今期どれくらい登場するか、ポアソン分布を使って予測するよ！')

# 検索文字列入力
search_string = st.text_input('キャラクターの名前を入力しよう:')

if search_string:
    # 検索文字列に基づいてフィルタリング
    matched_data = df[
        df['title'].str.contains(search_string, na=False) |
        df['content'].str.contains(search_string, na=False)
    ]

    if not matched_data.empty:
        st.write('23期～30期までの', search_string, 'が登場した回',
                 matched_data[['id', 'title']])

        # 検索結果に基づいたイベント数をカウント
        event_counts = len(matched_data)

        # 平均発生率 (λ) の計算
        lambda_value = event_counts / len(file_paths)
        st.write(f'１シーズン辺りの平均登場回数 (λ): {lambda_value:.4f} 回/シーズン')

        st.write(search_string, 'の今期の登場回数の確率は…？')

        # シミュレーション
        kaisu = np.arange(0, 11)
        pmf_values = stats.poisson.pmf(kaisu, lambda_value)
        cdf_values = stats.poisson.cdf(kaisu, lambda_value)

        # 可視化
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.bar(kaisu, pmf_values, alpha=0.8, color='skyblue', edgecolor='black')
        ax1.set_title(f'ポアソン分布(λ= {lambda_value:.4f})のPMF')
        ax1.set_xlabel('登場回数')
        ax1.set_ylabel('確率')
        ax1.set_xticks(range(min(kaisu), max(kaisu) + 1))

        ax2.step(kaisu, cdf_values, where='post', alpha=0.8, color='salmon', linewidth=2)
        ax2.set_title(f'ポアソン分布(λ= {lambda_value:.4f})のCDF')
        ax2.set_xlabel('登場回数')
        ax2.set_ylabel('累積確率')
        ax2.set_xticks(range(min(kaisu), max(kaisu) + 1))

        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.write('一致するデータがありません。')
