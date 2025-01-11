# XHM SDK 使用说明

# 封装sdk时请多考虑去解决一类问题、而不是一个问题

## 使用教程

安装单个模块：

    pip install xhm_all[xhm_log]

安装所有：

    pip install xhm_all

### 二、poetry

安装：

    poetry add xhm_all@0.1.7 --verbose

### 在代码中使用BOCHU SDK

    from xhm_log import log
    
    def test_case():
        log.error('cc')

### 更新并安装

    poetry add xhm_all==0.0.6

### 升级记录

| 版本    | 日期         | 更新记录          | 开发人员 |
|-------|------------|---------------|------|
| 0.0.6 | 2025-01-09 | 日志修复          | 邹慧刚  |
| 0.0.1 | 2024-12-08 | 拆分基础SDK和业务SDK | 邹慧刚  |

