from flask import Flask, render_template, request, send_file
import threading
import json
import os
import time

from core.scanner import WebScanner

app = Flask(__name__)


def run_scan(target):
    scanner = WebScanner(target, depth=2)
    scanner.start()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    report_data = None

    if request.method == "POST":

        target = request.form.get("url")

        if target:

            # 删除旧报告
            if os.path.exists("scan_report.json"):
                os.remove("scan_report.json")

            # 启动扫描线程
            run_scan(target)

            # 等待扫描完成（最多等10秒）
            for _ in range(20):  # 20 * 0.5 = 10秒
                if os.path.exists("scan_report.json"):
                    break
                time.sleep(0.5)

            # 读取 JSON 报告
            if os.path.exists("scan_report.json"):
                with open("scan_report.json", "r", encoding="utf-8") as f:
                    report_data = json.load(f)

            result = f"Scan completed for {target}"

    return render_template("index.html", result=result, report=report_data)

@app.route("/download")
def download_report():
    return send_file("scan_report.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)