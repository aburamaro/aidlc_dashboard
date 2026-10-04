# AIDLC Workflow Dashboard UI要件

## 1. 概要
AWS Workflows（AIDLC）の実行状況を可視化する、開発者向けのWebダッシュボードを作成する。
UIフレームワークには **Python Streamlit** を使用する。
本ツールはAIDLCそのものを操作するツールではなく、AIDLCの状態・進捗・成果物を確認するための **Read Onlyの可視化ダッシュボード** とする。
AIDLC v1 / v2 の両方に対応できる構成とする。

---

## 2. 背景・課題
現在AIDLCを利用して開発している際、以下の課題がある。
- 現在どのPhaseにいるのか分かりにくい
- 現在どのStageを実行しているのか分かりにくい
- 各Stageが完了・進行中・未着手・Skipのどの状態なのか一目で分からない
- SkipされたStageを確認するためにディレクトリやファイルを見る必要がある
- StageがSkipされた理由もファイルを確認しないと分からない
- 人間の承認待ちになっているStageが分かりにくい
- どのStageでどの成果物が生成されたのか確認しづらい
- AIDLC v2ではStage数が多いため、全体の現在地を把握しづらい

そのため、
> 「AIDLCが今どこまで進んでいるのか」を開発者が数秒で把握できる
ことを最重要目的とする。

---

## 3. 想定ユーザー

### ペルソナ
AIDLCを使用してアプリケーション開発を行う開発者。
主な利用目的は以下。
- AIDLCの現在地を確認する
- Workflow全体の進捗を確認する
- 現在実行中のStageを確認する
- 次に実行されるStageを確認する
- SkipされたStageと理由を確認する
- 人間の承認が必要なStageを確認する
- AIDLCによって生成された成果物を確認する

---

## 4. 基本方針

### 4.1 Read Only
本DashboardからAIDLCの状態を変更しない。
以下の操作は実装対象外とする。
- Stageの開始
- Stageの完了
- StageのSkip
- Scope/Profileの変更
- Approvalの実行
- Agentの変更
- AIDLC Versionの変更
- 成果物の編集
- AIDLC Workflowそのものの設定変更

DashboardはAIDLCの状態を読み取って表示することに専念する。

---

### 4.2 AIDLC v1 / v2対応
AIDLC v1 / v2の両方に対応する。
UI側では可能な限りv1/v2固有のPhase数・Stage数をハードコードしない。

イメージ：

```text
AIDLC v1
    ↓
Parser
    ↓
共通データモデル
    ↓
Streamlit UI


AIDLC v2
    ↓
Parser
    ↓
共通データモデル
    ↓
Streamlit UI
```

Phase / Stageの数が変わっても同じUIコンポーネントで表示できる構成を目指す。

---

## 5. 画面構成
サイドバーを使用し、以下の4画面を用意する。

```text
AIDLC

├── Dashboard
│     └── Workflow全体の概要
│
├── Workflow
│     └── Phase / Stage詳細
│
├── Artifacts
│     └── 成果物一覧
│
└── Settings
      └── Dashboard表示・更新設定
```

サイドバーは全画面共通とする。

---

## 6. 共通サイドバー
以下を表示する。

```text
AIDLC
ワークフローダッシュボード

Dashboard
  全体の進捗を確認

Workflow
  フェーズ・ステージ詳細

Artifacts
  成果物一覧

設定
  表示設定
```

現在選択しているメニューを視覚的に強調する。

例：

- 選択中：青背景
- 未選択：ダーク背景

---

## 7. Dashboard画面

### 7.1 目的
Dashboardを開いた瞬間に、

- どのAIDLC Versionか
- Workflowが進行中か完了か
- どのScope/Profileか
- 全Stageのうち何Stage完了しているか
- 現在どのPhaseにいるか
- 現在どのStageを実行しているか
- 次にどのStageを実行するか
- 人間の承認待ちが存在するか
- 最近何が更新されたか

を把握できること。

---

### 7.2 上部Summary
カード形式で以下を表示する。

#### AIDLC Version
例：

```text
AIDLCバージョン
v2
```

