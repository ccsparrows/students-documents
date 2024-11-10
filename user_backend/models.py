# -*- coding: utf-8 -*-
from extension import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def init_db():
        rets = [
            ('ad1', '111111'),
            ('ad2', '222222'),
            ('ad3', '333333'),
        ]
        for ret in rets:
            user = User()
            user.username = ret[0]
            user.password = ret[1]
            db.session.add(user)
        db.session.commit()  # 提交数据库会话，将修改保存到数据库中


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

    @staticmethod
    def init_students():
        rets = [
            (101, '小1', '男'),
            (102, '小2', '女'),
        ]
        for ret in rets:
            student = Student(id=ret[0], name=ret[1], sex=ret[2])
            db.session.add(student)
        db.session.commit()


class MoveInRecord(db.Model):
    __tablename__ = 'move_in_records'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), db.ForeignKey('students.id'), nullable=False)
    move_in_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    build_number = db.Column(db.Integer, nullable=False)
    room_number = db.Column(db.Integer, nullable=False)

    @staticmethod
    def init_move_in_records():
        rets = [
            (101, "小一", datetime.datetime(2023, 9, 1), 1, 101),
            (102, "小二", datetime.datetime(2023, 9, 2), 2, 102)
        ]
        for ret in rets:
            record = MoveInRecord(
                id=ret[0],
                student_name=ret[1],
                move_in_time=ret[2],
                build_number=ret[3],
                room_number=ret[4]
            )
            db.session.add(record)
        db.session.commit()


class MoveOutRecord(db.Model):
    __tablename__ = 'move_out_records'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), db.ForeignKey('students.id'), nullable=False)
    move_out_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    reason = db.Column(db.String(255))

    @staticmethod
    def init_move_out_records():
        rets = [
            (104, "小四", datetime.datetime(2024, 6, 1), '毕业'),
            (101, "小一", datetime.datetime(2024, 6, 1), '毕业'),
            (102, "小二", datetime.datetime(2024, 6, 2), '毕业')
        ]
        for ret in rets:
            record = MoveOutRecord(
                id=ret[0],
                student_name=ret[1],
                move_out_time=ret[2],
                reason=ret[3]
            )
            db.session.add(record)
        db.session.commit()


class AbsenceRecord(db.Model):
    __tablename__ = 'absence_records'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), db.ForeignKey('students.id'), nullable=False)
    absence_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    reason = db.Column(db.String(200))

    @staticmethod
    def init_absence_records():
        rets = [
            (101, "小一", datetime.datetime(2023, 11, 1), '病假'),
            (102, "小二", datetime.datetime(2023, 11, 2), '事假'),
            (103, "Jude", datetime.datetime(2023, 11, 2), '事假')
        ]
        for ret in rets:
            record = AbsenceRecord(
                id=ret[0],
                student_name=ret[1],
                absence_time=ret[2],
                reason=ret[3]
            )
            db.session.add(record)
        db.session.commit()


# 楼层管理模型
class Building(db.Model):
    __tablename__ = 'buildings'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    dorm_manager_id = db.Column(db.Integer, nullable=False)
    dorm_manager = db.Column(db.String(50), nullable=False)

    @staticmethod
    def init_buildings():
        rets = [
            (1, '1', 'Address 1', 1, 'Manager 1'),
            (2, '2', 'Address 2', 2, 'Manager 2')
        ]
        for ret in rets:
            building = Building(
                id=ret[0],
                number=ret[1],
                address=ret[2],
                dorm_manager_id=ret[3],
                dorm_manager=ret[4]
            )
            db.session.add(building)
        db.session.commit()


# 宿舍管理模型
class Dormitory(db.Model):
    __tablename__ = 'dormitories'
    id = db.Column(db.Integer, primary_key=True)
    build_address = db.Column(db.String(50), nullable=False)
    room_number = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, nullable=False)

    @staticmethod
    def init_dormitories():
        rets = [
            (1, '北区', '1-101', 4, 3),
            (2, '南区', '2-102', 4, 4)
        ]
        for ret in rets:
            dormitory = Dormitory(
                id=ret[0],
                build_address=ret[1],
                room_number=ret[2],
                capacity=ret[3],
                current_occupancy=ret[4]
            )
            db.session.add(dormitory)
        db.session.commit()
