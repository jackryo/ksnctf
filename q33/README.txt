
ksnctf q33

共通の素数と別の素数から生成された公開鍵を素因数分解し、秘密鍵を生成、wiresharkに登録してtls通信を復号

-----
○certificationパケットのsubjectPublicKeyInfoに公開鍵が格納
　公開鍵は(n.e)の形式になっており、nは4096bit、最後のeと頭、しっぽに余分なヘッダが付いている(2つのnで共通)のでそれを排除すればnが得られる
  eは65537(10001)

○ふたつのnを用いて、ユークリッド互除法により共通の素数pを探す

○qを求め、秘密鍵を生成する

○秘密鍵情報を、wiresharkが読み込めるpem形式に変換して鍵ファイルを作成

○wiresharkのpreference-protocols-sslで秘密鍵ファイルを登録
  ip : 接続先サーバのip port : 443 protocl : http
------



q33.pyは公開鍵のふたつのnから秘密鍵のpem生成までを一括して行う
