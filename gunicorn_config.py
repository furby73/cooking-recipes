import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 4
timeout = 30
keepalive = 2

preload_app = True
max_requests = 1200
max_requests_jitter = 50

accesslog = "-"
errorlog = "-"
loglevel = "info"

worker_class = "gthread"