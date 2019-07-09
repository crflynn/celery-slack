"""Celery configuration settings.

http://docs.celeryproject.org/en/latest/userguide/configuration.html#general-settings
Most of the settings commented here with default values.
"""
from .schedule import get_imports
from .schedule import get_schedule


# General settings
accept_content = ["json"]


# Time and date settings
enable_utc = True
timezone = "UTC"


# Task settings
# task_annotations = None
# task_compression = None
# task_protocol = 2
task_serializer = "json"
# task_publish_retry = True
# task_publish_retry_policy = {}


# Task execution settings
# task_always_eager = False
# task_eager_propagates = False
# task_remote_tracebacks = False
# task_ignore_result = False
# task_store_errors_even_if_ignored = False
# task_track_started = False
# task_time_limit = None
# task_soft_time_limit = None
# task_acks_late = False
# task_reject_on_worker_lost = False
# task_default_rate_limit = None


# Task result backend settings
result_backend = "redis://localhost:6379"
# result_backend = "amqp://guest:guest@localhost:5672//"
result_serializer = "json"
# result_compression = None
result_expires = 172800
# result_cache_max = False


# Database backend settings
# database_engine_options = {}
# database_short_lived_sessions = False
# database_table_names = {}


# RPC backend settings
# result_persistent = False


# Cache backend settings
# cache_backend_options = {}


# Redis backend settings
# redis_max_connections = None
# redis_socket_connect_timeout = None
redis_socket_timeout = 30


# Message Routing
# task_queues = None
# task_routes = None
# worker_direct = False
# task_create_missing_queues = True
# task_default_queue = "celery"
# task_default_exchange = "celery"
# task_default_exchange_type = "direct"
# task_default_routing_key = "celery"
# task_default_delivery_mode = "persistent"


# Broker settings
broker_url = "redis://localhost:6379"
BROKER_URL = "redis://localhost:6379"
# broker_url = "amqp://guest:guest@localhost:5672//"
# broker_read_url = broker_url
# broker_write_url = broker_url
# broker_failover_strategy = "round-robin"
# broker_use_ssl = False
# broker_pool_limit = 10
# broker_connection_timeout = 4.0
# broker_connection_retry = True
# broker_connection_max_retries = 100
# broker_login_method = "AMQPLAIN"
# broker_transport_options = {}


# Beat settings
beat_schedule = get_schedule()
# beat_scheduler = "celery.beat:PersistentScheduler"
# beat_schedule_filename = "celerybeat-schedule"
# beat_sync_every = 0
# beat_max_loop_interval = 0


# Worker settings
imports = get_imports(beat_schedule)
# include = []
worker_concurrency = 8
worker_prefetch_multiplier = 1
# worker_lost_wait = 10.0
# worker_max_tasks_per_child = None
# worker_max_memory_per_child = None
# worker_disable_rate_limits = False
# worker_state_db = None
# worker_timer_precision = 1.0
# worker_enable_remote_control = True


# Events settings
# worker_send_task_events = False
# task_send_sent_event = False
# event_queue_prefix = "celeryev"
event_serializer = "json"


# Remote Control commands
# control_queue_ttl = 300.0
# control_queue_expires = 10.0


# Logging settings
# worker_hijack_root_logger = True
# worker_log_color = True
# worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"  # noqa
# worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"  # noqa
# worker_redirect_stdouts = True
# worker_redirect_stdouts_level = "WARNING"


# Security options
# security_key = None
# security_certificate = None
# security_cert_store = None


# Custom component classes
# worker_pool = "prefork"
# worker_pool_restarts = False
# worker_autoscaler = "celery.worker.autoscale:Autoscaler"
# worker_consumer = "celery.worker.consumer:Consumer"
# worker_timer = "kombu.async.hub.timer:Timer"
