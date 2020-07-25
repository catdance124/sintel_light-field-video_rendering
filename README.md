blender_script
===

# what?
Sintelのシーンプロダクションファイル(.blend)からlight field videoをレンダリングするためのスクリプト

# how work this?
- light_field_video_rendering.py
    - カメラを動かしてanimation renderingを行うメインスクリプト．Blender内のエディタに直接記述しても動作するが，Blenderの--pyton引数にこのスクリプトを与えて動作させる．
- run_blender.py
    - light_field_video_rendering.pyにいい感じの引数を与えてBlenderにレンダリングさせるためのスクリプト．python bundled in blenderを呼び出すためのラッパー的なポジション
- batches/*.cmd
    - 各シーンファイルの設定が書かれたスクリプト．中でrun_blender.pyを呼び出す．書き方によっては一度で複数視点を同時にレンダリングし，CPUをフル活用することもできる．

# what is the structure of the file?
このrepositoryは下記のファイル構造でのみ動作する．  
```
Sintel/
  ┣━━ clean_files/    ...    cleanレンダリング用の.blendファイルがあるディレクトリ
  ┃     ┗━━ scenes/
  ┃             ┣━━ 02_shaman/
  ┃             ┗━━ 03.1_alley/
  ┣━━ rendering/
  ┃     ┗━━ clean/    ...    レンダリング結果が保存されるディレクトリ
  ┣━━ render25_win64/    ...    Render Branch(render25)の実行ファイルがあるディレクトリ
  ┗━━ blender_script/    ...    このrepository
```

# tips
複数マシンで処理を並列に行う場合には，上記ディレクトリをシンボリックリンクで繋ぐとファイルが一元化され，全てのマシンでローカルファイルとして扱うことができるので考えることが少なくて済む．  
実際にはネットワーク越しに実行ファイル(Sintel/render25_win64/blender.exe)は実行できないので，`render25_win64`のみコピーし，それ以外の3つのディレクトリをシンボリックリンクで繋ぐ．  
下記は別PCのディレクトリをネットワークドライブSに登録したときの場合．シンボリックリンクの作成は管理者権限cmdでしか行えない点に注意．

```
(ps)> mkdir sintel
(ps)> Copy-Item S:\render25_win64 .\sintel\ -Recurse
(cmd root)> mklink /D .\sintel\rendering S:\rendering
(cmd root)> mklink /D .\sintel\scripts S:\scripts
(cmd root)> mklink /D .\sintel\clean_files S:clean_files
```