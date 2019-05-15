# -*- coding: utf-8 -*-
import ipfsapi
from flask import Flask, render_template, session, redirect, url_for, request
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
# class NameForm(Form):
#     words = StringField('这是属于您的树洞，请说出任何您想说的话，不会有任何人知道您的真实身份', validators=[Required()])
#     submit = SubmitField('Submit')

@app.route('/shudong',methods=['GET', 'POST'])
def getdata():
    api = ipfsapi.connect('129.211.27.244', 5001)
    # form = NameForm()
    # hash_key = ''
    if request.method == 'POST':
        text = request.values['hash_key']
        if text == '':
            return render_template('ipfs.html', message='输入内容不能为空')
        else:
            hash_key = api.add('cont.txt')['Hash']
            with open('cont.txt', 'w') as f:
                f.write("")
            return render_template('ipfs.html',hash_key = hash_key)
    return render_template('ipfs.html')


@app.route('/news',methods=['GET', 'POST'])
def news():
    new = ''
    api = ipfsapi.connect('129.211.27.244', 5001)
    if request.method == 'POST':
        hash_key = request.form['hash_key']
        print(hash_key)
        new = api.cat(hash_key).decode('gbk')
        print(new)
    return render_template('news.html',new = new)

# @app.route('/',methods=['GET'])
# def index():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run()
