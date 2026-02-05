import pymongo

# 连接到 MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.cozshop

# 查找所有使用 admin@cozshop.com 邮箱的用户
users = db.users.find({"email": "admin@cozshop.com"})

print('找到的重复用户:')
for user in users:
    print(f'ID: {user.get("_id")}, 角色: {user.get("role")}, 状态: {user.get("status")}')

# 重置游标
users = db.users.find({"email": "admin@cozshop.com"})

# 删除所有重复的用户，只保留一个
admin_user = None
for user in users:
    if user.get("role") == "admin":
        admin_user = user
    else:
        # 删除非管理员用户
        db.users.delete_one({"_id": user.get("_id")})
        print(f'已删除用户: {user.get("_id")}, 角色: {user.get("role")}')

# 如果找到了管理员用户，将其状态设置为 active
if admin_user:
    db.users.update_one(
        {"_id": admin_user.get("_id")},
        {"$set": {"status": "active"}}
    )
    print(f'已将管理员用户状态设置为 active: {admin_user.get("_id")}')
else:
    # 如果没有找到管理员用户，创建一个
    new_admin = {
        "name": "Admin User",
        "email": "admin@cozshop.com",
        "password": "admin123",  # 注意：实际应用中应该使用密码哈希
        "role": "admin",
        "status": "active",
        "created_at": pymongo.MongoClient().cozshop.users.find_one()["created_at"]
    }
    result = db.users.insert_one(new_admin)
    print(f'已创建新的管理员用户: {result.inserted_id}')

# 验证修复结果
users = db.users.find({"email": "admin@cozshop.com"})
print('修复后的用户:')
for user in users:
    print(f'ID: {user.get("_id")}, 角色: {user.get("role")}, 状态: {user.get("status")}')

# 关闭连接
client.close()