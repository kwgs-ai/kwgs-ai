# 2022_senshuPJ_server
専修大プロジェクトのポーリングの基礎コード
### フォルダ構成について
flaskappとrequestに分かれていて、flaskappの方にサーバのコードがある。requestはラズパイに入れてサーバを立ててから実行する。
### 利用手順
flaskappに入り、ターミナルで docker-compose build → docker-compose up のコマンドを打つ。
サーバが立ち上がったらラズパイのプログラム、request.pyを実行すると10秒に一回日時とステータスを取得する。
実際に使う際はスレッド化を行ったりする。
