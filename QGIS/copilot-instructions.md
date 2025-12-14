# GithubCopilotProでプラグインを作るときのプロンプト
　プレミアムではなくて、GPT5-miniでも動くプロンプトを目指す！
 
## 関数の利用
関数は以下を利用のこと    
 https://qgis.org/pyqgis/master/  
 https://qgis.org/pyqgis/3.44/  
 https://qgis.org/pyqgis/3.40/  

## 基本構成
QGISの標準的なファイル・フォルダ構成として、作成せず、リポジトリの名前からプラグイン名等を作成して。  
本体のPYはplugin.pyとして。  
ログ出力先は、プラグイン名とすること。   
TESTのPYを作るときはTESTフォルダに作成のこと。   
demoを作成するときはdemoフォルダに作成のこと。  
 
## QT
QT5/QT6のプラグインとして作成すること。  
メタデータには以下を必ず記載のこと。   
 qgisMinimumVersion=3.00  
 qgisMaximumVersion=3.99  
 required_qt_version=6  
UIは、Qt Designerの.uiファイル方式すること。  
標準言語は英語として、PYの動作説明のコメントだけは日本語で作成のこと。    

## UI
UIはパネル・ツールバーのいずれで作成するか確認を行うこと。
パネル形式UIの場合は、左側ドックエリア（自動タブ化機能: 既存パネルとの統合）、右作業エリアのいずれで作成するか確認を行うこと。

## ユーザー関数（式関数）
ユーザー関数（式関数）の追加を行う場合は以下の例による行うこと。
```
from qgis.core import qgsfunction
@qgsfunction(args='auto', group='Custom', usesgeometry=False)
def my_custom_function(value1, value2, feature, parent):
    return value1 + value2
```

## 多言語化
QGISの設定言語によって、自動的に言語設定を行うようにして。  
QGISの翻訳は、複雑化せず、シンプルな翻訳方法であるtr()メソッドのみを使い、lrelease対応にして。   
ソースの言語は英語として、英語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、日本語、中国語、ロシア語、ヒンディー語に対応して。  
lrelease.exeは、C:\Qt\linguist_6.9.1\lrelease.exe　にあります。  
linguistは、C:\Qt\linguist_6.9.1\linguist.exe にあります。  
UIに表示される文字がある場合は、文字を英語にして、翻訳対象とすること。  
ただし、PYの説明やログ出力は日本語にして。  

## README
 READMEは、日本語のREADME_JP.MDを作成し、日本語に合わせてREADME.MDを英語版で作成のこと。    
 画像については同じ画像を利用のこと。    
 目次をアンカーリンク付きで作成のこと。  
 英語翻訳と日本語翻訳は、ページのトップで相互リンクを行うこと。    
 その他、仕様書等のMD作成も同様に取り扱うものとする。    

## バージョン管理 / Versioning
プラグインのバージョンは metadata.txt の version フィールドで管理して。  
新機能追加や修正時は metadata.txt の version を更新して。  
Changlogを以下を参考に作成して。  

バージョン表記: VA.B.C  
例: V2.0.0（A=2, B=0, C=0）  
バージョン番号の意味  
A: QGIS本体またはプラグインのバージョンアップに伴う本体の修正  
B: UIの変更（プラグインの追加等含む）、本体の簡易な機能追加  
C: プロファイル・プラグイン、本体の修正  

## 配布用ZIP
配布用ZIPの作成は、必要最小限をZIPにするcreate_zip.pyを作成して。  
ZIPファイルはプラグイン本体のフォルダのignore以外をZIPするようにして。  
metadata.txtからプラグイン情報を読み取って、バージョン文字列（例: 1.3.0）を+0.0.1してZIPを作成してmetadata.txtも更新して。    
metadata.txtは、以下サイトを参考に作成して。   
　https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins/plugins.html#metadata-txt      
前のバージョンのZIPは自動的にWINDOWSのごみ箱へ移動して。  

## README.MD  
 目次にMD内のリンクをつけて。  
 README_JP.MDは日本語メインサイトとして、README.MDは英語サイトとして作成して。    
 README_JP.MDが更新時のメインサイトとし、README.MDは日本語の英語サイトとして作成して。    
 READMEの日本語版と英語版の相互リンクをページのトップに設置する。  
 
# 開発環境
VSCODE用の一般的な .ignore を設定して。 
