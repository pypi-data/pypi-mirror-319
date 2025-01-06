import time
import logging
from logging.handlers import RotatingFileHandler
from prometheus_client import Counter,Histogram,make_wsgi_app, Gauge
import os
from pythonjsonlogger import jsonlogger
import contextvars
import json
from starlette.responses import Response
from ddtrace import tracer
from ddtrace.context import Context
from ddtrace.propagation.http import HTTPPropagator
import inspect


class UTF8JsonFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
  #  @tracer.wrap(enable=False)   
    def format(self, record):
        # 从当前 span 获取 trace_id
        span = tracer.current_span()
        trace_id = str(span.trace_id) if span else "0"
        span_id = str(span.span_id) if span else "0"
        
        # 自动设置 logger_name 为模块名
        if not getattr(record, 'logger_name', None):
            # 直接使用 record 中的 module 属性
            record.logger_name = record.module  # 设置为模块名

        log_data = {
            'time': self.formatTime(record),
            'level': record.levelname,
            'msg': record.getMessage(),
            'args':record.args,
            'stack_trace':record.stack_info,
            'logger': record.logger_name  # 使用自动设置的 logger_name
        }
        
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        log_data.update(request_context.get())
        return json.dumps(log_data, ensure_ascii=False)
    
# 创建上下文变量
request_context = contextvars.ContextVar('request_context', default={})

#Prometheus指标
REQUEST_COUNT = Counter('http_requests_total','Total HTTP Requests',
                        ['method','uri'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 
                            'HTTP Request Duration', ['method', 'uri'])
CPU_USAGE_GAUGE = Gauge('cpu_usage_percent', 'CPU Usage Percentage')
MEMORY_USAGE_GAUGE = Gauge('memory_usage_percent', 'Memory Usage Percentage')

# 后台线程更新 CPU 和内存使用情况
# def update_resource_usage():
#     while True:
#         # 获取 CPU 和内存使用率
#         cpu_usage = psutil.cpu_percent(interval=1)
#         memory_usage = psutil.virtual_memory().percent
#         
#         # 更新 Prometheus 指标
#         CPU_USAGE_GAUGE.set(cpu_usage)
#         MEMORY_USAGE_GAUGE.set(memory_usage)

# 创建并启动后台线程
#threading.Thread(target=update_resource_usage, daemon=True).start()

class ObservabilityMiddleware:
    def __init__(self, app, log_config=None):
        self.app = app
        self.common_extra = {
            "appName": log_config['app_name'] # 从 log_config 中读取 app_name
        }
        self.tracer = tracer
        self.propagator = HTTPPropagator()
        
        # 自定义日志配置
        log_config = {
            'app_name': 'sino-observability',  # 添加 app_name 字段
            'log_dir': 'logs',  # 相对路径，会在项目根目录下创建
            'log_file': f"{log_config['app_name']}_{time.strftime('%Y-%m-%d')}.log",  # 修改 log_file 格式
            'max_bytes': 20 * 1024 * 1024,  # 20MB
            'backup_count': 10,
            'level': logging.INFO
        }

        # 更新配置
        self.log_config = log_config
        if log_config:
            self.log_config.update(log_config)

        # 确保日志目录存在
        os.makedirs(self.log_config['log_dir'], exist_ok=True)

        # 设置日志处理器
        formatter = UTF8JsonFormatter()

        # 文件处理器
        log_path = os.path.join(self.log_config['log_dir'], self.log_config['log_file'])
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=self.log_config['max_bytes'],
            backupCount=self.log_config['backup_count'],
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 配置根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_config['level'])

        # 移除所有已存在的处理器
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # 添加处理器到根日志器
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)


        # 启动异步任务以定期更新指标
        # try:
        #     loop = asyncio.get_running_loop()  # 检查是否有正在运行的事件循环
        # except RuntimeError:  # 如果没有，则创建一个新的事件循环
        #     loop = asyncio.new_event_loop()
        #     asyncio.set_event_loop(loop)
        # loop.create_task(self.update_resource_usage())

    # async def update_resource_usage(self):
    #     while True:
    #         # 获取 CPU 和内存使用率
    #         cpu_usage = psutil.cpu_percent(interval=1)
    #         memory_usage = psutil.virtual_memory().percent
            
    #         # 更新 Prometheus 指标
    #         CPU_USAGE_GAUGE.set(cpu_usage)
    #         MEMORY_USAGE_GAUGE.set(memory_usage)
            
    #         # 添加日志以确认方法被调用
    #         logger.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
            
    #         # 每 5 秒更新一次
    #         await asyncio.sleep(5)

    # FastAPI 处理
    async def __call__(self, request, call_next):
        start_time = time.time()  # 记录开始时间

        # 提取链路上下文
        headers = dict(request.headers)
        context = self.propagator.extract(headers)
        if context:
            self.tracer.context_provider.activate(context)

        # 创建 span
        with self.tracer.trace(
            "http.request",
            service=self.common_extra["appName"],
            resource=f"{request.method} {request.url.path}",
            span_type="web"
        ) as span:
            span.set_tag("http.method", request.method)
            span.set_tag("http.url", str(request.url))
            
            context = {
                **self.common_extra,
                "URI": f"{request.method} {request.url.path}",
                "dd.trace_id": str(span.trace_id),
                "dd.span_id": str(span.span_id)
            }
            request_context.set(context)

            if request.url.path == "/metrics":
                return Response(
                    content=make_wsgi_app()(
                        {"PATH_INFO": "/metrics", "REQUEST_METHOD": "GET"},
                        lambda *args: None
                    )[0],
                    media_type="text/plain"
                )

            try:
                #输出请求开始
                logger.info("%s %s Start",request.method,request.url.path,extra=context) 
                response = await call_next(request)
                span.set_tag("http.status_code", response.status_code)
                
                duration = int((time.time() - start_time) * 1000)  # 转换为毫秒
                context["responseTime"] = duration  # 设置响应时间
                request_context.set(context)  # 更新上下文
                
                REQUEST_COUNT.labels(
                    method=request.method,
                    uri=request.url.path
                ).inc()
                REQUEST_LATENCY.labels(
                    method=request.method,
                    uri=request.url.path
                ).observe(duration)

               #输出请求END数据 
                logger.info("%s %s End",request.method,request.url.path,extra=context) 
                return response
            except Exception as e:
                span.set_tag("error", str(e))
                span.set_tag("error.type", type(e).__name__)
                raise

    # Flask 处理
    def __call_wsgi__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        if path == '/metrics':
            return make_wsgi_app()(environ, start_response)

        # 提取链路上下文
        headers = {k[5:].lower(): v for k, v in environ.items() 
                  if k.startswith('HTTP_')}
        context = self.propagator.extract(headers)
        if context:
            self.tracer.context_provider.activate(context)

        start_time = time.time()
        
        # 创建 span
        with self.tracer.trace(
            "http.request",
            service=self.common_extra["appName"],
            resource=f"{method} {path}",
            span_type="web"
        ) as span:
            span.set_tag("http.method", method)
            span.set_tag("http.url", path)
            
            context = {
                **self.common_extra,
                "URI": f"{method} {path}",
                "dd.trace_id": str(span.trace_id),
                "dd.span_id": str(span.span_id)
            }
            request_context.set(context)

            status_code = None
            def custom_start_response(status, headers, exc_info=None):
                nonlocal status_code
                status_code = int(status.split()[0])
                span.set_tag("http.status_code", status_code)
                
                duration = int(1000 * (time.time() - start_time))  # 转换为整型
                context["responseTime"] = duration  # 直接赋值为整型
                request_context.set(context)
                
                REQUEST_COUNT.labels(
                    method=method,
                    uri=path
                ).inc()
                REQUEST_LATENCY.labels(
                    method=method,
                    uri=path
                ).observe(duration)

                logger.info("%s %s End",method,path,extra=context) 
                return start_response(status, headers, exc_info)

            try:
                logger.info("%s %s Start",method,path,extra=context) 
                return self.app(environ, custom_start_response)
            except Exception as e:
                span.set_tag("error", str(e))
                span.set_tag("error.type", type(e).__name__)
                raise

    # _convert_wsgi_to_asgi 方法保持不变
