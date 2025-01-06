import pytest

from rick_db.backend.sqlite import Sqlite3Connection, Sqlite3Manager

create_table = (
    "create table animal(id_animal integer primary key autoincrement, name varchar);"
)
create_index = "create index idx01 on animal(id_animal)"
create_view = "create view list_animals as select * from animal"


class TestManager:

    def test_tables(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        # no tables created yet
        tables = meta.tables()
        assert len(tables) == 0
        assert meta.table_exists("animal") is False

        # create one table
        with sqlite_conn.cursor() as qry:
            qry.exec(create_table)

        tables = meta.tables()
        assert len(tables) == 1
        assert tables[0] == "animal"
        assert meta.table_exists("animal") is True

        # cleanup
        meta.drop_table("animal")

    def test_schemas(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        schemas = meta.schemas()
        assert len(schemas) == 0

    def test_databases(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        dbs = meta.databases()
        assert len(dbs) == 0

    def test_views(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        # no views created yet
        views = meta.views()
        assert len(views) == 0
        assert meta.view_exists("list_animals") is False

        # create one table
        with sqlite_conn.cursor() as qry:
            qry.exec(create_table)
            qry.exec(create_view)

        views = meta.views()
        assert len(views) == 1
        assert views[0] == "list_animals"
        assert meta.view_exists("list_animals") is True

        # cleanup
        meta.drop_view("list_animals")
        meta.drop_table("animal")

    def test_table_fields(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        with sqlite_conn.cursor() as qry:
            qry.exec(create_table)
            qry.exec(create_view)

        # test table fields
        fields = meta.table_fields("animal")
        assert len(fields) == 2
        field1, field2 = fields
        assert field1.field == "id_animal"
        assert field1.primary is True
        assert field2.field == "name"
        assert field2.primary is False

        # test view fields
        fields = meta.view_fields("list_animals")
        assert len(fields) == 2
        field1, field2 = fields
        assert field1.field == "id_animal"
        assert field1.primary is False  # views don't have keys
        assert field2.field == "name"
        assert field2.primary is False

        meta.drop_view("list_animals")
        meta.drop_table("animals")

    def test_table_keys(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        # create one table
        with sqlite_conn.cursor() as qry:
            qry.exec(create_table)
            qry.exec(create_index)
            qry.exec(create_view)

        # create table
        tables = meta.tables()
        assert len(tables) == 1
        assert tables[0] == "animal"
        assert meta.table_exists("animal") is True

        keys = meta.table_indexes("animal")
        assert len(keys) == 1
        assert keys[0].field == "id_animal"
        assert keys[0].primary is True

        pk = meta.table_pk("animal")
        assert pk.field == keys[0].field
        assert pk.primary == keys[0].primary
        assert pk.type == keys[0].type

        # cleanup
        meta.drop_table("animal")

    def test_users(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        assert len(meta.users()) == 0

    def test_user_groups(self, sqlite_conn: Sqlite3Connection):
        meta = Sqlite3Manager(sqlite_conn)
        assert len(meta.user_groups("someuser")) == 0
