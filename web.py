from flask import Flask
import os
web = Flask(__name__)

@web.route('/')
def index():
    return "Render部署成功！"

if __name__ == '__main__':
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
