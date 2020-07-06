import unittest

class FakeScanner:
    def __init__(self, config):
        self.config = config

class TestDefaultMessageStartParser(unittest.TestCase):

    def test_process_log_debug(self):

        config = { '_formats': {'format': {}}

        }
        scanner = FakeScanner(config)
        app = { 'name': 'pyramid',
                'config':
                    {'params':  {'access_token': 1234},
                                {'environment': 'production'}
                    },
                    {'log_format.default':'pyramid'},
                    {'log_format.patterns': 'celery*.log celery_process'},
                    {'min_log_level': 'INFO'}
        }

        new_processor = LogFileProcessor(scanner, app)
        #check if default_parser is a dict and has valid name
        self.assertEquals('pyramid', new_processor.default_parser['name'])

if __name__ == '__main__':
    unittest.main()
