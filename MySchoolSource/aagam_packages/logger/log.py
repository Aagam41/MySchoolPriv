import logging
log = logging.getLogger("AagamLogger")
log.setLevel(logging.DEBUG)
log_handler = logging.FileHandler("Logs/myschool.log")
log_handler.mode = "a"
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - '
           '%(message)s - %(process)d - %(processName)s - %(thread)d - %(threadName)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)
log.propagate = False