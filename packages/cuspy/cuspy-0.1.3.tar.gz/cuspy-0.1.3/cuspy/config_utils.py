#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 18:19
# @Author  : zbc@mail.ustc.edu.cn
# @File    : config.py
# @Software: PyCharm
import os
import re
from typing import Dict
import json
from types import SimpleNamespace


class ConfigUtils:

    @staticmethod
    def mkdir(dp: str):
        if not os.path.exists(dp):
            os.mkdir(dp)
        return dp

    @classmethod
    def _set_path(cls, config_json: Dict) -> Dict:
        old_keys = list(config_json.keys())
        if 'root' in config_json.keys():
            root = config_json.get('root')
            mkdir_auto = config_json.get('mkdir_auto')
            mkdir_auto = False if mkdir_auto is None else mkdir_auto
            for key in old_keys:
                value = config_json[key]
                if key.endswith('_fn') or key.endswith('_dn'):
                    fp_key = key[:-1] + 'p'
                    config_json[fp_key] = os.path.join(root, value)
                    # config_json.pop(key)
                    if mkdir_auto and key.endswith('_dn') and not key.startswith('v.'):
                        cls.mkdir(config_json[fp_key])
                elif key.endswith('_file_name') or key.endswith('_dir_name'):
                    fp_key = key[:-4] + 'path'
                    config_json[fp_key] = os.path.join(root, value)
                    # config_json.pop(key)
                    if mkdir_auto and key.endswith('_dir_name') and not key.startswith('v.'):
                        cls.mkdir(config_json[fp_key])
            return config_json
        else:
            return config_json

    @classmethod
    def _set_path_iter(cls, config_json: Dict) -> Dict:
        for key, value in config_json.items():
            if key.endswith('_config'):
                config_json[key] = cls._set_path(value)
        return config_json

    @classmethod
    def _parse_abs_config(cls, config_json: Dict) -> Dict:
        basic_keys = []
        old_keys = list(config_json.keys())
        for key in old_keys:
            if ':' in key:
                real_key, extend_key = key.split(':')
                real_key = real_key.strip()
                extend_key = extend_key.strip()
                if extend_key not in config_json.keys():
                    raise ValueError(f"Expect '{extend_key}' by '{key}', but not founded")
                basic_keys.append(extend_key)
                extend_json = config_json[extend_key]
                real_value = {}
                for k, v in config_json[key].items():
                    real_value[k] = v
                for ek, ev in extend_json.items():
                    if ek not in real_value.keys():
                        real_value[ek] = ev
                config_json[real_key] = real_value
                config_json.pop(key)
        for bk in basic_keys:
            if bk in config_json.keys():
                config_json.pop(bk)
        return config_json

    @classmethod
    def _parse_variable_config(cls, config_json: Dict) -> Dict:
        old_keys = list(config_json.keys())
        for key in old_keys:
            value = config_json[key]
            if key.startswith('v.') and '{' in value and '}' in value:
                for v in re.findall(r'{(.+?)}', value):
                    if v not in config_json.keys():
                        raise ValueError(f"Expect '{v}' by '{key}', but not founded")
                    value = value.replace(f'{{{v}}}', str(config_json[v]))
                config_json[key[2:]] = value
        return config_json

    @classmethod
    def _parse_variable_iter(cls, config_json: Dict) -> Dict:
        for key, value in config_json.items():
            if key.endswith('_config'):
                config_json[key] = cls._parse_variable_config(value)
        return config_json

    @classmethod
    def load_config(cls, confi_fp: str):
        with open(confi_fp, 'r', encoding='utf-8')as f:
            config_json = json.load(f)
        config_json = cls._parse_abs_config(config_json)
        config_json = cls._parse_variable_config(config_json)
        config_json = cls._parse_variable_iter(config_json)

        config_json = cls._set_path(config_json)
        config_json = cls._set_path_iter(config_json)
        res = json.loads(json.dumps(config_json), object_hook=lambda d: SimpleNamespace(**d))
        return res


if __name__ == "__main__":
    pass
