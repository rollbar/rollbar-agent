import unittest
import imp

rollbar_agent = imp.load_source('rollbar-agent', './rollbar-agent')


class FakeScanner:
    def __init__(self, config):
        self.config = config


class TestDefaultMessageStartParserUsage(unittest.TestCase):
    app = {'name': 'pyramid',
           'config': {
               'log_format.default': 'pyramid',
               'log_format.patterns': 'celery*.log celery_process',
               'min_log_level': 'INFO'
           }
           }

    def test_process_log_debug_with_format_name(self):
        # check if default_parser uses valid format name provided in the config
        config = {'_formats': {'pyramid': {'name': 'pyramid'}}
                  }
        scanner = FakeScanner(config)

        new_processor = rollbar_agent.LogFileProcessor(scanner, self.app)

        self.assertEqual('pyramid', new_processor.default_parser['name'])

    def test_process_log_debug_without_format_name(self):
        # check if default_parser can access _default_message_start_parser if format name not provided in the config
        config = {'_formats': {}}
        scanner = FakeScanner(config)

        new_processor = rollbar_agent.LogFileProcessor(scanner, self.app)

        self.assertEqual('default parser', new_processor.default_parser['name'])


if __name__ == '__main__':
    unittest.main()
