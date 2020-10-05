import os
from unittest import TestCase, main
from unittest.mock import Mock, patch
from qtcurate.document import Document
from qtcurate.exceptions import *


class TestDocument(TestCase):

    # Test set_id method
    def test_set_id(self):
        doc = Document()
        some_id = '123'
        doc.set_id(some_id)
        self.assertEqual(doc.id, some_id)

    # Test get_id method
    def test_get_id(self):
        doc = Document()
        self.assertEqual(doc.get_id(), None)

    # Test create method
    def test_create_arg_err(self):
        doc = Document()
        file = [1, 2, 3]
        with self.assertRaises(QtArgumentError):
            doc.create(file)

    @patch("qtcurate.document.connect")
    def test_create(self, con):
        doc = Document()
        some_json = {"uuid": "value"}
        some_file = "test.txt"
        with open(some_file, "w") as f:
            f.write("Delete me!")
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_json
        con.return_value = response
        res = doc.create(some_file)
        self.assertEqual(res, some_json["uuid"])
        os.remove(some_file)


if __name__ == '__main__':
    main()
