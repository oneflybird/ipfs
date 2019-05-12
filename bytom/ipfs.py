import ipfsapi

# 连接IPFS，需要先启动节点服务器daemon
# api = ipfsapi.connect('129.211.27.244', 5001)

# 查看节点ID
# print(api.id())
# res = api.add('test.txt')

# 查看文件内容
if __name__ == '__main__':
    api = ipfsapi.connect('129.211.27.244', 5001)
    # res = api.add('test.txt')
    content = api.cat('QmPFDCuavg58zyQVdDHVgUqos2CVSmDTLa1cRZESK8qARZ')
    print(content)
    print(content.decode('gbk'))
# 下载文件
# res = api.get(res['Hash'])