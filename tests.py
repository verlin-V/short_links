from unittest import TestCase

from dotenv import load_dotenv

load_dotenv('env/test.env')

from utils import (
    hash_exists,
    add_short_link_to_database,
    conn,
    delete_link,
    get_link_by_hash,
)


def _run_sql(sql, fetch=False):
    with conn.cursor() as cur:
        cur.execute(sql)
        if fetch:
            return cur.fetchall()


class DBMethodsTestCase(TestCase):
    SQL_FORMAT_ADD_SHORT_LINK = '''
        INSERT INTO short_link (link, hash)
        VALUES ('{}', '{}')
    '''
    SQL_FORMAT_RETRIEVE_LINK = '''
        SELECT * FROM short_link WHERE hash = '{}'
    '''
    SQL_FORMAT_DELETE = '''
        DELETE FROM short_link
        WHERE hash = '{}'
    '''
    SQL_FORMAT_COUNT_OF_LINKS_WITH_SPECIFIC_HASH = '''
        SELECT COUNT(*) FROM short_link
        WHERE hash = '{}'
    '''

    def tearDown(self):
        _run_sql('DELETE FROM short_link')

    def test_hash_exists_return_true_for_existing_hash(self):
        hash_val = 'aaaaaaaa'
        link_val = 'some_link_here'
        _run_sql(self.SQL_FORMAT_ADD_SHORT_LINK.format(link_val, hash_val))
        self.assertEqual(hash_exists(hash_val), True)

    def test_hash_exists_return_false_for_not_existing_hash(self):
        self.assertEqual(hash_exists('xxxxxxxx'), False)

    def test_add_short_link_adds_link(self):
        hash_val = 'aaaaaaaa'
        link_val = 'some_link_here'
        count_of_specific_links = _run_sql(
            self.SQL_FORMAT_COUNT_OF_LINKS_WITH_SPECIFIC_HASH.format(hash_val),
            True
        )[0][0]

        add_short_link_to_database(link_val, hash_val)

        count_of_specific_links_upd = _run_sql(
            self.SQL_FORMAT_COUNT_OF_LINKS_WITH_SPECIFIC_HASH.format(hash_val),
            True
        )[0][0]
        self.assertEqual(
            count_of_specific_links + 1,
            count_of_specific_links_upd
        )

    def test_delete_link_deletes_specific_link(self):
        hash_val = 'aaaaaaaa'
        link_val = 'some_link_here'
        _run_sql(self.SQL_FORMAT_ADD_SHORT_LINK.format(link_val, hash_val))
        link_before_delete = _run_sql(
            self.SQL_FORMAT_RETRIEVE_LINK.format(hash_val),
            True
        )

        delete_link(hash_val)

        self.assertTrue(link_before_delete)
        self.assertFalse(_run_sql(
            self.SQL_FORMAT_RETRIEVE_LINK.format(hash_val),
            True
        ))

    def test_get_link_by_hash_returns_specific_link(self):
        hash_val = 'aaaaaaaa'
        link_val = 'some_link_here'
        _run_sql(self.SQL_FORMAT_ADD_SHORT_LINK.format(link_val, hash_val))
        sql_code = f"SELECT link FROM short_link WHERE hash = '{hash_val}'"

        self.assertEqual(
            _run_sql(sql_code, True)[0][0],
            get_link_by_hash(hash_val)
        )