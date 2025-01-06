from src.sender.aliyun_sender import AliyunSmsSender


class SmsSenderFactory:
    @staticmethod
    def create_sms_sender(provider, access_key_id, access_key_secret, sign_name):
        if provider == 'aliyun':
            return AliyunSmsSender(access_key_id, access_key_secret, sign_name)
        else:
            raise ValueError("Unsupported SMS provider")
