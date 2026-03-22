from mcp.server.fastmcp import FastMCP
import subprocess
import platform
import csv
import io

mcp = FastMCP("port-mcp")
print("Starting port-mcp...")

@mcp.tool()
def get_open_ports():
    """空いているポートを取得する
    Returns:
            {
                num_open_ports: 空いているポートの数
                open_ports: 空いているポートのリスト。各要素は辞書で、以下のキーを持つ。
                    - process: プロセス名
                    - pid: プロセスID
                    - protocol: プロトコル (TCP/UDP)
                    - port: ポート番号
                    - state: ポートの状態 (LISTENなど)
                    - is_local: ローカルアドレスかどうか (True/False)
            }
    """

    if platform.system() != "Windows": 
        #lsof -inP コマンドを実行して、空いているポートを取得する
        result = subprocess.run([
            "lsof", "-i", "-n", "-P"
            ],
            capture_output=True, 
            text=True)
        open_ports = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            process = parts[0]
            if len(parts) == 10:
                state = parts[9].replace("(", "").replace(")", "")
            else:
                state = "NONE"
            pid = parts[1]
            protocol = parts[7]
            address = parts[8]
            port = address.split(":")[-1]
            is_local = address.startswith("127.0.0.1")
            open_ports.append({
                "process": process,
                "pid": pid,
                "protocol": protocol,
                "port": port,
                "state": state,
                "is_local": is_local
            })
        return {
            "num_open_ports": len(open_ports),
            "open_ports": open_ports
            }
    else:
        pid_map = get_pid_map()
        #netstat -ano コマンドを実行して、空いているポートを取得する
        result = subprocess.run([
            "netstat", "-ano"
            ],
            capture_output=True,
            text=True)
        open_ports = []
        for line in result.stdout.splitlines()[5:]:
            part = line.split()
            protocol = part[0]
            if protocol == "UDP":
                state = "NONE"
            else:
                state = part[3]
            pid = part[-1]
            process = pid_map[pid]
            protocol = part[0]
            address = part[1]
            port = address.split(":")[-1]
            is_local = address.startswith(("127.", "[::1]"))
            open_ports.append({
                "process": process,
                "pid": pid,
                "protocol": protocol,
                "port": port,
                "state": state,
                "is_local": is_local
            })
        return {
            "num_open_ports": len(open_ports),
            "open_ports": open_ports
        }

def get_pid_map():
    """ pid とprocess名を紐づける辞書作成メソッド"""
    result = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],capture_output=True, text=True
    )
    pid_map = {}
    reader = csv.reader(io.StringIO(result.stdout))
    for row in reader:
        pid_map[row[1]] = row[0]
    return pid_map
    
if __name__ == "__main__":
    """メイン"""
    mcp.run(transport="stdio")
