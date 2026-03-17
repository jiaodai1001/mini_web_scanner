import importlib
import os


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

    def run_plugins(self, target, urls):

        results = {}

        for plugin in self.plugins:

            print(f"[PluginManager] Executing {plugin.name}")

            output = plugin.run(target, urls)

            results[output["type"]] = output["results"]

        return results