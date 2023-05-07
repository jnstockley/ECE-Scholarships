"""
Utilities for managing the config
"""
import json
import os
from scholarship_app.utils.output import get_appdata_path


class ConfigManager:
    """
    Manages application config
    """

    def __init__(self):
        """
        Configures config
        """
        self.config_path = os.path.join(get_appdata_path(), "config.json")
        self.data = {}
        self.__load()

    def has_key(self, key: str):
        """
        Check if value exists in dict
        """
        return key in self.data

    def set_value(self, key: str, value: any):
        """
        Sets a value and saves config
        """
        self.data[key] = value
        self.__save()

    def __save(self):
        with open(self.config_path, "w", encoding="utf-8") as outfile:
            json.dump(self.data, outfile)

    def __load(self):
        """
        Updates data with content found in config.json
        """
        try:
            with open(self.config_path, encoding="utf-8") as config_file:
                self.data = json.load(config_file)
        except:
            # Failed loading file
            self.data = {}
            self.__save()
