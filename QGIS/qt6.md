# Qt5/Qt6 対応: 実装・検証プロンプト

以下は、任意の QGIS プラグインや PyQt を使うプロジェクトを Qt5 と Qt6（QGIS 3.44+ を含む）で互換させるために AI やエンジニアに渡す「そのまま実作業できる」詳細プロンプトです。
必要な実装・検証・提出物・品質ゲートをすべて含めています。コピペして実行可能な指示にしてください。

---

件名（短）:
プラグインを Qt5 と Qt6（QGIS 3.44+）両対応にする — 実装・検証・配布用 ZIP 作成

目的（1行）:
対象のプラグイン／プロジェクトを Qt5 / Qt6 両方で動作させる。変更は最小限に留めつつ互換 shim を導入し、動作検証（py_compile, tests, QGIS 実行）まで行ってください。

前提（必読）
- QGIS 固有 API の動作検証は実機（QGIS インストール環境）で実行する必要がある。CI などで QGIS がない環境だと一部検証は不可。
- 変更はできる限り既存のコードを壊さない「互換レイヤ（shim）」を追加する方針で実施すること。

必須タスク（実装・検証）
1) metadata
- プラグイン形式のプロジェクトであれば `metadata.txt`（存在する場合）に `supportsQt6 = True` を追加してください（既にあればスキップ）。変更したら1行コメントで理由を追記。

2) PyQt import の正規化
- QGIS プラグインであれば `from qgis.PyQt import ...` を優先して使うようにしてください。一般の PyQt/PySide プロジェクトでは、プロジェクトがサポートするバインディングに合わせて import を統一してください。
- 直接 `PyQt5` / `PyQt6` / `PySide2` / `PySide6` を混在させると互換性の問題が生じるため、プロジェクトの方針に従い一貫した import に揃えてください。

3) 互換 shim の追加（`qt_compat.py` を追加/更新）
- 目的: Qt5 と Qt6 の API 差を吸収する最小限の関数／ヘルパを提供する。
- 必要な helper（少なくとも次を含める）:
  - `exec_loop(loop)`: if hasattr(loop,'exec_'): return loop.exec_() else: return loop.exec()
  - `qiodevice_writeonly()`: 優先順で WriteOnly を解決して返す（`getattr(QIODevice,'WriteOnly', None)` 等）。フォールバックは整数 1。
  - `dock_feature_lookup(names)`: QDockWidget の feature を安全に解決するヘルパ。
  - `enum_get(obj, *names)`: getattr(obj, name) を順に試して返す（未発見なら None）。
  - 必要なら `QgsMessageLog.logMessage` の整数レベルを `Qgis.MessageLevel` にマップする短期的な monkey-patch（呼び出し箇所が膨大な場合の暫定措置）。
-- shim の位置: プロジェクト内の適切な場所（例: `qt_compat.py` または `your_package/qt_compat.py`）。モジュール内に短い docstring を入れること。

4) 既存コードの修正
- enum / flags / exec_ / QIODevice 参照個所を shim を用いるよう差し替える。直接置換できない箇所は try/except fallback を追加。
- 効果がある代表例（必ず網羅）:
  - QEventLoop.exec_ → use `exec_loop`
  - QIODevice.WriteOnly → use `qiodevice_writeonly()`
  - QHeaderView/other enum rename → `enum_get(header, 'ResizeToContents', 'Stretch', ...)`
  - QDockWidget フラグの取得に shim を使う
- UI のレンダリング安定化（result dialog 等）:
  - テーブル列幅が縮む問題（Qt6）対策：ヘッダーで `ResizeToContents` を試し、`setMinimumSectionSize` を設定、最後に `setStretchLastSection(True)` をセットする等の防御的コードを入れる。

