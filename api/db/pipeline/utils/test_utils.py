from pipeline.utils.filter import DataFilter
from pipeline.utils.paginate import Pagination
from pipeline.utils.cursor import Cursor


class Test_H2ogptUtils:
    def test_paginate(self):
        query = []  # type: ignore
        skip = 0
        limit = 10
        expected_result = [{"$skip": 0}, {"$limit": 10}]

        assert isinstance(Pagination().paginate(query, skip, limit), list)
        assert Pagination().paginate(query, skip, limit) == expected_result
        assert Pagination().paginate(query, skip, limit) is not None

    def test_cursor(self):
        import os

        assert isinstance(Cursor(), object)
        assert Cursor().port == int(os.getenv("MONGO_PORT", 0))
        assert Cursor().host == os.getenv("MONGO_HOST")
        assert Cursor().user == os.getenv("MONGO_USER")
        assert Cursor().passwd == os.getenv("MONGO_PASS")

    def test_filter(self):
        data = [
            {
                "lastUpdated": "2021-10-01",
                "id": "123",
                "patientNames": {
                    "family": "Doe",
                    "given": "John",
                },
                "age": 30,
            },
            {
                "lastUpdated": "2023-10-01",
                "id": "124",
                "patientNames": {
                    "family": "Dane",
                    "given": "Solomon",
                },
                "age": 21,
            },
        ]

        fields = ["id", "age"]
        conditions = ["123", "30"]

        res = DataFilter().filter(fields, conditions, data)

        assert isinstance(res, list)
        assert res[0]["id"] == "123"
        assert res[0]["age"] == 30
