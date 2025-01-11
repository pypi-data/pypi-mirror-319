from . import interceptor_entrance, interceptor_user_info

from . import

def register_middlewares(app):
    app.middleware("http")(interceptor_entrance.trace_log_filter_entrance)
    app.middleware("http")(interceptor_user_info.)
