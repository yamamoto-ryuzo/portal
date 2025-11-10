# GithubCopilotProでプラグインを作るときのプロンプト（作成中）
　プレミアムではなくて、GPT5-miniでも動くプロンプトを目指す！

## 基本構成
QGISの標準的なファイル・フォルダ構成として、作成せず、リポジトリの名前からプラグイン名等を作成して。  
本体のPYはmain.pyとせず、リポジトリの名前から作成して。  
ログ出力先は、プラグイン名とすること。  
TESTのPYを作るときはTESTフォルダに作成のこと。 
demoを作成するときはdemoフォルダに作成のこと。

## QT
QT6専用のプラグインとして作成すること。  
メタデータには以下を必ず記載のこと。   
 qgisMinimumVersion=3.44  
 qgisMaximumVersion=3.999  
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
QGISの翻訳は、複雑化せず、シンプルな翻訳方法であるtr()メソッドのみを使って行って。  
ソースの言語は英語として、英語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、日本語、中国語、ロシア語、ヒンディー語に対応して。  
lrelease.exeは、C:\Qt\linguist_6.9.1\lrelease.exe　にあります。  
UIに表示される文字がある場合は、文字を英語にして、翻訳対象とすること。  
ただし、PYの説明やログ出力は日本語にして。  

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
metadata.txtは、以下サイトを参考に作成して。  
　https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins/plugins.html#metadata-txt   
ZIP作成指示に、プラグインとしてのフォルダを作成を忘れないで。  
ライセンスファイルをZAPに入れるのを忘れないで。
前のバージョンのZIPは自動的にWINDOWSのごみ箱へ移動して。  

# 開発環境
VSCODE用の一般的な .ignore を設定して。  

# QT5-6対応プロンプト 「AI に投げる詳細プロンプト（実作業を任せるとき）」
「タスク：プラグインを Qt5 と Qt6 の両方で動作するように変更してください。具体要件は次の通りです。  

必須変更点（実装・検証を行ってください）  

metadata.txt に supportsQt6 = True を追加（既に無ければ）。  
全 Python モジュールで直接の PyQt5 / PyQt6 import を使っている箇所を from qgis.PyQt import ... に統一（qgis が適切なバインディングを選ぶため）。  
Qt6 の enum スコープ変更（例: QAbstractItemView.SelectRows → QAbstractItemView.SelectionBehavior.SelectRows）に対して、ランタイムで両方をサポートする shim を追加。可能なら getattr を使い、なければ代替の名前空間を探すこと。  
QEventLoop.exec_() が無い環境に対応するため、if hasattr(loop, 'exec_'): loop.exec_() else: loop.exec() の形に統一。  
QIODevice.WriteOnly（Qt6で名前空間が変わる）を直接参照する箇所はすべて、以下の優先順で取得して buffer.open(write_mode) するよう変更：  
getattr(QIODevice, 'WriteOnly', None)  
getattr(QIODevice, 'OpenMode', None).WriteOnly または OpenModeFlag.WriteOnly  
フォールバックで integer 1（WriteOnly に相当）を使う  
QDockWidget のフラグ（DockWidgetMovable, DockWidgetFloatable, DockWidgetClosable）等が Qt6 で名前空間変更されている場合に備え、存在しない場合は getattr(QDockWidget, 'DockWidgetMovable', None) → getattr(QDockWidget, 'DockWidgetFeature', ... ) 等をチェックして互換性を提供。  
変更したら python -m py_compile で構文チェック、可能なら既存のテスト（tests）を実行して緑にする。最終的に QGIS を起動してプラグインを試し、QGIS の Python ログにエラーが出ないことを確認。  
出力物（必須）  

変更ファイル一覧（1行ずつ目的を添えて）  
各変更で入れた互換 shim の短い説明（該当コード抜粋）  
実行手順（PowerShell 例）と QGIS での確認手順  
失敗時に回収すべきログ抜粋（どの情報を貼ればよいか）  
品質ゲート（必須）  

Syntax check: PASS  
Tests: all existing tests run and PASS (or list failing tests)  
Manual QGIS run: plugin loads without traceback in QGIS log (attach sample log)  
注意事項  

実動作確認は必ず QGIS 実行環境（対象ユーザープロファイル）で行う。ユニットテストだけでは enum / PyQt バインディングの違いを完全には検出できないことがある。  
破壊的な API 変更（QGIS 自体の API 変更）があれば別途対応が必要になる可能性あり。  
さあ、実装して変更 diff と実行ログをください。」  
