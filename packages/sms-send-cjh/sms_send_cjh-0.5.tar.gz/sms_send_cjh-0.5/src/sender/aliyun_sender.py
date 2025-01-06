import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

from src.sender.base import BaseSmsSender


class AliyunSmsSender(BaseSmsSender):
    def __init__(self, access_key_id, access_key_secret, sign_name):
        self.client = AcsClient(access_key_id, access_key_secret)
        self.sign_name = sign_name

    def send_sms(self, phone_number, template_code, code):
        """
        发送短信验证码
        :param phone_number: 手机号
        :param template_code: 模板标识符
        :param code: 验证码
        :return: 发送结果
        """
        template_param = json.dumps({
            'code': code,
        })

        # 构造发送请求
        request = SendSmsRequest()
        request.set_TemplateCode(template_code)  # 模板ID
        request.set_SignName(self.sign_name)  # 签名
        request.set_PhoneNumbers(phone_number)  # 手机号
        request.set_TemplateParam(template_param)  # 模板参数
        try:
            response = self.client.do_action_with_exception(request)
            return response.decode('utf-8')
        except Exception as e:
            return str(e)