VersionはAIDLCから自動判定する。

ユーザーが変更する機能は持たせない。

---

#### Workflow全体ステータス
例：

```text
ワークフロー全体ステータス
進行中
```

想定値：

- 進行中
- 完了

必要に応じて将来的なステータス追加に対応できる構造にする。

---

#### Scope / Profile
例：

```text
Scope / Profile
feature
```

AIDLCから取得した情報を表示する。

変更機能は持たせない。

---

#### Stage進捗
割合（%）ではなく、

```text
13 / 33
Stage完了
```

の形式で表示する。

進捗率の%表示は不要。

---

### 7.3 Workflow Progress
Phase単位の全体進捗を横方向に表示する。

例：

```text
Initialization
3 / 3 完了
      ↓
Ideation
5 / 5 完了
      ↓
Inception
2 / 6 完了
      ↓
Construction
0 / 12 完了
      ↓
Operation
0 / 7 完了
```

状態によって色を変更する。

#### 色の基本ルール

| 状態 | 色 |
|---|---|
| 完了 | 緑 |
| 進行中 | 青 |
| 未着手 | グレー |
| Skip | 必要に応じて赤/グレー系 |
| 承認待ち | オレンジ |

現在のPhaseは視覚的に強調する。

---

## 8. Dashboard：Current / Next Stage
現在のStageと次のStageを表示する。

Current → Nextという処理順序が理解しやすいようにする。

例：

```text
現在のステージ

Inception
User Stories
進行中


        ↓


次のステージ

Inception
Application Design
未着手
```

現在のStageには以下の情報を表示可能とする。

- Phase
- Stage
- Status
- 開始時刻
- 必要に応じて経過時間

次のStageには以下を表示する。

- Phase
- Stage
- Status

---

## 9. Dashboard：承認待ち
人間の承認が必要なStageが存在する場合、分かりやすく表示する。
ただし、Dashboard下部に「承認待ち一覧」の大きな一覧表は配置しない。

Current / Next Stage付近などで、
```text
承認待ち

API Design
人間による確認が必要
```

程度の情報を表示する。
承認待ちはオレンジなどの警告色で表現する。
Dashboardから承認操作そのものは行わない。

---

## 10. Dashboard：最近の更新
Dashboard最下部に配置する。

例：

```text
最近の更新

00:45  Inception      User Stories           進行中
00:42  Inception      Requirements Analysis  完了
00:30  Inception      -                      開始
00:15  Ideation       Ideation Summary       完了
00:10  Initialization Environment Setup      完了
```

最低限以下の情報を持つ。

- 時刻
- Phase
- Stage
- Status
- 概要

最新の更新を上に表示する。

---

## 11. Workflow画面

### 11.1 目的
AIDLC全体のPhase / Stageの詳細状況を確認する画面。
Dashboardより詳細な情報を表示する。

---

### 11.2 上部Status Filter
以下のステータスをタグ/ボタン形式で表示する。
例：

```text
すべて (33)
完了 (13)
進行中 (1)
未着手 (17)
スキップ (1)
承認待ち (1)
```

各タグには対象Stage数を表示する。
可能であればクリックすると対象StatusのStageだけ表示できるようにする。

---

## 12. Workflow：Phase Accordion
Phase単位でアコーディオン表示する。

例：

```text
Initialization       3 / 3 完了
Ideation             5 / 5 完了
Inception            2 / 6 進行中
Construction         0 / 12 未着手
Operation            0 / 7 未着手
```

### デフォルト表示

基本動作：
```text
完了Phase
→ CLOSED

現在進行中Phase
→ OPEN

未来Phase
→ CLOSED
```

設定画面で「完了Phaseをデフォルトで閉じる」を変更可能とする。

---

### 12.1 Phase状態表示
Phaseごとに、
- Phase番号
- Phase名
- 説明
- Stage完了数
- Stage総数
- Status

を表示する。

例：

```text
3  Inception

要件定義・設計

2 / 6 完了

進行中
```

---

## 13. Workflow：Stage一覧
Phaseアコーディオンを開くとStage一覧を表示する。

表示項目：

