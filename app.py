# -*- coding: utf-8 -*-
import base64

import ipfsapi
from flask import  render_template, redirect, url_for, request
from ipfs_model import hashid
from ipfs_model import db
from ipfs_model import app
import json
import os
app.config["SECRET_KEY"] = 12345678
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# print(app.config["SECRET_KEY"])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404



@app.route('/',methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        return render_template('index.html')



@app.route('/private.html',methods=['GET', 'POST'])
def getdata():
    if request.method == 'POST':
        try:
            api = ipfsapi.connect('129.211.27.244', 5001)
            text = request.form['hash_key']
            ifpub= request.form['public']
            with open('cont.txt', 'w') as f:
                b64 = base64.b64encode(text.encode('utf-8'))
                f.write(b64.decode())
            hash_key = api.add('cont.txt')['Hash']
            print(hash_key)
            with open('cont.txt', 'w') as f:
                f.write("")
            a = hashid( hash=hash_key,hashed='', is_public=int(ifpub))
            print(a)
            db.session.add(a)
            db.session.commit()
            return render_template('private.html', hash_key=hash_key)
        except:
            db.session.rollback()
            return render_template('404.html')
    return render_template('private.html')





@app.route('/check.html',methods=['GET', 'POST'])
def news():
    text=''
    if request.method == 'POST':
        try:
            api = ipfsapi.connect('129.211.27.244', 5001)
            hash_key = request.form["hash"]
            content = api.cat(hash_key).decode('gbk')
            text = content.encode(encoding='utf-8')
            text = base64.b64decode(text)
            print(text)
            text = text.decode()
            print(text)
        except:
            return render_template('404.html')
    return render_template('check.html', show=text)




@app.route('/forum.html/',methods=['GET'])
def index():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 9))
    # try:
    api =ipfsapi.connect('129.211.27.244', 5001)
    blogs = db.session.query(hashid).filter(hashid.hash != '', hashid.hashed == '', hashid.is_public == 1).order_by(
        hashid.createtime.desc()).paginate(page,per_page,error_out=False)
    stus=blogs.items
    for i in range(len(stus)):
        content = api.cat(stus[i].hash).decode('gbk')
        text = content.encode(encoding='utf-8')
        text = base64.b64decode(text)
        text = text.decode()
        if len(text)<10:
            pass
        else:
            text=text[:10]+'......'
        stus[i].hash=text
    return render_template('forum.html', paginate=blogs, stus=stus)
    # except:
    #     return render_template('404.html')




@app.route('/forum.html/？<id1>',methods=['GET', 'POST'])
def comment(id1):
    #变量id1是数据库相对应的键值
    # try:
    api = ipfsapi.connect('129.211.27.244', 5001)
    a=db.session.query(hashid).filter(hashid.id==id1).first()
    print(a.createtime)
    master = a.hash
    time=a.createtime
    content = api.cat(master).decode('gbk')
    text = content.encode(encoding='utf-8')
    text = base64.b64decode(text)
    text = text.decode()
    main = text
    reply=db.session.query(hashid).filter(hashid.hash != '', hashid.hashed == id1, hashid.is_public == 1).order_by(
        hashid.createtime.asc()).all()
    p=''
    for i in reply:
        content = api.cat(i.hash).decode('gbk')
        text = content.encode(encoding='utf-8')
        text = base64.b64decode(text)
        print(text)
        b = text.decode()
        print(text)
        c = str(i.createtime)
        p = p +'<br/>'+ c + '        ' + b + '<br/>'    #同样显示排版有问题
    if p=="":
        p='还没有人评论'
    #显示主贴和回复的话
    if request.method=='GET':
        return render_template('forum_content.html', main=main,posttime=time,reply=p)
    #下面是评论
    if request.method=='POST':
        target=id1
        com=request.form['what_user_wrote']
        with open('cont.txt', 'w') as f:
            b64 = base64.b64encode(com.encode('utf-8'))
            f.write(b64.decode('gbk'))
        hash_key = api.add('cont.txt')['Hash']
        a = hashid(hash=hash_key, hashed=target, is_public=1)
        db.session.add(a)
        db.session.commit()
        with open('cont.txt', 'w') as f:
            f.write("")
            #####更新评论
        reply = db.session.query(hashid).filter(hashid.hash != '', hashid.hashed == id1,
                                                hashid.is_public == 1).order_by(
            hashid.createtime.asc()).all()
        p = ''
        for i in reply:
            content = api.cat(i.hash).decode('gbk')
            text = content.encode(encoding='utf-8')
            text = base64.b64decode(text)
            print(text)
            b = text.decode()
            c = str(i.createtime)
            p = p + '<br/>' + c + '        ' + b + '<br/>'
            ######更新评论
        return render_template('forum_content.html', main=main, posttime=time, reply=p)
    # except:
    #     return render_template('404.html')


if __name__ == '__main__':
    app.run()
