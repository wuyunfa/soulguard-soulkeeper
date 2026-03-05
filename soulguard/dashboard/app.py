#!/usr/bin/env python3
"""
SoulGuard Web监控面板
"""

import sys
import json
import os
from datetime import datetime
sys.path.insert(0, '/root/.openclaw/soulguard')

from http.server import HTTPServer, BaseHTTPRequestHandler

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        if self.path == '/':
            self._serve_dashboard()
        elif self.path == '/api/status':
            self._serve_api_status()
        elif self.path == '/api/memories':
            self._serve_api_memories()
        else:
            self._serve_404()
    
    def _serve_dashboard(self):
        """服务主面板"""
        html = self._generate_html()
        self._send_response(200, 'text/html', html)
    
    def _serve_api_status(self):
        """服务API状态"""
        status = self._get_system_status()
        self._send_response(200, 'application/json', json.dumps(status))
    
    def _serve_api_memories(self):
        """服务记忆API"""
        memories = self._get_memories()
        self._send_response(200, 'application/json', json.dumps(memories))
    
    def _serve_404(self):
        self._send_response(404, 'text/plain', 'Not Found')
    
    def _send_response(self, code, content_type, content):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(content.encode() if isinstance(content, str) else content)
    
    def _get_system_status(self):
        """获取系统状态"""
        import psutil
        
        return {
            "timestamp": datetime.now().isoformat(),
            "memory": {
                "total": psutil.virtual_memory().total // (1024*1024),
                "used": psutil.virtual_memory().used // (1024*1024),
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total // (1024*1024*1024),
                "used": psutil.disk_usage('/').used // (1024*1024*1024),
                "percent": psutil.disk_usage('/').percent
            },
            "cpu": psutil.cpu_percent(interval=1),
            "soulguard": {
                "version": "v0.6.0",
                "status": "running"
            }
        }
    
    def _get_memories(self):
        """获取记忆统计"""
        data_dir = "/root/.openclaw/soulguard/memory_data"
        memories = []
        
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.json'):
                    filepath = os.path.join(data_dir, file)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            memories.append({
                                "file": file,
                                "count": len(data)
                            })
                    except:
                        pass
        
        return memories
    
    def _generate_html(self):
        """生成HTML页面"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>SoulGuard Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #00d4ff; }
        .card { background: #16213e; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .metric { display: inline-block; margin: 10px 20px; }
        .metric-value { font-size: 24px; color: #00d4ff; }
        .metric-label { font-size: 12px; color: #888; }
        .status-ok { color: #00ff88; }
        .status-warn { color: #ffaa00; }
        .status-error { color: #ff4444; }
    </style>
</head>
<body>
    <h1>🔮 SoulGuard Dashboard</h1>
    
    <div class="card">
        <h2>系统状态</h2>
        <div id="status">加载中...</div>
    </div>
    
    <div class="card">
        <h2>记忆统计</h2>
        <div id="memories">加载中...</div>
    </div>
    
    <script>
        async function loadStatus() {
            const res = await fetch('/api/status');
            const data = await res.json();
            
            document.getElementById('status').innerHTML = `
                <div class="metric">
                    <div class="metric-value">${data.memory.percent}%</div>
                    <div class="metric-label">内存使用</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${data.disk.percent}%</div>
                    <div class="metric-label">磁盘使用</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${data.cpu}%</div>
                    <div class="metric-label">CPU使用</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-ok">${data.soulguard.status}</div>
                    <div class="metric-label">SoulGuard状态</div>
                </div>
            `;
        }
        
        async function loadMemories() {
            const res = await fetch('/api/memories');
            const data = await res.json();
            
            let html = '<table style="width:100%">';
            html += '<tr><th>文件</th><th>记忆数</th></tr>';
            data.forEach(m => {
                html += `<tr><td>${m.file}</td><td>${m.count}</td></tr>`;
            });
            html += '</table>';
            
            document.getElementById('memories').innerHTML = html;
        }
        
        loadStatus();
        loadMemories();
        setInterval(loadStatus, 5000);
        setInterval(loadMemories, 10000);
    </script>
</body>
</html>
        '''

def start_dashboard(port=18790):
    """启动监控面板"""
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"SoulGuard Dashboard 启动于 http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    start_dashboard()
