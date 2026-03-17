import datetime
import json


class ReportGenerator:

    def __init__(self):

        self.report_file = "scan_report.txt"

    def generate(self, sql_results, xss_results, dir_results, header_results):

        print("[ReportGenerator] Generating report")

        now = datetime.datetime.now()

        with open(self.report_file, "w", encoding="utf-8") as f:

            f.write("=====================================\n")
            f.write(" Mini Web Vulnerability Scan Report\n")
            f.write("=====================================\n\n")

            f.write(f"Scan Time: {now}\n\n")

            self.write_sql_section(f, sql_results)
            self.write_xss_section(f, xss_results)
            self.write_directory_section(f, dir_results)
            self.write_header_section(f, header_results)

        print(f"[ReportGenerator] Report saved to {self.report_file}")

        # 生成 JSON（用于 Web 展示）
        self.generate_json(
            sql_results,
            xss_results,
            dir_results,
            header_results
        )

    # =============================
    # 文本报告部分（保持你原有逻辑）
    # =============================

    def write_sql_section(self, file, results):

        file.write("------ SQL Injection Scan ------\n")

        if not results:
            file.write("No SQL Injection vulnerabilities found.\n\n")
        else:
            for url in results:
                file.write(f"Vulnerable URL: {url}\n")
            file.write("\n")

    def write_xss_section(self, file, results):

        file.write("------ XSS Scan ------\n")

        if not results:
            file.write("No XSS vulnerabilities found.\n\n")
        else:
            for url in results:
                file.write(f"Vulnerable URL: {url}\n")
            file.write("\n")

    def write_directory_section(self, file, results):

        file.write("------ Sensitive Directory Scan ------\n")

        if not results:
            file.write("No sensitive directories found.\n\n")
        else:
            for directory in results:
                file.write(f"Found directory: {directory}\n")
            file.write("\n")

    def write_header_section(self, file, results):

        file.write("------ HTTP Security Headers ------\n")

        if not results:
            file.write("All important security headers are present.\n\n")
        else:
            for header in results:
                file.write(f"Missing header: {header}\n")
            file.write("\n")

    # =============================
    # JSON 报告（🔥重点升级部分）
    # =============================

    def generate_json(self, sql_results, xss_results, dir_results, header_results):

        data = {

            "summary": {
                "sql_count": len(sql_results),
                "xss_count": len(xss_results),
                "dir_count": len(dir_results),
                "header_issues": len(header_results)
            },

            "sql_injection": {
                "risk": "HIGH" if sql_results else "LOW",
                "count": len(sql_results),
                "details": sql_results
            },

            "xss": {
                "risk": "HIGH" if xss_results else "LOW",
                "count": len(xss_results),
                "details": xss_results
            },

            "directories": {
                "risk": "MEDIUM" if dir_results else "LOW",
                "count": len(dir_results),
                "details": dir_results
            },

            "headers": {
                "risk": "MEDIUM" if header_results else "LOW",
                "count": len(header_results),
                "details": header_results
            }
        }

        json_file = "scan_report.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[ReportGenerator] JSON report saved to {json_file}")