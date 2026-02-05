import pymongo

# 连接到 MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.cozshop

# 更新管理员用户状态
result = db.users.update_one(
    {"email": "admin@cozshop.com"},
    {"$set": {"status": "active"}}
)

print(f'更新结果: {result.modified_count} 个文档被更新')

# 验证更新结果
user = db.users.find_one({"email": "admin@cozshop.com"})
print(f'管理员用户现在的状态: {user.get("status