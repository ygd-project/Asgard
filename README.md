# Asgard
Webにおける標準的なアプリオリアルゴリズムの実装。

## 前提
python2.7.10で動作確認。

## 簡単な使い方
1. data.csvに[識別子(IPアドレスやログイン名など),URL]の形式でアクセスデータを用意する。
2. 「python main.py load_data」を実行する。分析結果が終わると分析結果がpickle.dumpに保存される。
3. target.csvにレコメンドしたいユーザのアクセスログを[URL]で各行に列挙する。
4. 「python main.py load_target」を実行する。標準出力でリフト値が高いURL順に[URL,リフト値]で出力される。

## pythonからの使い方
```
from main import Control
c = Control()

#データ分析
c.proc_load()

#レコメンド取得-戻り値[レコメンドURLリスト,リフト値,信頼度,支持度]
s = c.proc_macth()

```
## pythonでの拡張の仕方
継承しload_data_csv、load_target_csvをオーバーライドすることで入力をDBソースにすることで拡張可能。

## 構成
* main.py(制御用スクリプトファイル)
 - load_data_csv(データCSV読み込み)
 - go_apriori(アプリオアルゴリズム解析)
 - load_target_csv(ターゲットCSV読み込み)
 - go_macth(結果を使ったレコメンド)
 - save_pickel(結果を外部に保存)
 - load_pickel(結果を外部からロード)
* apriori.py(アプリオアルゴリズム本体)

## 謝辞
このサイトを参考にして実装した。
http://skzy.hatenablog.com/entry/2013/10/04/022218