5) 構文チェック・テスト
- 変更後、リポジトリルートで次を実行して構文チェック:
  - PowerShell (例):
    ```powershell
    # 例: 全 Python ファイルを再帰的にチェックする
    python -m py_compile $(Get-ChildItem -Recurse -Include *.py | ForEach-Object FullName)
    ```
  - もしくはプロジェクト全体:
    ```powershell
    python -m py_compile $(Get-ChildItem -Recurse -Include *.py | ForEach-Object FullName)
    ```
- 既存の tests があれば全て実行し、結果を報告（PASS / FAIL + failing tests）。

6) QGIS での手動検証（必須）
- 手順（PowerShell 例や QGIS 内でやる操作を明記）:
  1. プラグインフォルダをバックアップ（例: rename existing plugin folder）。
  2. ローカルのプラグインフォルダ（あなたのプロジェクト）を QGIS の plugins フォルダに上書きするか、配布用 ZIP を作成してインストールしてください（ツール名やスクリプトはプロジェクトに合わせて指定）。
  3. QGIS を再起動してプラグインを有効化。
  4. 検索 UI を開き、代表的な検索（単一レイヤ、複数レイヤ、page/timeout を含む検索）を実行。
  5. QGIS Python コンソール／メッセージログにエラーや traceback が出ていないか確認。
- 収集すべきログ（失敗時に必ず添付）:
  - QGIS のメッセージログの traceback（Python exception full）。
  - プラグイン側で出力した debug ログ（例: `QgsMessageLog.logMessage` の出力）。
  - 問題が UI の場合、以下の Python コンソール出力を貼る（README にも載せている診断スニペット）:
    - tab count, each tab の fields_count, features_count, table column widths
  - 変更差分（apply_patch 形式）と変更ファイル一覧

出力物（必須）
- 変更ファイル一覧（1行ずつ: ファイルパス — 目的/修正点を簡潔に）
- 互換 shim の説明（`qt_compat.py` の該当コード抜粋を提示）とその目的
- 変更差分: ガイドラインに従って apply_patch 形式の diff（ファイル編集は apply_patch を使う形式で提出）
- 実行手順（PowerShell 例）と QGIS での確認手順（箇条書き）
- 収集済みログ（上記収集項目）と、問題が残る場合の次のアクション案

品質ゲート（必須）
- Syntax check: PASS（`python -m py_compile` でエラー無し）
- Tests: 既存の tests が存在する場合は全て RUN → PASS。テストがない場合は N/A として明記。
- Manual QGIS run: プラグインを起動して代表的な検索を実行し、QGIS の Python ログに traceback が出ないこと。
- 最終的な ACCEPT 条件: 上の3つすべてが PASS または N/A（テスト無し）で、UI 表示（特に検索結果テーブル）が Qt5 / Qt6 両方で問題ない。

提出フォーマット（厳守）
- 変更は apply_patch 形式で差分を作成して送る（ミニマムなパッチで、1ファイルにつき 1 Update セクションを原則）。
  - 変更ファイル一覧をプレーンテキストで1行ずつ提示（例: `qt_compat.py` — Qt5/6 shim を追加）。
- 実行ログ（py_compile、テスト、create_zip、QGIS のログ）はプレーンテキストで貼る。
- shim の短いコード抜粋は提示してよい（最大 60 行程度）。ただし全ファイルの完全内容は apply_patch で渡す。

検討すべきエッジケース（指示に明示する）
- 既存コードが直接整数（例: 0,1,2）でログレベルやフラグを渡しているケース。shim で integer をマップするか、呼び出し箇所を enum に変換するかを指示する必要がある（短期は shim でマップ）。
- generator／イテレータを渡すコード（features 等）は UI 側で `list()` 化して複数回使えるようにする。
- QGIS のバインディング（PyQt6 / PyQt5 / PySide 等）は `qgis.PyQt` 経由で吸収される想定だが、QGIS バージョン差による API 変更は別途対応が必要。
- テストが無い場合は最小限の unit テスト（shim のユニットテスト）を追加してもらうと良い。

