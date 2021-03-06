# dynalist2md
Dynalist data export to Markdown

## 利用前にAPI Tokenを生成ください
[Dynalist Developer Page](https://dynalist.io/developer)でSecret tokenを生成してください。
生成したTokenを`.bashrc`などで

`export Dynalist_API_KEY='生成したSecretToken here'`

として、環境変数にexportしてください。

---

## 利用方法

### filename2dyna_id.py → ファイル名からID特定

`python3 filename2dyna_id.py`

でDynalistに登録しているファイル（フォルダーは除く）の全IDを表示します。

`python3 filename2dyna_id.py 'ファイル名'`

で特定のファイルのIDを表示します。このIDは途中で変化しません。
APIがそれほど速くないこともあり、一度生成し、使い回すことが出来るようにツールを分割しました。

### id2md.py → ID指定したファイルをMarkdownへ（標準出力）

一度、ファイルIDを調べておいて（変化しないものなので）、

`python3 id2md.py 'ファイルID'`

で指定したファイルをMarkdownに出力します（標準出力）。


## dyna_watch.py

 Dynalistのデータを監視し、変化がある毎に、指定されたMarkdownファイルを作成するツール。

 `python3 dyna_watch.py 'ファイルID' target_file.md`

 Dynalistの監視間隔は20sec（60secに6回のrate limitがある）。

## dyna2deckset.py

Dynalistのデータを監視し、変化がある毎に、指定されたMarkdownファイルをDecksetが受け入れるフォーマットで作成するツール。
利用方法はdyna_watch.pyと同じ。

Decksetが受け入れるフォーマットは`---`が改ページになっているので、H2を生成する前に必ず、その改ページを挿入する。