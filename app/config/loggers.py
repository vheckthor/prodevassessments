"""
    Logger module
"""
import inspect
import logging


log = logging.getLogger('ProdevsAssessments')


def _get_caller_object_name():
    stack_trace = inspect.stack()[2][0]
    if 'self' in stack_trace.f_locals:
        caller_obj_name = stack_trace.f_locals['self'].__class__.__name__
    elif '__name__' in stack_trace.f_locals:
        caller_obj_name = stack_trace.f_locals['__name__']
    else:
        caller_obj_name = stack_trace.f_code.co_name
    return caller_obj_name


def log_error(exception) -> None:
    """
    This function is used to log all errors.

    Sample:
        ERROR-... - [ERROR] on running file:
        Exception is: ValueError
        Error is: test_error
    """
    caller = _get_caller_object_name()
    message = f'[ERROR] on running file: <{caller}> \n'
    message += f'   Exception is: {str(exception.__class__.__name__)} \n'
    message += f'   Error is: {str(exception)} \n'

    log.error(message)


def log_info(data) -> None:
    """
    log_info info logger

    Args:
        data (Any): data to log
    """
    log.info(data)


def log_warning(data) -> None:
    """
    log_warning warning logger

    Args:
        data (Any): data to log
    """
    log.warning(data)
