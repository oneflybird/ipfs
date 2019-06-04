# -*- coding: utf-8 -*-
import ipfsapi
import base64

# 查看文件内容
if __name__ == '__main__':
    api = ipfsapi.connect('129.211.27.244', 5001)
    with open('cont.txt', 'w') as f:
        b64 = base64.b64encode("你好，我的孩子".encode('utf-8'))
        print(b64.decode())
        f.write(b64.decode())
    # with open('cont.txt', 'r') as f:
    #     text=f.read()
    #     print(text)
    #     text = text.encode(encoding='utf-8')
    #     print(text)
    #     text = base64.b64decode(text)
    #     print(text)
    #     print(text.decode())
    hash_key = api.add('cont.txt')['Hash']
    # print(hash_key)
    content = api.cat(hash_key).decode('gbk')
    text = content.encode(encoding='utf-8')
    print(text)
    text = base64.b64decode(text)
    print(text)
    print(text.decode())
    # print(content)
    # print(content.decode())
    # print(base64.b64decode(content.encode('utf-8')))
# 下载文件
# res = api.get(res['Hash'])