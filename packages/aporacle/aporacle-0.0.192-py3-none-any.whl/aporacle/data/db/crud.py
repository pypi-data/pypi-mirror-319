from komoutils.db.mongodb_reader_writer import MongoDBReaderWriter


class Crud(MongoDBReaderWriter):
    def __init__(self, uri: str, db_name: str):
        super().__init__(uri, db_name)

    def write_to_database(self, collection=None, data=None):
        assert collection is not None, "Collection cannot be None"
        assert data is not None, "Data cannot be None"
        assert len(data) > 0, "Data cannot be empty."
        return self.write(collection=collection, data=data)

    def read_from_data(self, collection=None, filters=None, omit=None, limit: int = 1000000, sort_key='_id', sort_order=-1):
        assert collection is not None, "Collection cannot be None"
        return self.read(collection=collection, filters=filters, omit=omit, limit=limit, sort_key=sort_key, sort_order=sort_order)


