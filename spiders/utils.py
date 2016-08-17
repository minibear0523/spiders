# encoding=utf-8
from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
def get_update_time():
    update_date = datetime.now()
    return update_date.strftime(DATE_FORMAT)


def form_index_settings(shards=10, replicas=0):
    settings = {
        'index': {
            'number_of_shards': shards,
            'number_of_replicas': replicas,
            'analysis': {
                'analyzer': {
                    'default': {
                        'filter': ['stemmer'],
                        'type': 'custom',
                        'tokenizer': 'ik_smart'
                    }
                }
            }
        }
    }

    return settings