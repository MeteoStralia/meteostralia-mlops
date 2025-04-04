from prometheus_client import make_asgi_app, Counter, Gauge, Summary, generate_latest
from prometheus_client import CollectorRegistry

metrics_app = make_asgi_app()
collector = CollectorRegistry()

def home_counter():
    home_counter = Counter(name = 'home_counter',
                            documentation = 'total home page request',
                            labelnames = ['method', 'endpoint']
                            )
    return home_counter

def home_summary():
    home_summary = Summary(name = 'home_summary',
                           documentation = 'test summary')
    return home_summary



def login_counter():
    login_counter = Counter(name = 'login_counter',
                            documentation = 'number of time login requested',
                            labelnames = ['status_code']
                            )
    return login_counter

def login_wrong_user_counter():
    login_wrong_user_counter = Counter(name = 'login_wrong_user_counter',
                                       documentation = 'counter wrong username request')
    return login_wrong_user_counter
