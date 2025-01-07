from dailycheckin_liang import CheckIn
import os
import json

from dailycheckin_liang.configs import get_notice_info
from dailycheckin_liang.utils.message import push_message


class TestNotice(CheckIn):
    name = "通知测试"

    def __init__(self, check_item):
        self.check_item = check_item

    def main(self):
        content_list = [f"测试内容{self.check_item}"]
        notice_info = get_notice_info(data=datas)
        push_message(content_list=content_list, notice_info=notice_info)


if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"),
        encoding="utf-8",
    ) as f:
        datas = json.loads(f.read())
    _check_item = 'Hello World'
    print(TestNotice(check_item=_check_item).main())