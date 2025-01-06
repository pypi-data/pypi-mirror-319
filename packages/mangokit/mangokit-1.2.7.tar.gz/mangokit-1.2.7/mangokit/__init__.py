# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-07 22:15
# @Author : 毛鹏
import sys

python_version = sys.version_info

if python_version.major != 3 and python_version.minor != 10:
    raise Exception("Python 3.10 is required.")

from mangokit.mango import Mango
from mangokit.tools.base_request import *
from mangokit.tools.log_collector import set_log
from mangokit.tools.data_processor import *
from mangokit.tools.database import *
from mangokit.models.models import *
from mangokit.tools.decorator import *
from mangokit.tools.notice import *
from mangokit.enums.enums import *
from mangokit.exceptions import MangoKitError

__all__ = [
    'DataProcessor',
    'DataClean',
    'ObtainRandomData',
    'CacheTool',
    'CodingTool',
    'EncryptionTool',
    'JsonTool',
    'RandomCharacterInfoData',
    'RandomNumberData',
    'RandomStringData',
    'RandomTimeData',

    'MysqlConingModel',
    'ResponseModel',
    'EmailNoticeModel',
    'TestReportModel',
    'WeChatNoticeModel',
    'FunctionModel',
    'ClassMethodModel',

    'CacheValueTypeEnum',
    'NoticeEnum',

    'MysqlConnect',
    'SQLiteConnect',
    'requests',
    'async_requests',
    'set_log',
    'WeChatSend',
    'EmailSend',

    'singleton',
    'convert_args',

    'Mango',

    'MangoKitError',
]
