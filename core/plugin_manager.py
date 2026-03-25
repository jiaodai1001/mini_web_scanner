import importlib
import os


# 插件执行阶段的进度区间：35% ~ 90%，按插件数量均分
_PLUGIN_PROGRESS_START = 35
_PLUGIN_PROGRESS_END = 90


class PluginManager:

    def __init__(self):

        self.plugins = []

    def load_plugins(self):

        plugin_folder = "plugins"

        for file in os.listdir(plugin_folder):

            if file.endswith("_plugin.py"):

                module_name = file[:-3]

                module = importlib.import_module(f"plugins.{module_name}")

                for attr in dir(module):

                    obj = getattr(module, attr)

                    try:

                        if hasattr(obj, "run") and hasattr(obj, "name"):

                            # 跳过基类
                            if obj.__name__ == "BasePlugin":
                                continue

                            # 确保是类（而不是函数/变量）
                            if isinstance(obj, type):
                                plugin = obj()
                                self.plugins.append(plugin)

                    except:
                        pass

    def run_plugins(self, target, urls, progress_callback=None):
        """
        执行所有插件。

        progress_callback(stage, message, percent) 可选；
        若未提供，行为与原版完全相同。
        """

        _progress = progress_callback or (lambda stage, msg, pct: None)

        results = {}
        total = len(self.plugins)

        for index, plugin in enumerate(self.plugins):

            # 计算本插件开始时的进度百分比
            if total > 0:
                percent = int(
                    _PLUGIN_PROGRESS_START
                    + (index / total) * (_PLUGIN_PROGRESS_END - _PLUGIN_PROGRESS_START)
                )
            else:
                percent = _PLUGIN_PROGRESS_START

            _progress(
                "scan",
                f"Running {plugin.name}... ({index + 1}/{total})",
                percent
            )

            print(f"[PluginManager] Executing {plugin.name}")

            output = plugin.run(target, urls)

            results[output["type"]] = output["results"]

            # 插件完成后更新进度
            percent_done = int(
                _PLUGIN_PROGRESS_START
                + ((index + 1) / total) * (_PLUGIN_PROGRESS_END - _PLUGIN_PROGRESS_START)
            )
            found = len(output["results"])
            _progress(
                "scan",
                f"{plugin.name} done — {found} issue(s) found",
                percent_done
            )

        return results
