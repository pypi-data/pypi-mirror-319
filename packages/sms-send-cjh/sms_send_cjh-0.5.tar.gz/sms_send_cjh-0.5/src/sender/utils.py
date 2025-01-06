import random


def generate_sms_code():
    """
    生成一个 6 位随机验证码
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])
