# GithubCopilotProでプラグインを作るときのプロンプト（作成中）
　プレミアムではなくて、GPT4.1でも動くプロンプトを目指す！

## 基本構成
QGISの標準的なファイル・フォルダ構成として、作成せず、リポジトリの名前からプラグイン名等を作成して。  
本体のPYはmain.pyとせず、リポジトリの名前から作成して。  

## QT
QT6専用のプラグインして作成すること。  
メタデータには以下を必ず記載のこと。  
 qgisMinimumVersion=3.44  
 qgisMaximumVersion=3.999  
 required_qt_version=6  
UIは、Qt Designerの.uiファイル方式すること。  
標準言語は英語として、PYの動作説明のコメントだけは日本語で作成のこと。    
  
## 多言語化
QGISの設定言語によって、自動的に言語設定を行うようにして。  
QGISの翻訳標準的な翻訳方法に従って。
ソースの言語は英語として、英語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、日本語、中国語、ロシア語、ヒンディー語に対応して。  
lrelease.exeは、C:\Qt\linguist_6.9.1\lrelease.exe　にあります。  

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
metadata.txtからプラグイン情報を読み取って、バージョン文字列（例: 1.3.0）を+0.0.1してZIPを作成してmetadata.txtも更新して。  
ZIP作成指示に、プラグインとしてのフォルダを作成を忘れないで。  
前のバージョンのZIPは自動的にごみ箱へ移動して。  



