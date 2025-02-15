# app
アニメ「忍たま乱太郎」のキャラクターの名前を入力するとそのキャラクターの過去の登場回数と今期の登場回数を予測するwebアプリです。
言語はpythonでstreamlitを使っています。また、登場回数の予測にはポアソン分布を使っています。
### 実行方法
```
$ pip install pipenv
$ pipenv install streamlit pandas matplotlib numpy scipy japanize-matplotlib
$ pipenv run streamlit run app.py
```
### Webアプリ
https://bdnkqcsnccgz4xdgkj2igb.streamlit.app/
