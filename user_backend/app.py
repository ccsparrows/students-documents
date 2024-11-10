from flask import Flask, request, jsonify, render_template, redirect
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from extension import db, cors
from models import User, MoveInRecord, MoveOutRecord, AbsenceRecord, Building, Dormitory, Student
from flask.views import MethodView
from sqlalchemy import or_
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import logging
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

cors.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止追踪
db.init_app(app)


@app.cli.command()  # 定义一个自定义的 Flask 命令
def create():
    db.drop_all()
    db.create_all()
    User.init_db()
    Student.init_students()
    MoveInRecord.init_move_in_records()
    MoveOutRecord.init_move_out_records()
    AbsenceRecord.init_absence_records()
    Building.init_buildings()
    Dormitory.init_dormitories()
    logging.debug("Database had initialized ")


app.config['JSON_AS_ASCII'] = False

logging.basicConfig(level=logging.DEBUG)


def authenticate_user(username, password):
    logging.debug(f"Authenticating user: {username}")
    user = User.query.filter_by(username=username).first()
    if user:
        logging.debug(f"Found user: {user.username}")
        if user.password == password:
            logging.debug("Password match")
            return True
        else:
            logging.debug("Password mismatch")
    else:
        logging.debug("User not found")
    return False


@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if not username or not password:
        data = {
            "status": 400,
            "message": "未输入帐号密码！",
            "token": " "
        }
        return jsonify(data), 400

    if authenticate_user(username, password):
        token = create_access_token(identity=username)
        data = {
            "username": username,
            "password": password,
            "status": 200,
            "message": "Login successful",
            "token": token
        }
        return jsonify(data), 200
    else:
        data = {
            "status": 401,
            "message": "密码或账号错误！",
            "token": " "
        }
        return jsonify(data), 401


# @app.route('/students/', methods=['GET', 'POST'])
class StudentApi(MethodView):
    def get(self):
        students = Student.query.all()
        results = [
            {
                'id': student.id,
                'name': student.name,
                'sex': student.sex,
            } for student in students
        ]
        retres = {
            'status': 'success',
            'message': '数据查询成功',
            'result': results
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_student = Student(name=data['name'], sex=data['sex'])
        db.session.add(new_student)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '学生添加成功'
        })


