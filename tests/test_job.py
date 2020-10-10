from unittest import TestCase, main
from unittest.mock import Mock, patch
from qtcurate.exceptions import *
from qtcurate.job import Job
from qtcurate.utilities import json_to_tuple


class TestJob(TestCase):

    # Test get_id method
    def test_get_id(self):
        job = Job()
        self.assertEqual(job.get_id(), str(None))

    # Test set_description method
    def test_set_description_arg_err(self):
        job = Job()
        some_title = 123
        with self.assertRaises(QtArgumentError):
            job.set_description(some_title)

    def test_set_description(self):
        job = Job()
        some_title = 'some description'
        job.set_description(some_title)
        self.assertEqual(job.temp_dict["title"], some_title)

    # Test with_documents method
    def test_with_documents(self):
        list_files = ["file1", "file2"]
        job = Job()
        job.with_documents(list_files)
        self.assertEqual(list_files, job.temp_dict['files'])

    def test_with_documents_arg_error(self):
        list_files = "string"
        job = Job()
        with self.assertRaises(QtArgumentError):
            job.with_documents(list_files)

    # Test with_model method
    def test_with_model_arg_err(self):
        job = Job()
        some_id = 123
        with self.assertRaises(QtArgumentError):
            job.with_model(some_id)

    def test_with_model(self):
        job = Job()
        some_id = "some id"
        job.with_model(some_id)
        self.assertEqual(job.model_id, some_id)

    # Test create method
    def test_create_no_description(self):
        job = Job()
        with self.assertRaises(QtJobError):
            job.create()

    def test_create_no_document(self):
        job = Job()
        some_description = "some description"
        job.set_description(some_description)
        with self.assertRaises(QtJobError):
            job.create()

    @patch("qtcurate.job.connect")
    def test_create(self, con):
        job = Job()
        some_json = {"id": "value"}
        some_list = ['file1', 'file2']
        some_title = "some title"
        job.set_description(some_title)
        job.with_documents(some_list)
        response = Mock()
        response.json.return_value = some_json
        con.return_value = response
        res = job.create()
        self.assertEqual(res, json_to_tuple(some_json))

    # Test fetch method
    def test_fetch_arg_err(self):
        some_id = 123
        job = Job()
        with self.assertRaises(QtArgumentError):
            job.fetch(some_id)

    @patch("qtcurate.job.connect")
    def test_fetch(self, con):
        job = Job()
        some_json = {"id": "value"}
        some_id = 'some id'
        response = Mock()
        response.json.return_value = some_json
        con.return_value = response
        res = job.fetch(some_id)
        self.assertEqual(res, json_to_tuple(some_json))

    # Test delete method
    def test_delete_arg_err(self):
        some_id = 123
        job = Job()
        with self.assertRaises(QtArgumentError):
            job.delete(some_id)

    @patch("qtcurate.job.connect")
    def test_delete(self, con):
        job = Job()
        some_id = 'some id'
        response = Mock()
        response.ok = True
        con.return_value = response
        res = job.delete(some_id)
        self.assertEqual(res, True)

    # Test progress method
    def test_progress_argument_type_error(self):
        job = Job()
        some_id = 123
        with self.assertRaises(QtArgumentError):
            job.progress(some_id)

    @patch("qtcurate.job.connect")
    def test_progress(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        job = Job()
        response = Mock()
        response.json.return_value = some_dict
        con.return_value = response
        res = job.progress(some_id)
        self.assertEqual(res, json_to_tuple(some_dict))


if __name__ == '__main__':
    main()
