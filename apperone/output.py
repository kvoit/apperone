import syslog


def log(message, level=syslog.LOG_INFO):
    print(message)
    syslog.openlog(ident='apperone', logoption=syslog.LOG_PID, facility=syslog.LOG_DAEMON)
    syslog.syslog(level, message)
    syslog.closelog()
