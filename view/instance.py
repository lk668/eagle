#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app
from flask import request, render_template, url_for, session, flash, redirect, jsonify
import datetime
from utils import UiQueue
from utils import eagle_logger
import json
from model import Instance
from model import User
from utils import db

@app.route('/list_ins', methods=['GET'])
def list_instance():
    res = {}
    instances = []
    user_query_result = db.session.query(User).filter(User.username == request.args.get('signin_username')).first()
    if user_query_result is not None:
        instances = db.session.query(Instance).filter(Instance.user_id == user_query_result.id).all()
    ins_list = []
    eagle_logger.debug('list: %s' % request.args.get('signin_user_name'))
    for ins in instances:
        ins_item = {}
        ins_item['image_id'] = ins.image_id
        ins_item['container_serial'] = ins.container_serial
        ins_item['container_name'] = ins.container_name
        ins_item['host'] = ins.host
        ins_item['port'] = ins.port
        ins_item['status'] = ins.status
        ins_list.append(ins_item)
    res['code'] = 'ok'
    res['instances'] = ins_list
    return jsonify(**res)

@app.route('/create_ins', methods=['GET', 'POST'])
def create_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = db.session.query(Instance).filter(\
            Instance.container_name == req_data['container_name']).first()
        if instance_query_result is None:
            policy = {}
            policy['operate'] = app.config['CREATE_INSTANCE']
            policy['image_id'] = req_data['image_id']
            policy['container_name'] = req_data['container_name']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            #blocking max time: 60s
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['instance'] = worker_res_dict['ins']
            eagle_logger.info(res['message'])
            eagle_logger.info('db add instance commit!')
        else:
            res['code'] = 'err'
            res['message'] = 'container name occupied.'
            eagle_logger.info('container name occupied.')
    return jsonify(**res)

@app.route('/stop_ins', methods=['GET', 'POST'])
def stop_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = db.session.query(Instance).filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['STOP_INSTANCE']
            policy['container_serial'] = req_data['container_serial']
            policy['container_name'] = instance_query_result.container_name
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['container_serial'] = worker_res_dict['container_serial']
            eagle_logger.info(res['message'])
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

@app.route('/remove_ins', methods=['GET', 'POST'])
def remove_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = db.session.query(Instance).filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['REMOVE_INSTANCE']
            policy['container_serial'] = req_data['container_serial']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['container_serial'] = worker_res_dict['container_serial']
            eagle_logger.info(res['message'])
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

