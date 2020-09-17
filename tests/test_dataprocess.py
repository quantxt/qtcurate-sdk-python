from unittest import TestCase
from qtcurate.dataprocess import DataProcess
from qtcurate.exceptions import *
from qtcurate.extractor import ChunkMode, SearchMode, Type, AnalyzeMode, Extractor

API_KEY = 'a5334f7d-2aac-44b3-aefc-a25cd9dd7bec'


class TestDataProcess(TestCase):

    def test_get_id(self):
        some_id = None
        dataprocess = DataProcess()
        self.assertEqual(dataprocess.get_id(), str(some_id))

    def test_set_id(self):
        dataprocess = DataProcess()
        dataprocess.set_id('some id')
        self.assertEqual(dataprocess.get_id(), 'some id')

    def test_set_id_arg_not_str(self):
        dataprocess = DataProcess()
        dataprocess.set_id([123])
        self.assertEqual(dataprocess.get_id(), str([123]))

    def test_set_chunk(self):
        dataprocess = DataProcess()
        chunk = ChunkMode.NONE
        dataprocess.set_chunk(chunk)
        self.assertEqual(dataprocess.temp_dict["chunk"], chunk.value)

    def test_get_uuid(self):
        dataprocess = DataProcess()
        some_uuid = None
        self.assertEqual(dataprocess.get_uuid(), str(some_uuid))

    def test_title(self):
        title = "some title"
        dataprocess = DataProcess()
        dataprocess.set_description(title)
        self.assertEqual(title, dataprocess.temp_dict["title"])

    def test_title_arg_error(self):
        title = 12
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.set_description(title)


    def test_exclude_utt(self):
        value = True
        dataprocess = DataProcess()
        dataprocess.exclude_utt_without_entities(value)
        self.assertEqual(value, dataprocess.temp_dict["excludeUttWithoutEntities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.exclude_utt_without_entities(value)

    def test_set_workers_arg_err(self):
        value = '123'
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.set_workers(value)

    def test_set_workers(self):
        value = 123
        dataprocess = DataProcess()
        dataprocess.set_workers(value)
        self.assertEqual(dataprocess.temp_dict["numWorkers"], value)

    def test_files(self):
        list_files = ["file1", "file2"]
        dataprocess = DataProcess()
        dataprocess.with_documents(list_files)
        self.assertEqual(list_files, dataprocess.temp_dict['files'])

    def test_files_arg_error(self):
        list_files = "string"
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.with_documents(list_files)

    def test_create_empty_search_dict(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtDataProcessError):
            dataprocess.create()

    def test_fetch_dp_id_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.fetch(dp_id=[])

    def test_update_dp_id_arg_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.update(dp_id=[], update_files=["test.txt"])

    def test_update_list_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.update(dp_id="some_id", update_files="file")

    def test_clone_dp_id_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.clone(dp_id=[])

    def test_delete_argument_type_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.delete(dp_id=[])

    def test_progress_argument_type_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.progress(dp_id=[])

    def test_search_dp_id_arg(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id=123)

    def test_search_param_from_arg_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id="some_dp", param_from="123")

    def test_search_size_range_arg(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id="some_dp", param_from=5, size=201)

    def test_search_size_not_int_arg(self):
        dp_id = "test"
        param_from = 5
        size = "test"
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        dataprocess = DataProcess()
        f1 = "string"
        with self.assertRaises(QtArgumentError):
            dataprocess.search(index, param_from, size, f1)
