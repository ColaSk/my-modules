# -*- encoding: utf-8 -*-
'''
@File    :   task_signals.py
@Time    :   2021/10/29 17:12:16
@Author  :   sk 
@Version :   1.0
@Contact :   ldu_sunkaixuan@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import logging
from celery.signals import (task_failure, task_postrun, task_prerun,
                            task_received, task_success)
from celery import Task

logger = logging.getLogger(__name__)

loginfo = "task id: {task_id}, method: {method}"

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, 
                        task=None, *args, **kwargs):
    """执行任务之前"""
    logger.info(loginfo.format(task_id=task_id, method='task prerun').center(128, '*'))
    

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, 
                         task=None, retval=None, 
                         state=None, *args, **kwargs):
    """执行任务之后"""
    logger.info(loginfo.format(task_id=task_id, method='task post run').center(128, '*'))

@task_success.connect
def task_success_handler(sender=None, result=None, *args, **kwargs):
    """任务成功之后"""
    logger.info("task_name: {task_name}, method: {method}, result: {result}".format(
                 task_name=sender.name, method='task success', result=result))

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, 
                         exception=None, traceback=None, 
                         einfo=None, *args, **kwargs):
    """任务失败之后"""
    logger.error("task id: {task_id}, method: {method}, einfo: {einfo}".format(
                 task_id=task_id, method='task failure', einfo=einfo))

@task_received.connect
def task_received_handler(sender=None, request=None, **kwargs):
    """当从代理接收到任务，并开始执行时"""
    logger.info(loginfo.format(task_id=request.task_id, method='task received').center(128, '*'))
