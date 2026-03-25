from flask import Flask, render_template, request, send_file, Response, jsonify
import threading
import json
import os
import queue
import time

from core.scanner import WebScanner

app = Flask(__name__)

# 全局进度队列：每次扫描创建一个，用 scan_id 隔离
_scan_queues = {}
_scan_lock = threading.Lock()


def get_or_create_queue(scan_id):
    with _scan_lock:
        if scan_id not in _scan_queues:
            _scan_queues[scan_id] = queue.Queue()
        return _scan_queues[scan_id]


def cleanup_queue(scan_id, delay=30):
    """扫描结束后延迟清理队列，避免客户端还没读完就被删除"""
    def _cleanup():
        time.sleep(delay)
        with _scan_lock:
            _scan_queues.pop(scan_id, None)
    threading.Thread(target=_cleanup, daemon=True).start()


def run_scan_async(scan_id, target):
    q = get_or_create_queue(scan_id)

    def progress_callback(stage, message, percent):
        """被 scanner 调用，把进度事件放入队列"""
        event = {
            "stage": stage,
            "message": message,
            "percent": percent
        }
        q.put(("progress", event))

    try:
        # 删除旧报告
        if os.path.exists("scan_report.json"):
            os.remove("scan_report.json")

        scanner = WebScanner(target, depth=2, progress_callback=progress_callback)
        scanner.start()

        # 扫描完成，读取报告推入队列
        report_data = None
        if os.path.exists("scan_report.json"):
            with open("scan_report.json", "r", encoding="utf-8") as f:
                report_data = json.load(f)

        q.put(("done", report_data))

    except Exception as e:
        q.put(("error", str(e)))

    finally:
        cleanup_queue(scan_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def start_scan():
    """接收扫描请求，立即返回 scan_id，前端凭此订阅 SSE"""
    data = request.get_json()
    target = data.get("url", "").strip() if data else ""

    if not target:
        return jsonify({"error": "URL is required"}), 400

    # 用时间戳作为简单的 scan_id
    scan_id = str(int(time.time() * 1000))
    get_or_create_queue(scan_id)  # 提前创建队列，避免 SSE 连接先于线程启动

    thread = threading.Thread(target=run_scan_async, args=(scan_id, target), daemon=True)
    thread.start()

    return jsonify({"scan_id": scan_id})


@app.route("/progress/<scan_id>")
def progress_stream(scan_id):
    """SSE 端点：持续推送扫描进度，直到扫描完成或出错"""

    def generate():
        q = get_or_create_queue(scan_id)

        while True:
            try:
                event_type, payload = q.get(timeout=60)  # 最多等 60 秒
            except queue.Empty:
                # 超时，发送心跳保持连接
                yield "event: heartbeat\ndata: {}\n\n"
                continue

            if event_type == "progress":
                yield f"event: progress\ndata: {json.dumps(payload)}\n\n"

            elif event_type == "done":
                yield f"event: done\ndata: {json.dumps(payload)}\n\n"
                break

            elif event_type == "error":
                yield f"event: error\ndata: {json.dumps({'message': payload})}\n\n"
                break

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"   # 关闭 Nginx 缓冲（生产环境必需）
        }
    )


@app.route("/download")
def download_report():
    return send_file("scan_report.json", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
