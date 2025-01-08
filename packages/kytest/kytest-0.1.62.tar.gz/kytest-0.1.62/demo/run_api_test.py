"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from data.login_data import get_headers


if __name__ == '__main__':
    kytest.main(
        host='https://app-test.qizhidao.com/',  # 域名，针对接口和web测试
        headers=get_headers(),  # 请求头信息，针对接口测试
        path="tests/test_api.py",  # 测试脚本目录
        # xdist=True  # 并发执行，针对接口和web测试tests/Product_Detail_Controller
    )