"""
# 创建一个包装器函数来自动添加上下文信息
def log_with_context(func):
    def wrapper(self, message, *args, **kwargs):
        context = request_context.get()  # 获取当前上下文
        # 获取调用的函数名
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            func_name = caller_frame.f_code.co_name
        finally:
            del frame
        # 合并上下文到 kwargs['extra']
        if 'extra' in kwargs:
            if kwargs['extra'] is None:
                kwargs['extra'] = {}
            if isinstance(kwargs['extra'], dict):
                kwargs['extra'] = {**context, **kwargs['extra']}  # 合并上下文和额外信息
        else:
            kwargs['extra'] = context  # 如果没有extra，直接使用上下文  
        # 将函数名添加到 extra 中
        kwargs['extra']['funcName'] = func_name      
        # 直接调用 func，确保 extra 被包含在 kwargs 中
        return func(self, message, *args, **kwargs)  # 这里的 kwargs 已经包含了 extra
    return wrapper
"""
# 扩展 Logger 类
class ContextLogger(logging.Logger):
    def _process_extra(self, kwargs):
        context = request_context.get()  # 获取当前上下文
        class_name, func_name = self.get_caller_class_and_func_name()

        if 'extra' in kwargs:
            if kwargs['extra'] is None:
                kwargs['extra'] = {}
            if isinstance(kwargs['extra'], dict):
                kwargs['extra'] = {**context, **kwargs['extra']}  # 合并上下文和额外信息
                request_context.set(kwargs['extra'])
        else:
            kwargs['extra'] = context  # 如果没有extra，直接使用上下文
        kwargs['extra']['callerFuncName'] = func_name
        kwargs['extra']['callerClassName'] = class_name

        return kwargs
    def get_caller_class_and_func_name(self):
        stack = inspect.stack()
        caller_frame_info = stack[3]  # 获取调用 logger 的帧
        caller_frame = caller_frame_info.frame  # 获取实际的帧对象
        local_vars = caller_frame.f_locals 
        # 获取类名
        class_name = local_vars['self'].__class__.__name__ if 'self' in local_vars else "Unknown"
        # 获取函数名
        func_name = caller_frame.f_code.co_name
        
        return class_name, func_name  # 返回类名和函数名的元组
    
    def info(self, message, *args, **kwargs):
        kwargs = self._process_extra(kwargs)  # 处理 extra
        super().info(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        kwargs = self._process_extra(kwargs)
        super().error(message, *args, **kwargs)
    def warning(self, message, *args, **kwargs):
        kwargs = self._process_extra(kwargs) 
        super().warning(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        kwargs = self._process_extra(kwargs)  
        super().debug(message, *args, **kwargs)

# 注册自定义 Logger 类
logging.setLoggerClass(ContextLogger)
logger = logging.getLogger("observability")