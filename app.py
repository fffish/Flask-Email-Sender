from flask import Flask, request, jsonify
import yagmail
import configparser
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# 请求跟踪字典
request_counts = {}
window_size = timedelta(minutes=1)  # 时间窗口设置为1分钟

# 检查配置文件是否存在
config_file = '.config'
if not os.path.isfile(config_file):
    print("配置文件不存在，请确认配置文件已放置在正确路径！")
    exit()

config = configparser.ConfigParser()

# 尝试读取配置文件
try:
    config.read(config_file)
    # 检查必需的配置项
    email_sender = config['EMAIL']['EMAIL_SENDER']
    email_password = config['EMAIL']['EMAIL_PASSWORD']
    smtp_server = config['EMAIL']['SMTP_SERVER']
    smtp_port = config['EMAIL']['SMTP_PORT']
    api_keys = config['API']['API_KEYS'].split(',')
    api_key_limit = int(config['API']['API_KEY_LIMIT'])
except KeyError as e:
    print(f"缺少必要的配置项: {e}")
    exit()
except Exception as e:
    print(f"读取配置文件时出现错误: {e}")
    exit()


def verify_api_key(key):
    """验证API密钥并记录请求次数"""
    current_time = datetime.now()
    if key in api_keys:
        # 检查密钥是否超过频率限制
        if key in request_counts:
            timestamps, count = request_counts[key]
            if current_time - timestamps > window_size:
                request_counts[key] = (current_time, 1)  # 重置计数和时间
            else:
                if count >= api_key_limit:
                    return False  # 请求次数过多
                request_counts[key] = (timestamps, count + 1)  # 更新计数
        else:
            request_counts[key] = (current_time, 1)  # 初始化计数
        return True
    return False


# 发送邮件的接口
@app.route('/email/send', methods=['POST'])
def send_email():
    api_key = request.headers.get('Authorization')
    if not verify_api_key(api_key):
        return jsonify({"code": 429, "msg": "请求次数过多或无效的API密钥"}), 429

    # 解析请求数据
    addr = request.form.get('addr')
    title = request.form.get('title')
    content = request.form.get('content')

    # 检查参数完整性
    if not all([addr, title, content]):
        return jsonify({"code": 1, "msg": "参数错误"}), 400

    try:
        # SMTP服务器设置
        yag = yagmail.SMTP(
            user=email_sender,
            password=email_password,
            host=smtp_server,  # SMTP 服务器地址
            port=smtp_port,  # SSL 端口号
            smtp_starttls=False,  # 禁用 STARTTLS，因为我们使用 SSL
            smtp_ssl=True  # 使用 SSL 连接
        )

        # 发送邮件
        yag.send(to=addr, subject=title, contents=content)
        yag.close()

    except Exception as e:
        # 捕获所有异常并返回失败信息
        return jsonify({"code": 2, "msg": f"邮件发送失败: {str(e)}"}), 500

    return jsonify({"code": 0, "msg": "Email sent successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
