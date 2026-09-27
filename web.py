"""
PythonAnywhere 后端参考实现：登录 / 注册发码 / 验证码校验。
部署到 yanghuangluo.pythonanywhere.com 后，前端 github.io 即可调用。
注意：
1. 需在 PythonAnywhere 的 Web 标签页开启静态文件并配置 WSGI。
2. 需 pip install flask flask-cors。
3. 邮箱密码请填到环境变量 MAIL_PASSWORD（不要硬编码）。
4. 这里用内存 dict 存用户和验证码，重启会丢；正式使用请换数据库。
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, random, smtplib
from email.mime.text import MIMEText

web = Flask(__name__)
CORS(web)  # 允许 github.io 跨域访问

# 内存存储（开发用）
users = {}            # UserName -> {PassWord, UserEmail, verified}
pending_codes = {}    # UserEmail -> code

SMTP_HOST = "smtp.qq.com"          # 按你的邮箱服务商改，QQ/163/Gmail 不同
SMTP_PORT = 465
MAIL_USER = os.environ.get("MAIL_USER", "your_email@qq.com")
MAIL_PASS = os.environ.get("MAIL_PASSWORD", "")


def send_email(to_addr, code):
    msg = MIMEText(f"【注册验证码】您的验证码是：{code}，5 分钟内有效。", "plain", "utf-8")
    msg["Subject"] = "注册验证码"
    msg["From"] = MAIL_USER
    msg["To"] = to_addr
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as s:
        s.login(MAIL_USER, MAIL_PASS)
        s.sendmail(MAIL_USER, [to_addr], msg.as_string())


@web.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    uname = data.get("UserName", "")
    pwd = data.get("PassWord", "")
    u = users.get(uname)
    if u and u["PassWord"] == pwd and u.get("verified"):
        return jsonify(msg=f"欢迎 {uname}", user=uname)
    return jsonify(msg="用户名或密码错误，或邮箱未验证"), 401


@web.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True)
    uname = data.get("UserName", "")
    pwd = data.get("PassWord", "")
    email = data.get("UserEmail", "")
    if not uname or not pwd or not email:
        return jsonify(msg="参数不全"), 400
    if uname in users and users[uname].get("verified"):
        return jsonify(msg="用户名已被注册"), 409

    code = f"{random.randint(0, 999999):06d}"
    pending_codes[email] = code
    users[uname] = {"PassWord": pwd, "UserEmail": email, "verified": False}

    try:
        send_email(email, code)
    except Exception as e:
        # 邮件发送失败时，dev 模式仍把 code 返回给前端，方便调试
        return jsonify(msg=f"邮件发送失败：{e}", code=code), 200

    # 按需求：同时把验证码返回给 github.io 页面（dev 调试用）
    return jsonify(msg="验证码已发送", code=code)


@web.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(force=True)
    uname = data.get("UserName", "")
    email = data.get("UserEmail", "")
    code = data.get("Code", "")
    if pending_codes.get(email) == code:
        users[uname]["verified"] = True
        pending_codes.pop(email, None)
        return jsonify(msg="注册成功")
    return jsonify(msg="验证码错误"), 400


@web.route("/")
def index():
    return "Render部署成功！"


if __name__ == "__main__":
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
