# AIDLC Workflow Dashboard

AIDLC Workflow Dashboard は、AIDLC の実行状況を可視化するための Streamlit 製ダッシュボードです。

本ツールは AIDLC を操作するためのものではなく、AIDLC の状態・進捗・成果物・更新履歴を確認するための **Read Only の可視化ダッシュボード** として設計します。

## 目的

AIDLC を利用した開発では、現在どの Phase / Stage にいるのか、どの Stage が完了・進行中・未着手・Skip・承認待ちなのかを素早く把握する必要があります。

このダッシュボードでは、開発者が数秒で以下を確認できることを目指します。

- 現在の AIDLC リリースバージョン
- Workflow 全体の進行状況
- 現在の Phase / Stage
- 次に実行される Stage
- Stage ごとの完了状況
- Skip された Stage と理由
- 人間の承認待ちが必要な Stage
- AIDLC によって生成された成果物
- audit 情報に基づく最近の更新履歴

## 背景

AIDLC の実行結果は、`aidlc-state.md`、各 Phase 配下の成果物、`audit/` 配下の更新履歴など、複数のファイルやディレクトリに分散しています。

そのため、開発中に現在地を把握するには、複数のファイルを直接確認する必要があります。

本ダッシュボードでは、これらの情報を読み取り、Dashboard / Workflow / Artifacts / Settings の 4 画面に整理して表示します。

## 基本方針

- Python Streamlit を使用する
- AIDLC の状態変更は行わない
- Stage の開始・完了・Skip・承認などの操作は行わない
- AIDLC 側の設定変更は行わない
- 表示対象データを読み取り専用で扱う
- 画面ファイルに処理を詰め込まず、役割ごとにファイルを分離する
- ファイル名・ディレクトリ名から処理内容が分かる命名にする

## 配置と実行方法

本ダッシュボードは、AIDLC で開発を進めているルートディレクトリ直下に `aidlc_dashboard/` を配置して利用する想定です。

配置イメージ:

```text
<aidlc_project_root>/
├── aidlc/
├── core/
└── aidlc_dashboard/
    ├── app.py
    ├── config.yml
    ├── requirements.txt
    ├── src/
    └── ...
```

初回のみ、`aidlc_dashboard/` ディレクトリに移動して依存ライブラリをインストールします。

```bash
cd aidlc_dashboard
pip install -r requirements.txt
```

ダッシュボードは以下のコマンドで起動します。

```bash
streamlit run app.py
```

起動後、Streamlit が表示するローカル URL をブラウザで開いて利用します。

## 想定する AIDLC データ構造

ダッシュボードは、主に以下のような AIDLC intent 配下の情報を読み取る想定です。

```text
aidlc/
└── spaces/
    └── default/
        └── intents/
            └── <intent>/
                ├── aidlc-state.md
                ├── audit/
                ├── ideation/
                ├── inception/
                ├── construction/
                ├── operation/
                └── verification/
```

### 主な読み取り元

| 読み取り元 | 用途 |
|---|---|
| `aidlc-state.md` | 現在の Phase / Stage、Scope / Profile などの状態情報を取得する |
| `audit/` | Dashboard 下部の最近の更新履歴を取得する |
| `ideation/` などの Phase 配下 | Stage 情報、成果物、Skip 理由、承認待ち情報などを取得する |
| `core/tools/aidlc-version.ts` | `v2.9.1` のような AIDLC リリースバージョンを取得する |

## 画面構成

| 画面 | 役割 |
|---|---|
| Dashboard | 全体進捗、現在 Stage、次 Stage、承認待ち、最近の更新を表示する |
| Workflow | Phase / Stage の詳細、ステータス別フィルタ、Stage 一覧を表示する |
| Artifacts | 成果物一覧、検索、フィルタ、プレビュー、ダウンロードを表示する |
| Settings | ダッシュボードの表示設定、自動更新設定、リセットを表示する |

## 成果物プレビュー対象

Artifacts 画面では、以下のファイル形式をプレビュー対象とします。

| 拡張子 | 表示方針 |
|---|---|
| `.md` | Markdown として表示する |
| `.csv` | 表形式で表示する |
| `.txt` | テキストとして表示する |
| `.json` | 整形済み JSON として表示する |
| `.yaml` / `.yml` | YAML テキストとして表示する |
| `.png` | 画像として表示する |
| `.jpg` / `.jpeg` | 画像として表示する |

## 設定ファイル

