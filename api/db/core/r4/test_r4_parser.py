import os
from core.r4.parser import init, drop_all


class Test_DBCore:
    def test_unpack_r4_parser(self):
        parser = init()
        assert parser is None, "Parser is None"

    def test_drop_collection_r4_parse(self):
        if "prod" in os.getenv("ENV", ""):
            print ("droppping everything as of nows")
            db = drop_all()
            assert db is None, "DB is None"
