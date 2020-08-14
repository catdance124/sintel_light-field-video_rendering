blender_script
===

# what?
Sintelのシーンプロダクションファイル(.blend)からlight field videoをレンダリングするためのスクリプト

# env?
windows10  
Blender ... render25 ブランチ [ここ](https://download.blender.org/durian/blender/)から落としてくる  
python v3.6.5  
numpy==1.14.3+mkl  
OpenEXR==1.3.2  
Pillow==5.3.0  

# how work this?
(B) ... Blender内（python3.1）で動作させることを考えて書いたコード  
(C) ... コンソール（python3.6）で動作させることを考えて書いたコード  
- [light_field_video_rendering.py](light_field_video_rendering.py)(B)
    - カメラを動かしてanimation renderingを行うメインスクリプト．Blender内のエディタに直接記述しても動作するが，Blenderの--pyton引数にこのスクリプトを与えて動作させる．
- [run_blender.py](run_blender.py)(C)
    - light_field_video_rendering.pyにいい感じの引数を与えてBlenderにレンダリングさせるためのスクリプト．python bundled in blenderを呼び出すためのラッパー的なポジション
- [batches/*.cmd](batches)
    - 各シーンファイルの設定が書かれたスクリプト．中でrun_blender.pyを呼び出す．書き方によっては一度で複数視点を同時にレンダリングし，CPUをフル活用することもできる．
- 小ツール的なサブスクリプト
    - [generate_clean_file.py](generate_clean_file.py)(B)
        - cleanレンダリングを行うための設定を一括で行う．（透過オフ，解像度固定，レイヤーの畳み込みなどの設定）基本的に各ファイル一度のみBlender内のプロンプトから実行し，保存する．
    - [get_focal_length.py](get_focal_length.py)(B)
        - カメラの焦点距離を標準出力するスクリプト
    - [check_error_files.py](check_error_files.py)(C)
        - 他のすべてのビューと比較して問題のあるビュー (例: 一部のオブジェクトがブラックアウトされている) を検出するスクリプト
    - [organize_rendering_data.py](organize_rendering_data.py)(C)
        - EXR(depth)->npy(disparity)に変換するスクリプト．現在は水平垂直十字視点のみ処理する．
        - [readEXR.py](readEXR.py)
            - EXRファイルを読み込む

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


# timeline
データセット作成の時系列作業メモ  
レンダリングに関する作業は[ここ](https://docs.google.com/spreadsheets/d/1L9ZVGB_6EjVpHKJBAojlOixZthO2Pd0NFOCK6JKR3Hk/edit?usp=sharing)に残している．
1. オリジナルのSintelプロダクションファイルを落としてくる
1. プロダクションファイルを[generate_clean_file.py](generate_clean_file.py)を使って編集する．ノードネットワークなどは手動で編集する．
1. [run_blender.py](run_blender.py)を使ってLFをレンダリングする．バッチ化したスクリプトで実行した．
1. [organize_rendering_data.py](organize_rendering_data.py)を使ってdepthデータをdisparityデータに変換する．
    1. その際に，焦点距離が必要となるので，[get_focal_length.py](get_focal_length.py)を使って取得しておき，[focal_length.csv](focal_length.csv)として保存しておく．
1. 問題のあるデータを[check_error_files.py](check_error_files.py)で検出し控えておく．使用するデータに問題がある場合は，除外するか個別に再レンダリングを施す．


# error files
check_error_files.pyにより検出したもの．  
XX_04, 04_XX視点のみエラーファイルの除去を手動で行った．
エラーファイルの関係により，03.4_chickenrun/03.4b_comp，06_shaman_b/06.e_compはすべて使用していない．
```
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/03_01/0505.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/05_04/0502.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/05_04/0505.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/06_02/0535.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/07_01/0507.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/07_08/0531.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/07_08/0533.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/08_04/0516.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/08_06/0514.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/08_07/0502.png
../rendering/clean/02_shaman/02.f_comp/9x9_baseline0.01/08_07/0511.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/00_06/0072.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/01_00/0083.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/01_03/0081.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/01_07/0078.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/02_00/0081.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/02_00/0083.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/02_05/0084.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/02_06/0074.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/02_08/0070.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/03_05/0076.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/03_08/0083.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/04_04/0084.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/05_08/0069.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/07_04/0078.png
../rendering/clean/03.4_chickenrun/03.4b_comp/9x9_baseline0.01/07_05/0081.png
../rendering/clean/05.1_questbegins/05.1b_comp/9x9_baseline0.01/00_07/0156.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_00/0372.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_01/0369.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_01/0373.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_01/0401.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_02/0409.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_03/0401.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_06/0393.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_07/0389.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/00_08/0409.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_01/0373.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_02/0405.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_03/0404.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_07/0373.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_07/0388.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/01_08/0376.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_01/0370.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_01/0381.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_01/0382.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_02/0384.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_02/0385.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_02/0411.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_04/0403.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_05/0367.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/02_05/0370.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/03_02/0367.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/03_02/0393.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/03_03/0400.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/03_07/0370.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_00/0366.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_02/0395.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_02/0403.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_03/0393.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_03/0413.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_04/0382.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_05/0393.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_06/0408.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_07/0410.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/04_07/0412.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_00/0383.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_00/0392.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_03/0382.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_03/0389.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_03/0395.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_04/0409.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_05/0412.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_06/0368.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_06/0394.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_06/0408.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/05_07/0408.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/06_02/0380.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/06_02/0384.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/06_05/0382.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/06_07/0391.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_02/0384.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_02/0395.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_03/0401.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_05/0383.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_06/0407.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/07_07/0411.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/08_02/0381.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/08_04/0380.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/08_06/0414.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/08_07/0393.png
../rendering/clean/06_shaman_b/06.e_comp/9x9_baseline0.01/08_08/0405.png
../rendering/clean/08.2_thebigfight/08.2l_comp/9x9_baseline0.01/00_00/0561.png
```
