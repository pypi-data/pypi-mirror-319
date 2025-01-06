#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from abc import ABCMeta, abstractmethod

from testbot.app.base import TestType
from testbot.result.testreporter import StepReporter


class PreConditionBase(metaclass=ABCMeta):
    """
    前置条件判断基类
    """
    @abstractmethod
    def is_meet(self, test_case, reporter: StepReporter):
        pass

    @abstractmethod
    def get_description(self):
        pass


class IsTestCaseType(PreConditionBase):
    """
    判断测试用例是否是指定的类型
    """
    def __init__(self, expected_type):
        self.case_type = expected_type

    def is_meet(self, test_case, reporter: StepReporter):
        ret = test_case.test_type and self.case_type > 0
        if ret:
            reporter.logger.info(msg=self.get_description())
        else:
            reporter.logger.info(self.get_description() + f",当前测试用例类型是{test_case.test_type}")
        return ret

    def get_description(self):
        return f"测试用例的类型必须是{TestType(self.case_type).name}"


class IsTestCasePriority(PreConditionBase):
    """
    判断测试用例是否是指定额优先级
    """
    def __init__(self, expected_priority):
        self.priority = expected_priority

    def is_meet(self, test_case, reporter: StepReporter):
        ret = test_case.priority in self.priority
        if ret:
            reporter.logger.info(message=self.get_description())
        else:
            reporter.logger.info(message=self.get_description() + f",当前测试用例优先级是{test_case.priority}")
        return ret

    def get_description(self):
        return f"测试用例的优先级必须是{self.priority}"


class IsPreCasePassed(PreConditionBase):
    """
    判断前置测试用例是否是某个期望的结果
    """
    def __init__(self, result_list):
        self.result_list = result_list

    def is_meet(self, test_case, reporter: StepReporter):
        if not any(test_case.pre_tests):
            # 没有前置测试用例，直接返回真
            return True
        for pre_case in test_case.pre_tests:
            for case, data in self.result_list.items():
                if pre_case == case:
                    if not data['result']:
                        reporter.logger.info(message=f"{case}的执行结果不成功")
                        return False
                    else:
                        break
            else:
                reporter.logger.info(message=f"{pre_case}没有执行")
                return False
        reporter.logger.info(message=self.get_description())
        return True

    def get_description(self):
        return "前置测试用例运行结果必须为通过"


class IsHigherPriorityPassed(PreConditionBase):
    """
    高优先级测试用例全部通过
    """
    def __init__(self, priority, result_list):
        self.priority = priority
        self.result_list = result_list

    def is_meet(self, test_case, reporter: StepReporter):
        if not test_case.skip_if_high_priority_failed:
            return True
        for case, data in self.result_list.items():
            if data['priority']<self.priority and not data["result"]:
                reporter.logger.info(message=f"测试用例{case}没有执行成功")
                return False
        reporter.logger.info(message=self.get_description())
        return

    def get_description(self):
        return f"优先级{self.priority}以上的测试用例必须通过"
