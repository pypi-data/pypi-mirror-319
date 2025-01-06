import unittest
from unittest.mock import patch

from factory import SmsSenderFactory
from sender.aliyun_sender import AliyunSmsSender
from utils import generate_sms_code


class TestSmsSender(unittest.TestCase):
    @patch.object(AliyunSmsSender, 'send_sms', return_value={"status": "success"})
    def test_send_sms_success(self, mock_send_sms):
        # 创建工厂并生成 AliyunSmsSender 实例
        sender = SmsSenderFactory.create_sms_sender(
            provider="aliyun",
            access_key_id="test_id",
            access_key_secret="test_secret",
            sign_name="test_sign",
        )
        print(sender)
        # 测试发送短信
        # response = sender.send_sms("1234567890", 'verification', generate_sms_code())