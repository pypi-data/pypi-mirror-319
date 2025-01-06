from abc import ABC, abstractmethod


class BaseSmsSender(ABC):
    @abstractmethod
    def send_sms(self, phone_number, template_code, template_param):
        """发送短信，子类必须实现"""
        pass
