# -*- coding: utf-8 -*-
# 版权所有 2019 深圳米筐科技有限公司（下称“米筐科技”）
#
# 除非遵守当前许可，否则不得使用本软件。
#
#     * 非商业用途（非商业用途指个人出于非商业目的使用本软件，或者高校、研究所等非营利机构出于教育、科研等目的使用本软件）：
#         遵守 Apache License 2.0（下称“Apache 2.0 许可”），您可以在以下位置获得 Apache 2.0 许可的副本：http://www.apache.org/licenses/LICENSE-2.0。
#         除非法律有要求或以书面形式达成协议，否则本软件分发时需保持当前许可“原样”不变，且不得附加任何条件。
#
#     * 商业用途（商业用途指个人出于任何商业目的使用本软件，或者法人或其他组织出于任何目的使用本软件）：
#         未经米筐科技授权，任何个人不得出于任何商业目的使用本软件（包括但不限于向第三方提供、销售、出租、出借、转让本软件、本软件的衍生产品、引用或借鉴了本软件功能或源代码的产品或服务），任何法人或其他组织不得出于任何目的使用本软件，否则米筐科技有权追究相应的知识产权侵权责任。
#         在此前提下，对本软件的使用同样需要遵守 Apache 2.0 许可，Apache 2.0 许可与本许可冲突之处，以本许可为准。
#         详细的授权流程，请联系 public@ricequant.com 获取。

from datetime import datetime
import logbook
from logbook import Logger, StderrHandler

from rqalpha.utils.py2 import to_utf8

logbook.set_datetime_format("local")


# patch warn
logbook.base._level_names[logbook.base.WARNING] = 'WARN'


__all__ = [
    "user_log",
    "system_log",
    "user_system_log",
]


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def user_std_handler_log_formatter(record, handler):
    from rqalpha.environment import Environment
    try:
        dt = Environment.get_instance().calendar_dt.strftime(DATETIME_FORMAT)
    except Exception:
        dt = datetime.now().strftime(DATETIME_FORMAT)

    log = "{dt} {level} {msg}".format(
        dt=dt,
        level=record.level_name,
        msg=to_utf8(record.message),
    )
    return log


user_std_handler = StderrHandler(bubble=True)
user_std_handler.formatter = user_std_handler_log_formatter


def formatter_builder(tag):
    def formatter(record, handler):

        log = "[{formatter_tag}] [{time}] {level}: {msg}".format(
            formatter_tag=tag,
            level=record.level_name,
            msg=to_utf8(record.message),
            time=record.time,
        )

        if record.formatted_exception:
            log += "\n" + record.formatted_exception
        return log
    return formatter


# loggers
# 用户代码logger日志
user_log = Logger("user_log")
# 给用户看的系统日志
user_system_log = Logger("user_system_log")

# 用于用户异常的详细日志打印
user_detail_log = Logger("user_detail_log")
# user_detail_log.handlers.append(StderrHandler(bubble=True))

# 系统日志
system_log = Logger("system_log")
basic_system_log = Logger("basic_system_log")

# 标准输出日志
std_log = Logger("std_log")


def init_logger():
    system_log.handlers = [StderrHandler(bubble=True)]
    basic_system_log.handlers = [StderrHandler(bubble=True)]
    std_log.handlers = [StderrHandler(bubble=True)]
    user_log.handlers = []
    user_system_log.handlers = []


def user_print(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "")

    message = sep.join(map(str, args)) + end

    user_log.info(message)


init_logger()
