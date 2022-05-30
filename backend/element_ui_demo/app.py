from flask import Flask, jsonify, request
from flask_cors import CORS

from database.ext import db
from database.orm import User

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDB.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/data?charset=utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# 允许所有
# CORS(app, resources=r'/*')
# 允许指定主机和端口
CORS(app, origins=['http://localhost:8080'])


@app.route('/findAll')
def find_all():
    data = []
    users = User.query.all()
    for user in users:
        user_dict = user.to_dict()
        user_dict["bir"] = datetime.strftime(user_dict["bir"], '%Y-%m-%d')
        data.append(user_dict)
    # print(data)
    return jsonify(data)

@app.route('/findByPage', methods=["GET"])
def find_by_page():
    page_num = int(request.args.get("pageNum", 1))
    page_size = int(request.args.get("pageSize", 4))
    data = []
    # 分页1
    # users = User.query.offset((page_num-1)*page_size).limit(page_size).all()
    # total = User.query.count()
    # 分页2
    pagination = User.query.paginate(page=page_num, per_page=page_size, error_out=False)
    users = pagination.items
    total = pagination.total
    for user in users:
        user_dict = user.to_dict()
        user_dict["bir"] = datetime.strftime(user_dict["bir"], '%Y-%m-%d')
        data.append(user_dict)
    # print(total, data)
    return jsonify({"data":data, "total":total})


@app.route('/saveOrUpdate', methods=["POST"])
def insert():
    id = request.json.get('id', None)
    name = request.json.get('name')
    sex = request.json.get('sex')
    bir = request.json.get('bir')
    address = request.json.get('address')
    if not id:
        # 创建
        u = User(
            name=name,
            sex=sex,
            bir=datetime.strptime(bir, '%Y-%m-%d'),
            address=address
        )
        try:
            db.session.add(u)
            db.session.commit()
            return jsonify({
                "status": True,
                "msg": "添加成功"
            })
        except Exception as e:
            return jsonify({
                "status": False,
                "msg": "添加失败"
            })
    else:
        # 更新
        user = User.query.get(id)
        user.name = name
        user.sex = sex
        user.bir = datetime.strptime(bir, '%Y-%m-%d')
        user.address = address
        try:
            db.session.commit()
            return jsonify({
                "status": True,
                "msg": "编辑成功"
            })
        except Exception as e:
            print(e)
            return jsonify({
                "status": False,
                "msg": "编辑失败"
            })


@app.route('/delete', methods=["POST"])
def delete():
    id = request.json.get('id')
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            "status": True,
            "msg": "删除成功"
        })
    return jsonify({
        "status": False,
        "msg": "用户不存在"
    })


@app.route('/create/db')
def create_db():
    db.create_all()
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
