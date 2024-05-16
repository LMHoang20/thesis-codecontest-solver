import threading

def make_message(*messages):
    parsed_messages = []
    for m in messages:
        if m == None:
            parsed_messages.append('None')
        else:
            parsed_messages.append(str(m))
    return ' '.join(parsed_messages)
            
class Logger:
    def __init__(self, name='logger'):
        self.name = name
    def info(self, *messages):
        pass
    def error(self, *messages):
        pass
    def warning(self, *messages):
        pass

class ConsoleLogger(Logger):
    def __init__(self, name='console'):
        self.name = name
    def info(self, *messages):
        message = make_message(*messages)
        print(f'[{self.name}-INFO] {message}')
    def error(self, *messages):
        message = make_message(*messages)
        print(f'[{self.name}-ERROR] {message}')
    def warning(self, *messages):
        message = make_message(*messages)
        print(f'[{self.name}-WARNING] {message}')

class FileLogger(Logger):
    def __init__(self, path, name='file'):
        self.path = path
        self.name = name
    def info(self, *messages):
        message = make_message(*messages)
        with open(self.path, 'a') as f:
            f.write(f'[{self.name}-INFO] {message}\n')
    def error(self, *messages):
        message = make_message(*messages)
        with open(self.path, 'a') as f:
            f.write(f'[{self.name}-ERROR] {message}\n')
    def warning(self, *messages):
        message = make_message(*messages)
        with open(self.path, 'a') as f:
            f.write(f'[{self.name}-WARNING] {message}\n')
            
class DatabaseLogger(Logger):
    def __init__(self, connection, table, session_id):
        self.connection = connection
        self.table = table
        self.session_id = session_id
        self.insert = f'INSERT INTO {self.table}'
    def info(self, *messages):
        message = make_message(*messages)
        with self.connection.cursor() as cursor:
            cursor.execute(self.insert + ' VALUES (%s, %s, %s)', (self.session_id, 'INFO', message))
    def error(self, *messages):
        message = make_message(*messages)
        with self.connection.cursor() as cursor:
            cursor.execute(self.insert + ' VALUES (%s, %s, %s)', (self.session_id, 'ERROR', message))
    def warning(self, *messages):
        message = make_message(*messages)
        with self.connection.cursor() as cursor:
            cursor.execute(self.insert + ' VALUES (%s, %s, %s)', (self.session_id, 'WARNING', message))

class ThreadSafe(Logger):
    def __init__(self, logger):
        self.logger = logger
        self.lock = threading.Lock()
    def info(self, *messages):
        with self.lock:
            self.logger.info(messages)
    def error(self, *messages):
        with self.lock:
            self.logger.error(messages)
    def warning(self, *messages):
        with self.lock:
            self.logger.warning(messages)

def get_logger(type='console', config={'threadsafe': False}) -> Logger:
    logger = Logger()
    match type:
        case 'console':
            if 'name' in config:
                logger = ConsoleLogger(config['name'])
            else:
                logger = ConsoleLogger()
        case 'file':
            if 'name' in config:
                logger = FileLogger(config['path'], config['name'])
            else:
                logger = FileLogger(config['path'])
        case 'database':
            logger = DatabaseLogger(config['connection'], config['table'], config['session_id'])
        case _:
            raise ValueError('Invalid logger type')
    if config['threadsafe']:
        logger = ThreadSafe(logger)
    return logger
    
