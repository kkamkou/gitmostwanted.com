from unittest import TestCase
from gitmostwanted.bigquery.result import Result


class BigQueryResultTestCase(TestCase):
    def setUp(self):
        self.result = Result(self.response_example())

    def test_convert_incoming_obj(self):
        self.assertEquals(len(self.result), 1)
        self.assertEquals(
            next(self.result),
            ['29028775', 'facebook/react-native', '225']
        )
        self.assertRaises(StopIteration, next, self.result)

    def response_example(self):
        return {
            'cacheHit': False,
            'jobComplete': True,
            'jobReference': {
                'jobId': 'job_123-4567',
                'projectId': 'my-project-1234567890'
            },
            'kind': 'bigquery#queryResponse',
            'rows': [
                {
                    'f': [
                        {'v': '29028775'},
                        {'v': 'facebook/react-native'},
                        {'v': '225'}
                    ]
                }
            ],
            'schema': {
                'fields': [
                    {
                        'mode': 'NULLABLE',
                        'name': 'repo_id',
                        'type': 'INTEGER'
                    },
                    {
                        'mode': 'NULLABLE',
                        'name': 'repo_name',
                        'type': 'STRING'
                    },
                    {
                        'mode': 'NULLABLE',
                        'name': 'cnt',
                        'type': 'INTEGER'
                    }
                ]
            },
            'totalBytesProcessed': '5568164',
            'totalRows': '1'
        }
