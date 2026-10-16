from unittest import TestCase, mock
from gitmostwanted.lib.bigquery.job import Job
from gitmostwanted.lib.bigquery.result import ResultJob


class LibBigQueryResultTestCase(TestCase):
    def setUp(self):
        pass

    def test_convert_incoming_obj(self):
        result = ResultJob(self.response_example())

        self.assertEqual(len(result), 2)
        self.assertEqual(next(result), ['29028775', 'facebook/react-native', '225'])
        self.assertEqual(next(result), ['29028776', 'facebook/react-native2', '226'])
        self.assertRaises(StopIteration, next, result)

    def test_convert_incoming_empty_obj(self):
        result = ResultJob(self.response_example_empty())

        self.assertEqual(len(result), 0)
        self.assertRaises(StopIteration, next, result)

    def response_example_empty(self):
        data = self.response_example()
        data['rows'] = []
        data['totalRows'] = 0
        return data

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
                },
                {
                    'f': [
                        {'v': '29028776'},
                        {'v': 'facebook/react-native2'},
                        {'v': '226'}
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
            'totalRows': '2'
        }


class LibBigQueryJobTestCase(TestCase):
    def test_job_insert_payload(self):
        mock_api = mock.MagicMock()
        mock_api.project_id = 'test-project'
        mock_jobs = mock.MagicMock()
        mock_api.jobs.return_value = mock_jobs
        mock_jobs.insert.return_value.execute.return_value = {
            'jobReference': {'jobId': 'job_123'}
        }

        job = Job(mock_api, 'SELECT 1')
        job_id = job.execute()

        self.assertEqual(job_id, 'job_123')
        mock_jobs.insert.assert_called_once()
        _, kwargs = mock_jobs.insert.call_args
        body = kwargs['body']
        self.assertIn('jobId', body['jobReference'])
        self.assertNotIn('job_id', body['jobReference'])

