#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公文渲染引擎 V14 - API 服务

简单的 HTTP API 服务，用于接收 JSON 数据并生成 Word 公文。

启动方式：
python3 api_server.py

Docker 启动：
docker-compose up -d
"""

import os
import sys
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# 导入引擎
from gongwen_engine import generate_gongwen

# 导入数据校验
try:
    from schemas import validate_gongwen_data, format_validation_error
    VALIDATION_ENABLED = True
except ImportError:
    VALIDATION_ENABLED = False
    print("[WARN] pydantic not installed, validation disabled")

# 配置
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
HOST = "0.0.0.0"
PORT = 8001


class GongwenHandler(BaseHTTPRequestHandler):
    """公文 API 处理器"""

    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self._send_json(200, {
                "status": "healthy",
                "engine": "V14",
                "validation": VALIDATION_ENABLED,
                "timestamp": datetime.now().isoformat()
            })
        elif path == "/":
            self._send_json(200, {
                "service": "公文渲染引擎 V14",
                "docs": "POST /api/generate",
                "validation": VALIDATION_ENABLED
            })
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        path = urlparse(self.path).path

        if path not in ["/api/generate", "/api/gongwen/generate"]:
            self._send_json(404, {"error": "Not Found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                self._send_json(400, {"error": "Empty body"})
                return

            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            # 数据校验（如果启用）
            if VALIDATION_ENABLED:
                try:
                    validated_data = validate_gongwen_data(data)
                    data = validated_data.model_dump()
                except Exception as e:
                    self._send_json(400, format_validation_error(e))
                    return

            # 检查必填字段
            if not data.get("title"):
                self._send_json(400, {
                    "success": False,
                    "error": "缺少必填字段: title"
                })
                return

            # 生成文件名
            title = data.get("title", "公文")[:20].replace("/", "_")
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{title}_{date_str}.docx"
            output_path = os.path.join(OUTPUT_DIR, filename)

            # 确保输出目录存在
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            # 调用引擎
            result = generate_gongwen(data, output_path)

            self._send_json(200, {
                "success": True,
                "filename": filename,
                "path": result,
                "timestamp": datetime.now().isoformat()
            })

        except json.JSONDecodeError as e:
            self._send_json(400, {"error": f"Invalid JSON: {e}"})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {fmt % args}")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"""
╔════════════════════════════════════════════════════════════╗
║ 公文渲染引擎 V14 - API 服务 ║
╠════════════════════════════════════════════════════════════╣
║ 监听: http://{HOST}:{PORT} ║
║ 健康检查: GET /health ║
║ 生成公文: POST /api/generate ║
║ 数据校验: {"启用" if VALIDATION_ENABLED else "禁用"} ║
╚════════════════════════════════════════════════════════════╝
""")

    server = HTTPServer((HOST, PORT), GongwenHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()
