# -*- coding: utf-8 -*-
import ipfsapi
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from ipfs_model import hashid
from ipfs_model import db
from ipfs_model import app
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form
import uuid
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
        text = request.form['hash_key']
        ifpub= request.form['public']
        if text == '':
            return render_template('ipfs.html', message='输入内容不能为空')
        else:
            with open('cont.txt', 'w') as f:
                f.write(text)
            hash_key = api.add('cont.txt')['Hash']
            with open('cont.txt', 'w') as f:
                f.write("")
            a = hashid( hash=hash_key,hashed='', is_public=int(ifpub))
            db.session.add(a)
            db.session.commit()

            return render_template('ipfs.html',hash_key =hash_key)
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



@app.route('/public',methods=['GET', 'POST'])
def index():
    api =ipfsapi.connect('129.211.27.244', 5001)
    a = db.session.query(hashid).filter(hashid.hash != '', hashid.hashed == '', hashid.is_public == 1).order_by(
        hashid.createtime.desc()).all()
    p = ''
    for i in a:
        b = api.cat(i.hash).decode('gbk')
        c = str(i.createtime)
        p = p + '<br/>' + c + '        ' + b + '<br/>'
    return render_template('public.html',message = p)



@app.route('/public/<hash1>',methods=['GET', 'POST'])
def comment(hash1):                                      #变量hash是帖主说的话的哈希值
    api = ipfsapi.connect('129.211.27.244', 5001)
    #显示主贴和回复的话
    master = hash1
    main=api.cat(master).decode('gbk')
    reply=db.session.query(hashid).filter(hashid.hash != '', hashid.hashed == master, hashid.is_public == 1).order_by(
        hashid.createtime.desc()).all()
    p=''
    for i in reply:
        b = api.cat(i.hash).decode('gbk')
        c = str(i.createtime)
        p = p + '<br/>' + c + '        ' + b + '<br/>'
    if request.method=='GET':
        return render_template('comment.html', main=main,reply=p)
    #下面是评论
    if request.method=='POST':
        target=master
        com=request.form['demo']

        if com=='':
            return render_template('comment.html', message='评论不能为空')
        else:
            with open('cont.txt', 'w') as f:
                f.write(com)
            hash_key = api.add('cont.txt')['Hash']
            a = hashid(hash=hash_key, hashed=target, is_public=1)
            db.session.add(a)
            db.session.commit()
            with open('cont.txt', 'w') as f:
                f.write("")
        return render_template('comment.html', hash_key=hash_key,main=main,reply=p)
    return render_template('comment.html')

# @app.route('/',methods=['GET'])
# def index():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run()