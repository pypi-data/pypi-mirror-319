from flask import Flask, render_template
from flask_wechat_share import WeChatShare

app = Flask(__name__)

app.config["SECRET_KEY"] = 'hello'
app.config["WECHAT_APP_ID"] = '<app_id>'
app.config["WECHAT_APP_SECRET"] = '<app_secret>'

weixin = WeChatShare(app)


@app.route('/')
def index():
    return render_template('share.html')
