import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://yanghuangluo.github.io'])

USER_FILE = "/home/yanghuangluo/user_name.txt"


@app.post("/signup")
def signup():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"code": 400, "msg": "请求体非json"}), 400

    username = data.get("UserName") or ""
    password = data.get("UserPassword") or ""
    useremail = data.get("UserEmail") or ""

    if not username or not password or not useremail:
        return jsonify({"code": 400, "msg": "用户名/密码/邮箱不能为空"}), 400

    # 简单防重名
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts and parts[0] == username:
                    return jsonify({"code": 400, "msg": "用户名已存在"}), 400

    with open(USER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{password},{useremail}\n")

    return jsonify({"code": 200, "msg": "注册成功"}), 200


@app.post("/login")
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"code": 400, "msg": "请求体非json"}), 400

    username = data.get("UserName") or ""
    password = data.get("UserPassword") or ""

    if not os.path.exists(USER_FILE):
        return jsonify({"code": 400, "msg": "没有此用户名"}), 400

    found_user = False
    found_pwd = False
    with open(USER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            if parts[0] == username:
                found_user = True
                if parts[1] == password:
                    found_pwd = True
                break

    if not found_user:
        return jsonify({"code": 400, "msg": "没有此用户名"}), 400
    if not found_pwd:
        return jsonify({"code": 400, "msg": "密码错误"}), 400

    return jsonify({"code": 200, "msg": "登录成功"}), 200


@app.post("/")
def hellouser():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"code": 400, "msg": "请求体非json"}), 400
    return jsonify(data), 200
