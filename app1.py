#app1.py
from flask import Flask, render_template, request
from mark1 import fun_1
from cloud3 import cloud_model3
from markupsafe import Markup
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
import os

app = Flask(__name__, static_url_path='/static')

# 设置代理环境变量
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890" # os.environ["http_proxy"] = "http://<代理ip>:<代理端口>"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890" # os.environ["https_proxy"] = "http://<代理ip>:<代理端口>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST','GET'])
def get_response():
    user_input = request.form['user_input']
    if user_input == "bye":
        return "Goodbye!"
    print(user_input)

    # Step 1: 敏感信息屏蔽
    masked_text = fun_1(user_input)
    print(masked_text)

    # Step 2: 与云端模型对话
    cloud_response = cloud_model3(masked_text)
    print(cloud_response)

    # 将云端模型回答转换为Markdown格式
    return Markup(markdown.markdown(cloud_response, extensions=['fenced_code', 'codehilite']))



if __name__ == '__main__':
    app.run(debug=True)