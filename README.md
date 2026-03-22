# port-mcp

LLMから現在のマシンの **開いているポート情報を取得できる MCP サーバー**です。
ローカル環境のネットワーク状態を取得し、LLMが分析しやすい **構造化データ(JSON)** で返します。

主な用途:

* ローカルPCのポート監視
* 開いているサービスの確認
* LLMエージェントによるネットワーク状況の把握
* セキュリティチェックの補助

---

# Features

このMCPサーバーは現在以下のツールを提供します。

## get_open_ports()

現在 **LISTEN状態のポート一覧** を取得します。

返却例:

```json
{
    "num_open_ports": 1,
    "open_ports":
        [
            {
                "process": "Python",
                "pid": 116,
                "protocol": "TCP",
                "port": 8889,
                "address": "127.0.0.1",
                "state": "LISTEN",
                "local_only": true
            }
        ]
}
```

フィールド説明

| field      | description     |
| ---------- | --------------- |
| process    | プロセス名           |
| pid        | プロセスID          |
| protocol   | TCP / UDP       |
| port       | ポート番号           |
| address    | バインドされているIP     |
| state      | 接続状態 (LISTENなど) |
| local_only | ローカルのみ公開かどうか    |

---

# Supported Platforms
Mac
Linux
Windows

# How it works

このサーバーは内部で以下のコマンドを使用します。
Mac, Linux の場合

```
lsof -i -P -n
```
Windowsの場合
```
lsof -i -P -n
```

取得した情報を解析し、LLMが扱いやすい形式に整形します。

処理フロー

```
lsof
 ↓
stdout取得
 ↓
ポート行を解析
 ↓
JSONに変換
 ↓
MCPツールとして返却
```

---

# Installation

```bash
git clone https://github.com/takata-hiroyuki/port-mcp
cd port-mcp
uv sync
```

---

# Run

```
uv run main.py
```

---

# Claude Desktop Integration

Claude Desktopで利用する場合、MCP 設定ファイルを開きます。

Mac:

~/Library/Application Support/Claude/claude_desktop_config.json

Windows:

%APPDATA%\Claude\claude_desktop_config.json

```
{
  "mcpServers": {
    "PortChecker": {
      "command": "uv",
      "args": [
        "--directory",
        "<プロジェクトフォルダの絶対パス>",
        "run",
        "main.py"
      ]
    }
  }
}
```
上記設定後、Claude Desktopを再起動してください。

---

# Example Usage (LLM)

LLMエージェントから:

```
現在開いているポートを教えて
```

LLMは `get_open_ports()` を呼び出し、結果を分析できます。

例:

* 外部公開ポートの検出
* 不審なプロセス確認
* 開発サーバー確認

---

# Project Structure

```
port-inspector-mcp
│
├─ main.py
├─ pyproject.toml
├─ README.md
└─ test_port.ipynb
```

---

# Future Ideas

今後追加予定の機能:

* `get_connections()`
  現在の接続一覧

* `get_process_ports(pid)`
  特定プロセスのポート情報

* ポート差分監視
  新しく開いたポートの検出

---

# Why MCP?

このツールをMCPとして提供することで

LLMが

* OS状態
* ネットワーク状態
* 実行プロセス

を **直接観測できるようになります。**

---

# License

MIT License
