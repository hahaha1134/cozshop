import pymongo

# 连接到 MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.cozshop

# 获取所有用户
users = db.users.find({})

print('现有用户:')
for user in users:
    print(f'邮箱: {user.get("email")}, 角色: {user.get("role")}, 状态: {user.get("status")}')

# 关闭连接
client.close()