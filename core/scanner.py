from core.crawler import Crawler

from report.report_generator import ReportGenerator

from utils.parameter_parser import ParameterParser
from utils.logger import Logger

from core.plugin_manager import PluginManager


class WebScanner:

    def __init__(self, target, depth, progress_callback=None):

        self.target = target
        self.depth = depth
        self.urls = []

        self.logger = Logger()

        # progress_callback(stage: str, message: str, percent: int)
        # 若未传入则使用空函数，保持向后兼容（CLI 直接调用时不受影响）
        self.progress = progress_callback or (lambda stage, msg, pct: None)

    def start(self):

        # ===== 1. 爬虫 =====
        self.progress("crawler", "Starting crawler...", 5)
        self.logger.info("Starting crawler")

        crawler = Crawler(self.target, self.depth)
        self.urls = crawler.crawl()

        msg = f"Crawler finished — found {len(self.urls)} URLs"
        print(f"[+] Found {len(self.urls)} URLs")
        self.progress("crawler", msg, 20)

        # ===== 2. 参数扩展 =====
        self.progress("params", "Parsing URL parameters...", 25)
        self.logger.info("Parsing URL parameters")

        parser = ParameterParser(self.urls)
        param_urls = parser.extract_parameters()
        generated_urls = parser.discover_common_parameters()

        self.urls.extend(param_urls)
        self.urls.extend(generated_urls)
        self.urls = list(set(self.urls))

        msg = f"Parameter expansion done — {len(self.urls)} total URLs"
        print(f"[+] Total URLs after parameter expansion: {len(self.urls)}")
        self.progress("params", msg, 35)

        # ===== 3. 插件扫描 =====
        self.progress("plugins", "Loading plugins...", 38)
        self.logger.info("Loading plugins")

        plugin_manager = PluginManager()
        plugin_manager.load_plugins()

        self.logger.info("Running plugins")

        # 把 progress_callback 传给 plugin_manager，让它在每个插件执行前后汇报
        results = plugin_manager.run_plugins(
            self.target,
            self.urls,
            progress_callback=self.progress
        )

        # ===== 4. 结果拆分 =====
        sql_results = results.get("sql_injection", [])
        xss_results = results.get("xss", [])
        dir_results = results.get("directories", [])
        header_results = results.get("headers", [])

        # ===== 5. 生成报告 =====
        self.progress("report", "Generating report...", 95)
        self.logger.info("Generating report")

        report = ReportGenerator()
        report.generate(sql_results, xss_results, dir_results, header_results)

        self.progress("report", "Scan complete!", 100)
