# Config for Python

## 1. Introduction
Parse config from json file

## 2. Usage

### 2.1 Basic

* config.json
```json
{
  "a": 1,
  "b": 2
}
```
* python file
```python
from cuspy import ConfigUtils

config = ConfigUtils("config.json")
a = config.aaa_config.a
b = config.aaa_config.b
```

### 2.2 File/Directory Path

* config.json
```json
{
  "aaa_config": {
    "root": "/home/aaa",
    "data_dn": "data_dir",
    "data_fp": "data.tsv"
  }
}
```

* python file
```python
from cuspy import ConfigUtils

config = ConfigUtils("config.json")

data_dp = config.aaa_config.data_dp
# data_dp = "/home/aaa/data_dir"

data_fp = config.aaa_config.data_fp
# data_fp = "/home/aaa/data_dir/data.tsv"
```