人間が直接編集する設定ファイルは、プロジェクト直下の `config.yml` のみとします。

`config.yml` では、AIDLC の読み込み対象パスとダッシュボードの表示設定を管理します。

読み込み対象パスは、AIDLC のルートディレクトリだけを指定してアプリ側で全てを推測するのではなく、画面や用途ごとに明示します。

これにより、AIDLC のディレクトリ構成が変わった場合や、一部の画面だけ別のディレクトリを参照したい場合でも、`config.yml` の修正だけで対応できるようにします。

`config.yml` で管理する主な値は以下です。

- Dashboard で読み込む対象ディレクトリパス
- Workflow を表示するために読み込む対象ディレクトリパス
- Artifacts 一覧で読み込む対象ディレクトリパス
- 最近の更新履歴として読み込む `audit/` ディレクトリパス
- AIDLC リリースバージョンを取得する `core/tools/aidlc-version.ts` のファイルパス
- 自動更新 ON / OFF
- 更新間隔
- 日時表示形式
- Artifacts の 1 ページあたり表示件数
- Theme
- Skip Stage の表示 ON / OFF
- 完了 Phase をデフォルトで閉じるかどうか
- 現在の Phase を自動展開するかどうか

## 命名方針

ディレクトリ名・ファイル名は、処理内容が一目で分かる名前にします。

たとえば、ファイルやディレクトリを読み込む処理は `file_readers/`、読み込んだ内容から AIDLC の表示対象データを抜き出す処理は `aidlc_data_extractors/`、画面表示用にデータを整える処理は `display_data_builders/` に配置します。

画面ファイルや UI 部品も、`dashboard_screen.py`、`phase_stage_accordion.py`、`artifact_detail_panel.py` のように、用途が分かる名前にします。

## ディレクトリ構成案

`src/` 配下に、Streamlit 画面、UI 部品、ファイル読み込み、データ抽出、表示用データ生成などの実装コードを配置します。

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `app.py` | Streamlit アプリの起動入口。ページ設定、画面遷移、共通 CSS 読み込みを行う |
| `config.yml` | 人間が編集する唯一の設定ファイル。読み込み対象ディレクトリパス、自動更新、表示件数、テーマなどを管理する |
| `requirements.txt` | Python 依存ライブラリを定義する |
| `README.md` | 起動方法、設定方法、ディレクトリ構成、利用方法を説明する |
| `requirements/requirements.md` | UI 要件定義書を置く |
| `src/` | アプリ本体の実装コードを置くディレクトリ |

### screens

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/screens/` | Streamlit の各画面を置く |
| `src/screens/dashboard_screen.py` | Dashboard 画面。全体進捗、現在 Stage、次 Stage、最近の更新を表示する |
| `src/screens/workflow_screen.py` | Workflow 画面。Phase / Stage 詳細、ステータスフィルタ、アコーディオンを表示する |
| `src/screens/artifacts_screen.py` | Artifacts 画面。成果物一覧、検索、フィルタ、プレビューを表示する |
| `src/screens/settings_screen.py` | Settings 画面。ダッシュボード表示設定、自動更新設定、リセットを表示する |

### ui_parts

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/ui_parts/` | 画面で再利用する UI 部品を置く |
| `src/ui_parts/sidebar_navigation.py` | 左側サイドバーのナビゲーション部品を描画する |
| `src/ui_parts/page_title_header.py` | 画面タイトル、説明文、最終更新日時、更新ボタンを描画する |
| `src/ui_parts/summary_metric_cards.py` | Dashboard 上部の AIDLC バージョン、全体ステータス、Scope/Profile、Stage 進捗カードを描画する |
| `src/ui_parts/phase_progress_flow.py` | Dashboard の Phase 横並び進捗フローを描画する |
| `src/ui_parts/current_next_stage_panel.py` | Dashboard の現在 Stage / 次 Stage パネルを描画する |
| `src/ui_parts/stage_status_badge.py` | 完了、進行中、未着手、Skip、承認待ちのステータスバッジを描画する |
| `src/ui_parts/workflow_status_filter_buttons.py` | Workflow 画面上部のステータス絞り込みボタンを描画する |
| `src/ui_parts/phase_stage_accordion.py` | Workflow 画面の Phase 単位アコーディオンと Stage 一覧を描画する |
| `src/ui_parts/artifact_filter_bar.py` | Artifacts 画面の Phase、Stage、File Type、Status、検索欄を描画する |
| `src/ui_parts/artifact_list_table.py` | Artifacts 画面の成果物一覧テーブルを描画する |
| `src/ui_parts/artifact_detail_panel.py` | Artifacts 画面右側の成果物詳細・プレビュー・ダウンロード領域を描画する |
| `src/ui_parts/settings_option_panel.py` | Settings 画面の設定セクション、トグル、セレクトボックスを描画する |