| 項目 | 内容 |
|---|---|
| No | Stage番号 |
| Stage | Stage名 |
| Status | Stage状態 |
| Skip理由 | Skipされた理由 |
| 成果物 | Stageで生成された成果物 |
| 更新日時 | 最終更新日時 |
| メモ | 必要に応じた補足 |

例：

```text
3-1 Requirements Analysis  完了
3-2 User Stories           進行中
3-3 Application Design     未着手
3-4 Data Model             未着手
3-5 API Design             承認待ち
3-6 Inception Summary      未着手
```

---

## 14. Stage Status
最低限以下のStatusに対応する。

```text
完了
進行中
未着手
Skip
承認待ち
```

色：

```text
完了       → 緑
進行中     → 青
未着手     → グレー
Skip       → 赤またはグレー系
承認待ち   → オレンジ
```

StatusはBadge形式などで視覚的に判別しやすくする。

---

## 15. Skip Stage
SkipされたStageについて、

```text
Stage
Status
Skip Reason
```

を確認できるようにする。

例：

```text
Market Research

Status:
Skip

Reason:
Scope対象外
```

単にStageが存在しない場合と、意図的にSkipされた場合を区別する。

---

## 16. Approval

人間の承認が必要なStageはWorkflow画面でも明確に表示する。

例：

```text
API Design

承認待ち

設計内容の確認が必要
```

Phase内に承認待ちStageが存在する場合、

Phaseを閉じていても可能であれば、

```text
Inception
2 / 6
承認待ち 1
```

のように把握できるようにする。

---

## 17. Artifacts画面

### 17.1 目的
AIDLCによって生成された成果物を一覧で確認する。

---

### 17.2 フィルタ
以下のフィルタを用意する。

- Phase
- Stage
- File Type
- Status

検索欄も設ける。

例：

```text
成果物を検索...
```

---

### 17.3 ファイル種別
必要に応じて以下の分類を行う。

```text
すべて
ドキュメント
図表
表
コード
その他
```

それぞれ件数を表示可能とする。

---

## 18. Artifacts一覧
最低限以下を表示する。

| 項目 | 内容 |
|---|---|
| Phase | 生成元Phase |
| Stage | 生成元Stage |
| Artifact | 成果物名 |
| File Type | ファイル種別 |
| Updated | 更新日時 |
| Action | ダウンロード等 |

例：

```text
Initialization | Workspace Detection     | workspace-info.md
Ideation       | Business Ideation       | business-ideation.md
Inception      | Requirements Analysis   | requirements.md
Inception      | User Stories            | user-stories.md
```

---

## 19. Artifact詳細
成果物を選択した場合、可能であれば右側などに詳細を表示する。

表示候補：

- ファイル名
- Status
- Phase
- Stage
- Preview
- 概要
- メタ情報
- ファイルパス

操作候補：

```text
ダウンロード
ファイルパスをコピー
```

成果物の編集機能は持たせない。

---

## 20. Settings画面

### 20.1 基本方針
SettingsはAIDLCそのものを設定する画面ではない。

設定対象は、

> Dashboardの表示方法・データ更新方法

のみとする。

---

## 21. Settings：データ取得設定

### 自動更新
```text
自動更新

ON / OFF
```

ONの場合、一定間隔でAIDLCの状態を再取得する。

---

### 更新間隔
候補：

```text
5秒
10秒
30秒
60秒
```

自動更新ONの場合のみ有効。

---

## 22. Settings：表示設定

### 完了したPhaseをデフォルトで閉じる
```text
ON / OFF
```

ON：

```text
✓ Initialization  CLOSED
✓ Ideation        CLOSED
● Inception       OPEN
```

---

## 現在のPhaseを自動展開

```text
ON / OFF
```

Dashboard / Workflowを開いた際に現在進行中のPhaseを自動展開する。

初期値はON。

---

## Skip Stageを表示

```text
ON / OFF
```

ON：
SkipされたStageをWorkflowに表示。

OFF：
SkipされたStageを非表示。

---

## 日時表示形式

必要に応じて選択可能とする。

例：