例: 推奨する shim の短いサンプル（プロンプト内で渡す）
- exec wrapper:
```python
def exec_loop(loop):
    if hasattr(loop, 'exec_'):
        return loop.exec_()
    return loop.exec()
```

- QIODevice WriteOnly resolver:
```python
from qgis.PyQt.QtCore import QIODevice

def qiodevice_writeonly():
    # try common names
    w = getattr(QIODevice, 'WriteOnly', None)
    if w is not None:
        return w
    # Qt6 may have OpenMode / OpenModeFlag
    om = getattr(QIODevice, 'OpenMode', None) or getattr(QIODevice, 'OpenModeFlag', None)
    if om is not None:
        v = getattr(om, 'WriteOnly', None)
        if v is not None:
            return v
    # fallback numeric
    return 1
```

- enum getter helper:
```python
def enum_get(obj, *names):
    for n in names:
        try:
            return getattr(obj, n)
        except Exception:
            continue
    return None
```

- QDockWidget feature lookup:
```python
from qgis.PyQt.QtWidgets import QDockWidget

def dock_feature(name_candidates):
    for n in name_candidates:
        if hasattr(QDockWidget, n):
            return getattr(QDockWidget, n)
    return None
```

- QgsMessageLog integer-level monkey-patch (必要なら短期的に):
```python
from qgis.core import QgsMessageLog, Qgis
_orig_log = QgsMessageLog.logMessage

def _logMessage(msg, tag, level):
    try:
        # if level is int, try to map to Qgis.MessageLevel
        if isinstance(level, int) and not isinstance(level, Qgis.MessageLevel):
            # naive mapping: 0->Info,1->Warning,2->Critical (adjust as needed)
            lvl_map = {0: Qgis.MessageLevel.Info, 1: Qgis.MessageLevel.Warning, 2: Qgis.MessageLevel.Critical}
            level = lvl_map.get(level, Qgis.MessageLevel.Info)
    except Exception:
        pass
    return _orig_log(msg, tag, level)

QgsMessageLog.logMessage = _logMessage
```

実行手順（PowerShell 例）
- 構文チェック:
```powershell
# 例: 全 Python ファイルを再帰的にチェックする (PowerShell)
python -m py_compile $(Get-ChildItem -Recurse -Include *.py | ForEach-Object FullName)
```
- create_zip の dry-run（作成済みなら実行して問題無ければ zip 作成）:
```powershell
# パッケージ作成スクリプトがある場合はプロジェクトに合わせて実行してください。例:
python .\create_zip.py --dry-run
python .\create_zip.py --output ..\project-name-vX.Y.Z.zip
```

QGIS での確認（手順）
-- QGIS を起動 → プラグインを有効 → 代表的な機能（例: 検索 UI の表示や操作）を実行 → Python コンソールにて診断スニペットを実行して内部 state を確認してください（README の診断スニペット等を使用）。

失敗時に貼ってほしいログ（コピペで十分）
-- Python traceback の全文（QGIS メッセージログ または 実行環境のログ）
-- プロジェクトが出力するログ（例: `QgsMessageLog` または標準出力の debug 出力）
-- 診断スニペットの出力（UI 問題の場合はウィジェット状態やテーブル列幅等の情報）
- 変更差分（apply_patch）

提出物（納品フォーマット、厳守）
- apply_patch 形式の差分（編集済みファイルのみ）
- 変更ファイル一覧（1行ずつ）
- shim の説明（短いコード抜粋）
- 実行ログ（py_compile, tests, create_zip, QGIS 実行ログ）
- 最終的な「品質ゲート」サマリ（Syntax: PASS, Tests: PASS/N/A, Manual QGIS: PASS）

最後に（優先順）
1. shim を追加して構文チェックをパスさせる（py_compile）。
2. QGIS 上で代表的な検索（UI）を動かし、エラーがないことを確認する。
3. 問題が残るなら呼び出し側に最小限の追加ログを入れて原因を切り分ける（fields が空か UI の表示問題か）。
