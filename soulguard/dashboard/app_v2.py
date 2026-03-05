#!/usr/bin/env python3
"""
SoulGuard Dashboard v2.0 - 增强版
"""

import sys
sys.path.insert(0, '/root/.openclaw/soulguard')

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            '/': self._serve_dashboard,
            '/api/status': self._serve_status,
            '/api/memories': self._serve_memories,
            '/api/timeline': self._serve_timeline,
            '/api/graph': self._serve_graph,
            '/api/stats': self._serve_stats
        }
        
        handler = routes.get(self.path, self._serve_404)
        handler()
    
    def _serve_dashboard(self):
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>SoulGuard Dashboard v2</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee; 
            min-height: 100vh;
        }
        .header { 
            background: rgba(0,0,0,0.3); 
            padding: 20px; 
            text-align: center;
            border-bottom: 2px solid #00d4ff;
        }
        .header h1 { color: #00d4ff; font-size: 2em; }
        .container { display: flex; flex-wrap: wrap; padding: 20px; gap: 20px; }
        .card { 
            background: rgba(255,255,255,0.05);
            border-radius: 12px; 
            padding: 20px; 
            flex: 1 1 300px;
            border: 1px solid rgba(0,212,255,0.2);
        }
        .card h2 { color: #00d4ff; margin-bottom: 15px; }
        .metric { 
            display: inline-block; 
            margin: 10px 15px; 
            text-align: center;
        }
        .metric-value { 
            font-size: 32px; 
            font-weight: bold;
            color: #00d4ff; 
        }
        .metric-label { font-size: 12px; color: #888; }
        .status-ok { color: #00ff88; }
        .status-warn { color: #ffaa00; }
        .status-error { color: #ff4444; }
        .timeline-item { 
            padding: 10px; 
            margin: 5px 0;
            background: rgba(0,0,0,0.2);
            border-radius: 6px;
            border-left: 3px solid #00d4ff;
        }
        .refresh-btn {
            background: #00d4ff;
            color: #1a1a2e;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔮 SoulGuard Dashboard v2.0</h1>
        <p>让AI灵魂延续</p>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>系统状态</h2>
            <div id="system-stats">加载中...</div>
        </div>
        
        <div class="card">
            <h2>记忆统计</h2>
            <div id="memory-stats">加载中...</div>
        </div>
        
        <div class="card">
            <h2>时间线</h2>
            <div id="timeline">加载中...</div>
        </div>
        
        <div class="card">
            <h2>操作</h2>
            <button class="refresh-btn" onclick="refreshAll()">刷新数据</button>
            <div id="actions" style="margin-top: 20px;"></div>
        </div>
    </div>
    
    <script>
        async function loadSystemStats() {
            const res = await fetch('/api/status');
            const data = await res.json();
            
            document.getElementById('system-stats').innerHTML = `
                <div class="metric">
                    <div class="metric-value">${data.memory.percent}%</div>
                    <div class="metric-label">内存</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${data.cpu}%</div>
                    <div class="metric-label">CPU</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-ok">${data.soulguard.status}</div>
                    <div class="metric-label">SoulGuard</div>
                </div>
            `;
        }
        
        async function loadMemoryStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            
            document.getElementById('memory-stats').innerHTML = `
                <div class="metric">
                    <div class="metric-value">${data.total_memories}</div>
                    <div class="metric-label">总记忆</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${data.total_users}</div>
                    <div class="metric-label">用户数</div>
                </div>
            `;
        }
        
        async function loadTimeline() {
            const res = await fetch('/api/timeline');
            const data = await res.json();
            
            let html = '';
            Object.entries(data).slice(0, 5).forEach(([date, memories]) => {
                html += `<div class="timeline-item">
                    <strong>${date}</strong> - ${memories.length} 条记忆
                </div>`;
            });
            
            document.getElementById('timeline').innerHTML = html;
        }
        
        function refreshAll() {
            loadSystemStats();
            loadMemoryStats();
            loadTimeline();
        }
        
        refreshAll();
        setInterval(refreshAll, 10000);
    </script>
</body>
</html>
        '''
        self._send_response(200, 'text/html', html)
    
    def _serve_status(self):
        import psutil
        status = {
            "timestamp": datetime.now().isoformat(),
            "memory": {
                "percent": psutil.virtual_memory().percent
            },
            "cpu": psutil.cpu_percent(interval=1),
            "soulguard": {"status": "running", "version": "v0.11.0"}
        }
        self._send_json(status)
    
    def _serve_stats(self):
        data_dir = "/root/.openclaw/soulguard/memory_data"
        total_memories = 0
        users = set()
        
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.json'):
                    user = file.replace('_memories.json', '')
                    users.add(user)
                    try:
                        with open(os.path.join(data_dir, file)) as f:
                            import json
                            data = json.load(f)
                            total_memories += len(data)
                    except:
                        pass
        
        self._send_json({
            "total_memories": total_memories,
            "total_users": len(users)
        })
    
    def _serve_timeline(self):
        from memory_core.enhanced import SoulMemoryEnhanced
        sm = SoulMemoryEnhanced("default")
        timeline = sm.get_timeline()
        self._send_json(timeline)
    
    def _serve_memories(self):
        self._send_json([])
    
    def _serve_graph(self):
        self._send_json({"nodes": [], "edges": {}})
    
    def _serve_404(self):
        self._send_response(404, 'text/plain', 'Not Found')
    
    def _send_json(self, data):
        self._send_response(200, 'application/json', json.dumps(data))
    
    def _send_response(self, code, content_type, content):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(content.encode() if isinstance(content, str) else content)

def start_dashboard(port=18790):
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f"SoulGuard Dashboard v2.0 启动于 http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == '__main__':
    start_dashboard()
