import logging

from nameko.extensions import DependencyProvider


def _worker_ctx_to_dict(worker_ctx):
    ctx = {
        'call_id': worker_ctx.call_id,
        'call_id_parent': worker_ctx.immediate_parent_call_id,
        'call_id_stack': worker_ctx.call_id_stack,
        'method_name': worker_ctx.entrypoint.method_name,
        'service_name': worker_ctx.service_name,
        'data': worker_ctx.data,
    }
    return {'worker': ctx}


def _exception_info_to_dict(exc_info):
    exc_type, msg, traceback = exc_info
    info = {'type': exc_type, 'message': msg, 'traceback': traceback}
    return {'exception_info': info}


class WorkerLogger(DependencyProvider):
    """Logs exceptions and provides logger with worker's contextual info."""

    def __init__(self):
        """:param logger_name: name of logger instance."""
        # self.logger = logging.getLogger(logger_name)
        pass

    def get_dependency(self, worker_ctx):
        """Create logger adapter with worker's contextual data."""
        worker_info = _worker_ctx_to_dict(worker_ctx)
        if not hasattr(self, "adapter"):
            self.logger = logging.getLogger(worker_ctx.service_name)
        adapter = logging.LoggerAdapter(self.logger, extra=worker_info)
        return adapter

    def worker_setup(self, worker_ctx):
        """Log task info, before starting task execution."""
        method_name =  worker_ctx.entrypoint.method_name
        service_name = worker_ctx.service_name
        logger = self.get_dependency(worker_ctx)
        logger.info(
            f"service: {service_name} method: {method_name} start.".center(100, "*")
        )

    def worker_result(self, worker_ctx, result=None, exc_info=None):
        """Log exception info, if it is present."""
        method_name =  worker_ctx.entrypoint.method_name
        service_name = worker_ctx.service_name
        logger = self.get_dependency(worker_ctx)
        
        if not exc_info is None:
            
            logger.info( f"service: {service_name} method: {method_name} error start.".center(100, "*"))
            exception_info = _exception_info_to_dict(exc_info)
            logger.error(exception_info)
            logger.info( f"service: {service_name} method: {method_name} error end.".center(100, "*"))

        logger.info(f"service: {service_name} method: {method_name} end.".center(100, "*"))