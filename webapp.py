from flask import Flask, render_template, request, send_file
import threading
import json
import os
import time
import logging

from core.scanner import WebScanner

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

app = Flask(__name__)


def run_scan(target):
    logging.info(f"Starting scan for target: {target}")
    scanner = WebScanner(target, depth=2)
    scanner.start()
    logging.info(f"Scan finished for target: {target}")


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    report_data = None

    if request.method == "POST":

        target = request.form.get("url")

        if target:

            logging.info(f"Received scan request: {target}")

            # 删除旧报告
            if os.path.exists("scan_report.json"):
                os.remove("scan_report.json")
                logging.info("Old scan report removed")

            # 启动扫描线程
            run_scan(target)

            # 等待扫描完成（最多等10秒）
            for _ in range(20):  # 20 * 0.5 = 10秒
                if os.path.exists("scan_report.json"):
                    logging.info("Scan report generated")
                    break
                time.sleep(0.5)

            # 读取 JSON 报告
            if os.path.exists("scan_report.json"):
                with open("scan_report.json", "r", encoding="utf-8") as f:
                    report_data = json.load(f)
                    logging.info("Scan report loaded successfully")
            else:
                logging.warning("Scan report not found after waiting")

            result = f"Scan completed for {target}"

    return render_template("index.html", result=result, report=report_data)


@app.route("/download")
def download_report():
    logging.info("Report download requested")
    return send_file("scan_report.json", as_attachment=True)


if __name__ == "__main__":
    logging.info("Starting Flask web application")
    app.run(debug=True)