### data_models

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/data_models/` | アプリ内で使うデータ構造を定義する |
| `src/data_models/workflow_summary_model.py` | Workflow 全体の状態、AIDLC バージョン、Scope/Profile、完了数などを表す |
| `src/data_models/phase_model.py` | Phase 番号、Phase 名、説明、進捗、ステータスを表す |
| `src/data_models/stage_model.py` | Stage 番号、Stage 名、ステータス、Skip 理由、成果物、更新日時、メモを表す |
| `src/data_models/artifact_model.py` | 成果物名、ファイルパス、ファイル種別、生成元 Phase / Stage、更新日時を表す |
| `src/data_models/audit_log_model.py` | `audit/` 配下から取得する最近の更新履歴を表す |
| `src/data_models/dashboard_settings_model.py` | 自動更新、更新間隔、表示件数、テーマなどの表示設定を表す |

### file_readers

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/file_readers/` | AIDLC 関連ファイルを探して読み込む処理を置く |
| `src/file_readers/config_yml_reader.py` | `config.yml` を読み込む |
| `src/file_readers/aidlc_intent_path_finder.py` | `aidlc/spaces/default/intents/<intent>/` の場所を特定する |
| `src/file_readers/aidlc_state_file_reader.py` | `aidlc-state.md` を読み込む |
| `src/file_readers/aidlc_phase_files_reader.py` | `ideation/`、`inception/` など各 Phase 配下のファイルを一覧取得・読み込みする |
| `src/file_readers/aidlc_audit_files_reader.py` | `audit/` 配下の更新履歴ファイルを一覧取得・読み込みする |
| `src/file_readers/aidlc_artifact_files_reader.py` | 成果物として表示するファイルを一覧取得・読み込みする |
| `src/file_readers/aidlc_version_file_reader.py` | `core/tools/aidlc-version.ts` を読み込む |

### aidlc_data_extractors

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/aidlc_data_extractors/` | 読み込んだファイル内容から AIDLC の表示対象データを抜き出す |
| `src/aidlc_data_extractors/aidlc_state_markdown_extractor.py` | `aidlc-state.md` から現在 Phase、現在 Stage、Scope/Profile などを抜き出す |
| `src/aidlc_data_extractors/aidlc_phase_stage_extractor.py` | 各 Phase 配下から Stage 情報、Skip 理由、承認待ち情報などを抜き出す |
| `src/aidlc_data_extractors/aidlc_audit_log_extractor.py` | `audit/` 配下ファイルから最近の更新履歴を抜き出す |
| `src/aidlc_data_extractors/aidlc_artifact_metadata_extractor.py` | 成果物ファイルからファイル種別、更新日時、表示名などのメタ情報を抜き出す |
| `src/aidlc_data_extractors/aidlc_release_version_extractor.py` | `core/tools/aidlc-version.ts` から `v2.9.1` のような AIDLC リリースバージョンを抜き出す |

### display_data_builders

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/display_data_builders/` | 画面表示用にデータを集計・整形する |
| `src/display_data_builders/dashboard_display_data_builder.py` | Dashboard 画面用に、サマリー、現在 Stage、次 Stage、最近の更新を作る |
| `src/display_data_builders/workflow_display_data_builder.py` | Workflow 画面用に、Phase 一覧、Stage 一覧、ステータス別件数を作る |
| `src/display_data_builders/artifacts_display_data_builder.py` | Artifacts 画面用に、成果物一覧、フィルタ候補、選択中成果物詳細を作る |
| `src/display_data_builders/settings_display_data_builder.py` | Settings 画面用に、現在の設定値と選択肢を作る |

