from core.crawler import Crawler

from report.report_generator import ReportGenerator

from utils.parameter_parser import ParameterParser
from utils.logger import Logger

from core.plugin_manager import PluginManager


class WebScanner:

    def __init__(self, target, depth):

        self.target = target
        self.depth = depth
        self.urls = []

        self.logger = Logger()

    def start(self):

        # ===== 1. 爬虫 =====
        self.logger.info("Starting crawler")

        crawler = Crawler(self.target, self.depth)

        self.urls = crawler.crawl()

        print(f"[+] Found {len(self.urls)} URLs")

        # ===== 2. 参数扩展 =====
        self.logger.info("Parsing URL parameters")

        parser = ParameterParser(self.urls)

        param_urls = parser.extract_parameters()

        generated_urls = parser.discover_common_parameters()

        self.urls.extend(param_urls)
        self.urls.extend(generated_urls)

        self.urls = list(set(self.urls))

        print(f"[+] Total URLs after parameter expansion: {len(self.urls)}")

        # ===== 3. 插件扫描 =====
        self.logger.info("Loading plugins")

        plugin_manager = PluginManager()

        plugin_manager.load_plugins()

        self.logger.info("Running plugins")

        results = plugin_manager.run_plugins(self.target, self.urls)

        # ===== 4. 结果拆分 =====
        sql_results = results.get("sql_injection", [])
        xss_results = results.get("xss", [])
        dir_results = results.get("directories", [])
        header_results = results.get("headers", [])

        # ===== 5. 生成报告 =====
        self.logger.info("Generating report")

        report = ReportGenerator()

        report.generate(
            sql_results,
            xss_results,
            dir_results,
            header_results
        )