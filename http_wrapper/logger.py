import logging, os

main_logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__ + '.general')
access_logger = logging.getLogger(__name__ + '.access')

log_dir = os.environ.get("SIIBRA_TOOLBOX_LOG_DIR")

if log_dir:
    from logging.handlers import TimedRotatingFileHandler
    import socket
    
    general_filename = os.path.join(log_dir, f"{socket.gethostname()}.general.log")
    general_log_handler = TimedRotatingFileHandler(general_filename, when="d", encoding="utf-8")
    
    access_filename = os.path.join(log_dir, f"{socket.gethostname()}.access.log")
    access_log_handler = TimedRotatingFileHandler(access_filename, when="d", encoding="utf-8")

else:
    general_log_handler = logging.StreamHandler()
    access_log_handler = logging.StreamHandler()

formatter = logging.Formatter('[%(name)s:%(levelname)s]  %(message)s')
general_log_handler.setFormatter(formatter)
logger.addHandler(general_log_handler)

access_log_formatter = logging.Formatter('%(asctime)s - %(status)s - %(process_time_ms)s - %(message)s')
access_log_handler.setFormatter(access_log_formatter)
access_logger.addHandler(access_log_handler)