### artifact_previewers

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/artifact_previewers/` | 成果物ファイルのプレビュー表示用データを作る |
| `src/artifact_previewers/markdown_artifact_previewer.py` | `.md` ファイルを Markdown プレビュー用に変換する |
| `src/artifact_previewers/csv_artifact_previewer.py` | `.csv` ファイルを表形式プレビュー用に変換する |
| `src/artifact_previewers/text_artifact_previewer.py` | `.txt` ファイルをテキストプレビュー用に変換する |
| `src/artifact_previewers/json_artifact_previewer.py` | `.json` ファイルを整形済み JSON プレビュー用に変換する |
| `src/artifact_previewers/yaml_artifact_previewer.py` | `.yaml` / `.yml` ファイルを YAML プレビュー用に変換する |
| `src/artifact_previewers/image_artifact_previewer.py` | `.png` / `.jpg` / `.jpeg` ファイルを画像プレビュー用に変換する |

### dashboard_config

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/dashboard_config/` | `config.yml` の読み込み、保存、初期値管理を行う |
| `src/dashboard_config/dashboard_config_loader.py` | `config.yml` を読み込み、アプリ用設定として扱う |
| `src/dashboard_config/dashboard_config_saver.py` | Settings 画面から変更された値を `config.yml` に保存する |
| `src/dashboard_config/default_dashboard_config.py` | `config.yml` がない場合やリセット時の初期値を定義する |

### styles

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/styles/` | CSS やテーマ適用処理を置く |
| `src/styles/custom_streamlit_style.css` | 添付画像のようなカード、サイドバー、バッジ、テーブル見た目を調整する CSS |
| `src/styles/streamlit_style_loader.py` | CSS ファイルを Streamlit に読み込ませる |

### common_helpers

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `src/common_helpers/` | 複数箇所で使う小さな共通処理を置く |
| `src/common_helpers/datetime_display_formatter.py` | 日時を `YYYY/MM/DD HH:mm` などの表示形式に変換する |
| `src/common_helpers/artifact_file_type_detector.py` | 拡張子からドキュメント、図表、表、コード、その他を判定する |
| `src/common_helpers/stage_status_normalizer.py` | AIDLC 側の状態表記を、完了・進行中・未着手・Skip・承認待ちに正規化する |
| `src/common_helpers/markdown_heading_extractor.py` | Markdown から見出しや概要を抽出する |
| `src/common_helpers/safe_file_path_formatter.py` | 画面表示用にファイルパスを安全に整形する |

### sample_data

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `sample_data/` | 開発・テスト用の AIDLC サンプルデータを置く |
| `sample_data/aidlc/spaces/default/intents/sample_intent/aidlc-state.md` | サンプルの AIDLC 状態ファイル |
| `sample_data/aidlc/spaces/default/intents/sample_intent/audit/` | サンプルの更新履歴ファイル |
| `sample_data/aidlc/spaces/default/intents/sample_intent/ideation/` | サンプルの Ideation 成果物 |
| `sample_data/aidlc/spaces/default/intents/sample_intent/inception/` | サンプルの Inception 成果物 |
| `sample_data/aidlc/spaces/default/intents/sample_intent/construction/` | サンプルの Construction 成果物 |
| `sample_data/aidlc/spaces/default/intents/sample_intent/operation/` | サンプルの Operation 成果物 |
| `sample_data/aidlc/spaces/default/intents/sample_intent/verification/` | サンプルの Verification 成果物 |

### tests

| ディレクトリ / ファイル名 | どんな処理をする想定か |
|---|---|
| `tests/` | テストコードを置く |
| `tests/file_readers/` | ファイル読み込み処理のテスト |
| `tests/aidlc_data_extractors/` | AIDLC 情報抽出処理のテスト |
| `tests/display_data_builders/` | 画面表示用データ生成処理のテスト |
| `tests/artifact_previewers/` | 成果物プレビュー処理のテスト |
| `tests/common_helpers/` | 共通処理のテスト |

## データ処理の流れ

```text
config.yml
  ↓
file_readers/
  AIDLC のファイルを探して読む
  ↓
aidlc_data_extractors/
  AIDLC に必要な情報を抜き出す
  ↓
data_models/
  アプリ内で扱うデータの形にする
  ↓
display_data_builders/
  各画面で表示しやすい形に整える
  ↓
screens/ + ui_parts/
  Streamlit で表示する
```

## 今後の実装方針

1. `config.yml` の項目を定義する
2. サンプル AIDLC データを用意する
3. `file_readers/` でファイル読み込み処理を作る
4. `aidlc_data_extractors/` で必要情報を抽出する
5. `data_models/` でアプリ内データ構造を定義する
6. `display_data_builders/` で画面表示用データを作る
7. `screens/` と `ui_parts/` で Streamlit UI を実装する
8. 添付画像に近づくように `styles/` で見た目を調整する