```text
YYYY/MM/DD HH:mm
YYYY-MM-DD HH:mm
```

---

## 23. Settings：画面表示設定（Optional）
初期版で余裕があれば実装する。

### Theme

```text
Light
Dark
```

初期値：

```text
Light
```

---

### 1ページあたりの表示件数
Artifactsなどの一覧画面に利用。

例：

```text
10
20
50
```

---

## 24. Settings：設定リセット
以下のボタンを設ける。

```text
デフォルト設定に戻す
```

Dashboardの表示設定・更新設定を初期値へ戻す。

AIDLCのWorkflowデータには一切影響を与えない。

---

## 25. Settingsに含めないもの
以下は設定画面から操作させない。

```text
AIDLC Version
AIDLC Scope/Profile
AIDLC Project Path
Artifact Root Directory
Stage Status
Stage Skip
Approval
Agent
AIDLC Workflow設定
```

これらはAIDLC側の情報として読み取る。

---

## 26. 更新日時
Dashboard / Workflow / Artifacts等で、

```text
最終更新日時

2026/10/04 00:45:12
```

を表示する。

必要に応じて手動更新ボタンも設置する。

```text
更新
```

---

## 27. デザイン方針
全体として開発者向けのシンプルで視認性の高いDashboardとする。

### 基本

- Light Themeを基本とする
- 左側にDark系Sidebar
- Main Contentは白系
- Card UIを使用
- 角丸を使用
- 過剰な装飾は避ける
- 情報密度は高めでもよいが、状態を瞬時に判別できることを優先する

### Status Color

```text
Completed
→ Green

Active
→ Blue

Pending
→ Gray

Skipped
→ Red / Gray

Awaiting Approval
→ Orange
```

色だけに依存せず、

```text
アイコン + 色 + テキスト
```

でStatusを表現する。

---

## 28. Streamlit実装方針
Python Streamlitで実装する。

React等の独自フロントエンドへの置き換えは行わない。

Streamlit標準機能を可能な限り活用する。

利用候補：

```python
st.sidebar
st.navigation
st.Page
st.container
st.columns
st.metric
st.expander
st.dataframe
st.status
st.badge
st.toggle
st.selectbox
st.radio
st.button
```

Phase / Stage表示には `st.expander` 等を利用し、アコーディオンUIを実現する。

---

## 29. 初期画面

アプリケーション起動時は、

```text
Dashboard
```

を表示する。

---

## 30. 画面遷移
```text
                    ┌────────────────┐
                    │   Dashboard    │
                    │                │
                    │ 全体進捗       │
                    │ Current Stage  │
                    │ Next Stage     │
                    │ 最近の更新     │
                    └───────┬────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼

     ┌──────────┐     ┌───────────┐    ┌──────────┐
     │ Workflow │     │ Artifacts │    │ Settings │
     │          │     │           │    │          │
     │Phase     │     │成果物一覧 │    │表示設定  │
     │Stage     │     │Preview    │    │更新設定  │
     │Status    │     │Download   │    │          │
     │Skip理由  │     │           │    │          │
     └──────────┘     └───────────┘    └──────────┘
```

すべての画面はSidebarから直接遷移可能とする。

---

## 31. UIで最重要なこと
本Dashboardで最も重要なのは、

> 情報量の多さではなく、AIDLCの現在地を瞬時に理解できること。

開発者がDashboardを開いて数秒以内に、

```text
AIDLC v2
feature
Workflow進行中

13 / 33 Stage完了

現在：
Inception
└ User Stories

次：
Application Design

承認待ち：
API Design
```

まで理解できるUIを目指す。

---

## 32. 参考画像
別途提供する以下4枚のUIモックアップ画像をデザイン参考として使用する。

1. Dashboard画面
2. Workflow画面
3. Artifacts画面
4. Settings画面

画像を完全にピクセル単位でコピーする必要はない。

Streamlitで実現可能な範囲で、

- 情報の優先順位
- レイアウト
- Status表現
- Card構成
- Sidebar
- Accordion
- Table
- Filter

を再現する。

特に機能要件については、本Markdownの内容を正とする。