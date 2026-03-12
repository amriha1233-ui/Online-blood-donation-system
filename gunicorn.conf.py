"""
Gunicorn configuration for production deployment
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = max(multiprocessing.cpu_count() - 1, 2)
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "obdms"

# Preload app
preload_app = True

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ssl_version = None
cert_reqs = 0
ca_certs = None
suppress_ragged_eof = True
do_handshake_on_connect = False
ciphers = None

# Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    pass

def on_exit(server):
    """Called just before exiting."""
    pass

def pre_fork(server, worker):
    """Called just after a worker has been forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    pass

def pre_exec(server):
    """Called just before a new master process has been created."""
    pass

def when_ready(server):
    """Called just after the server is started."""
    pass

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    pass