class MoveInRecordApi(MethodView):
    def get(self):
        query = request.args.get('query', '', type=str)
        pagenum = request.args.get('pagenum', 1, type=int)
        pagesize = request.args.get('pagesize', 10, type=int)

        # 构建查询条件
        query_filters = [
            or_(
                MoveInRecord.student_name.like(f"%{query}%"),
                MoveInRecord.id.like(f"%{query}%")  # 假设学号字段名为 student_id
            )
        ]

        # 查询数据库
        records_query = MoveInRecord.query.filter(*query_filters)

        # 计算分页
        total = records_query.count()
        logging.debug(f"Received login data: {total}")
        records = records_query.offset((pagenum - 1) * pagesize).limit(pagesize).all()

        results = [
            {
                'id': record.id,
                'student_name': record.student_name,
                'move_in_time': record.move_in_time.strftime('%Y-%m-%d'),
                'build_number': record.build_number,
                'room_number': record.room_number,
            } for record in records
        ]
        retres = {
            # 'state': 'success',
            'message': '数据查询成功',
            'result': results,
            'total': total,  # 返回总记录数
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_record = MoveInRecord(
            student_name=data['student_name'],
            move_in_time=datetime.datetime.strptime(data['move_in_time'], '%Y-%m-%d'),
            build_number=data['build_number'],
            room_number=data['room_number']
        )
        db.session.add(new_record)
        db.session.commit()

        retres = {
            # 'status': 'success',
            'message': '入住记录添加成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def delete(self):
        data = request.get_json()
        record_id = data.get('id')
        record = MoveInRecord.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'message': '数据删除成功'}, 200
        return {'status': 'error', 'message': '记录未找到'}, 404

    def put(self):
        data = request.get_json()
        record_id = data.get('id')
        record = MoveInRecord.query.get(record_id)

        if not record:
            return {'status': 'error', 'message': '记录未找到'}, 404

        # 更新记录字段
        if 'student_name' in data:
            record.student_name = data['student_name']
        if 'move_in_time' in data:
            record.move_in_time = datetime.datetime.strptime(data['move_in_time'], '%Y-%m-%d')
        if 'build_number' in data:
            record.build_number = data['build_number']
        if 'room_number' in data:
            record.room_number = data['room_number']

        db.session.commit()

        retres = {
            'message': '入住记录更新成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200


class MoveOutRecordApi(MethodView):
    def get(self):
        query = request.args.get('query', '', type=str)
        pagenum = request.args.get('pagenum', 1, type=int)
        pagesize = request.args.get('pagesize', 10, type=int)

        # 构建查询条件
        query_filters = [
            or_(
                MoveOutRecord.student_name.like(f"%{query}%"),
                MoveOutRecord.id.like(f"%{query}%")  # 假设学号字段名为 student_id
            )
        ]

        # 查询数据库
        records_query = MoveOutRecord.query.filter(*query_filters)

        # 计算分页
        total = records_query.count()
        records = records_query.offset((pagenum - 1) * pagesize).limit(pagesize).all()
        results = [
            {
                'id': record.id,
                'student_name': record.student_name,
                'move_out_time': record.move_out_time.strftime('%Y-%m-%d'),
                'reason': record.reason
            } for record in records
        ]
        retres = {
            # 'status': 'success',
            'message': '数据查询成功',
            'result': results,
            'total': total,  # 返回总记录数
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_record = MoveOutRecord(
            id=data['id'],
            student_name=data['student_name'],
            move_out_time=datetime.datetime.strptime(data['move_out_time'], '%Y-%m-%d'),
            reason=data['reason']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '迁出记录添加成功'
        })

    def delete(self):
        data = request.get_json()
        record_id = data.get('id')
        record = MoveOutRecord.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'message': '迁出记录删除成功'}
        return {'status': 'fail', 'message': '迁出记录未找到'}, 404

    def put(self):
        data = request.get_json()
        record_id = data.get('id')
        record = MoveOutRecord.query.get(record_id)

        if not record:
            return {'status': 'error', 'message': '记录未找到'}, 404

        # 更新记录字段
        if 'student_name' in data:
            record.student_name = data['student_name']
        if 'move_out_time' in data:
            record.move_out_time = datetime.datetime.strptime(data['move_out_time'], '%Y-%m-%d')
        if 'reason' in data:
            record.reason = data['reason']

        db.session.commit()

        retres = {
            'message': '离校记录更新成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200


class AbsenceRecordApi(MethodView):
    def get(self):
        query = request.args.get('query', '', type=str)
        pagenum = request.args.get('pagenum', 1, type=int)
        pagesize = request.args.get('pagesize', 10, type=int)

        # 构建查询条件
        query_filters = [
            or_(
                AbsenceRecord.student_name.like(f"%{query}%"),
                AbsenceRecord.id.like(f"%{query}%")  # 假设学号字段名为 student_id
            )
        ]

        # 查询数据库
        records_query = AbsenceRecord.query.filter(*query_filters)

        # 计算分页
        total = records_query.count()
        records = records_query.offset((pagenum - 1) * pagesize).limit(pagesize).all()

        results = [
            {
                'id': record.id,
                'student_name': record.student_name,
                'absence_time': record.absence_time.strftime('%Y-%m-%d'),
                'reason': record.reason,
            } for record in records
        ]
        retres = {
            # 'status': 'success',
            'message': '数据查询成功',
            'result': results,
            'total': total,  # 返回总记录数
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_record = AbsenceRecord(
            student_name=data['student_name'],
            absence_time=datetime.datetime.strptime(data['absence_time'], '%Y-%m-%d'),
            reason=data['reason']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '缺寝记录添加成功'
        })

    def delete(self):
        data = request.get_json()
        record_id = data.get('id')
        record = AbsenceRecord.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'message': '缺寝记录删除成功'}
        return {'status': 'fail', 'message': '缺寝记录未找到'}, 404

    def put(self):
        data = request.get_json()
        record_id = data.get('id')
        record = AbsenceRecord.query.get(record_id)

        if not record:
            return {'status': 'error', 'message': '记录未找到'}, 404

        # 更新记录字段
        if 'student_name' in data:
            record.student_name = data['student_name']
        if 'absence_time' in data:
            record.absence_time = datetime.datetime.strptime(data['absence_time'], '%Y-%m-%d')
        if 'reason' in data:
            record.reason = data['reason']

        db.session.commit()

        retres = {
            'message': '缺勤记录更新成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200


class BuildingApi(MethodView):
    def get(self):
        query = request.args.get('query', '', type=str)
        pagenum = request.args.get('pagenum', 1, type=int)
        pagesize = request.args.get('pagesize', 10, type=int)

        # 构建查询条件
        query_filters = [
            or_(
                Building.address.like(f"%{query}%"),
                Building.number.like(f"%{query}%")  # 假设学号字段名为 student_id
            )
        ]

        # 查询数据库
        records_query = Building.query.filter(*query_filters)

        # 计算分页
        total = records_query.count()
        records = records_query.offset((pagenum - 1) * pagesize).limit(pagesize).all()
        results = [
            {
                'id': building.id,
                'number': building.number,
                'address': building.address,
                'dorm_manager_id': building.dorm_manager_id,
                'dorm_manager': building.dorm_manager,
            } for building in records
        ]
        retres = {
            # 'status': 'success',
            'message': '数据查询成功',
            'result': results,
            'total': total,  # 返回总记录数
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_building = Building(
            number=data['number'],
            address=data['address'],
            dorm_manager_id=data['dorm_manager_id'],
            dorm_manager=data['dorm_manager']
        )
        db.session.add(new_building)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '楼层记录添加成功'
        })

    def delete(self):
        data = request.get_json()
        record_id = data.get('id')
        record = Building.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'message': '楼层删除成功'}
        return {'status': 'fail', 'message': '楼层未找到'}, 404

    def put(self):
        data = request.get_json()
        building_id = data.get('id')
        building = Building.query.get(building_id)

        if not building:
            return {'status': 'error', 'message': '楼层记录未找到'}, 404

        # 更新记录字段
        if 'number' in data:
            building.number = data['number']
        if 'address' in data:
            building.address = data['address']
        if 'dorm_manager_id' in data:
            building.dorm_manager_id = data['dorm_manager_id']
        if 'dorm_manager' in data:
            building.dorm_manager = data['dorm_manager']

        db.session.commit()

        retres = {
            'message': '楼层记录更新成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200


class DormitoryApi(MethodView):
    def get(self):
        query = request.args.get('query', '', type=str)
        pagenum = request.args.get('pagenum', 1, type=int)
        pagesize = request.args.get('pagesize', 10, type=int)

        # 构建查询条件
        query_filters = [
            or_(
                Dormitory.build_address.like(f"%{query}%"),
                Dormitory.room_number.like(f"%{query}%")  # 假设学号字段名为 student_id
            )
        ]

        # 查询数据库
        records_query = Dormitory.query.filter(*query_filters)

        # 计算分页
        total = records_query.count()
        records = records_query.offset((pagenum - 1) * pagesize).limit(pagesize).all()

        logging.debug(f"Received login data: {query}")
        results = [
            {
                'id': dormitory.id,
                'build_address': dormitory.build_address,
                'room_number': dormitory.room_number,
                'capacity': dormitory.capacity,
                'current_occupancy': dormitory.current_occupancy,
            } for dormitory in records
        ]
        retres = {
            # 'status': 'success',
            'message': '数据查询成功',
            'result': results,
            'total': total,  # 返回总记录数
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200

    def post(self):
        data = request.get_json()
        new_dormitory = Dormitory(
            build_number=data['build_number'],
            room_number=data['room_number'],
            capacity=data['capacity'],
            current_occupancy=data['current_occupancy']
        )
        db.session.add(new_dormitory)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '宿舍记录添加成功'
        })

    def delete(self):
        data = request.get_json()
        record_id = data.get('id')
        record = Dormitory.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'message': '宿舍删除成功'}
        return {'status': 'fail', 'message': '宿舍未找到'}, 404

    def put(self):
        data = request.get_json()
        dormitory_id = data.get('id')
        dormitory = Dormitory.query.get(dormitory_id)

        if not dormitory:
            return {'status': 'error', 'message': '宿舍记录未找到'}, 404

        # 更新记录字段
        if 'build_address' in data:
            dormitory.build_address = data['build_address']
        if 'room_number' in data:
            dormitory.room_number = data['room_number']
        if 'capacity' in data:
            dormitory.capacity = data['capacity']
        if 'current_occupancy' in data:
            dormitory.current_occupancy = data['current_occupancy']

        db.session.commit()

        retres = {
            'message': '宿舍记录更新成功',
            'status': 200
        }

        logging.debug(f"Received login data: {retres}")
        return jsonify(retres), 200


# 管理视图
student_view = StudentApi.as_view('student_api')
app.add_url_rule('/students/', view_func=student_view, methods=['GET', 'POST'])
app.add_url_rule('/move_in_records/', view_func=MoveInRecordApi.as_view('move_in_record_api'),
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
app.add_url_rule('/move_out_records/', view_func=MoveOutRecordApi.as_view('move_out_record_api'),
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
app.add_url_rule('/absence_records/', view_func=AbsenceRecordApi.as_view('absence_record_api'),
                 methods=['GET', 'POST', 'DELETE', 'PUT'])

app.add_url_rule('/buildings/', view_func=BuildingApi.as_view('building_api'), methods=['GET', 'POST', 'DELETE', 'PUT'])

app.add_url_rule('/dormitories/', view_func=DormitoryApi.as_view('dormitory_api'),
                 methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == '__main__':
    app.run(debug=True)
