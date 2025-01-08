"""
@author: Ethan
@contact: email:
@Created on: 2025/1/1 11:49
@Remark:
"""
from application import settings

# ================================================= #
# ***************** 插件配置区开始 *******************
# ================================================= #
# 路由配置
plugins_url_patterns = [
    {"re_path": r'api/lelu_admin_test/', "include": "lelu_admin_test.urls"}
]
# app 配置
apps = ['lelu_admin_test']
