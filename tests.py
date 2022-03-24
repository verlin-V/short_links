from datetime import datetime, timedelta
from unittest import TestCase

from dotenv import load_dotenv

load_dotenv('env/test.env')

from utils import (
    hash_exists,
    add_short_link_to_database,
    conn,
    delete_link,
    get_link_by_hash,
    delete_expired_links,
)


def _run_sql(sql, fetch=False):
    with conn.cursor() as cur:
        cur.execute(sql)
        if fetch:
            return cur.fetchall()


class DBMethodsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expired = datetime.now() + timedelta(days=3)
        cls.hash_val = 'aaaaaaaa'
        cls.link_val = 'some_link_here'

    SQL_FORMAT_ADD_SHORT_LINK = '''
        INSERT INTO short_link (link, hash, expired)
        VALUES ('{}', '{}', '{}')
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
        WHERE hash = '{}' and expired = '{}'
    '''

    def tearDown(self):
        _run_sql('DELETE FROM short_link')

    def test_hash_exists_return_true_for_existing_hash(self):
        _run_sql(
            self.SQL_FORMAT_ADD_SHORT_LINK.format(
                self.link_val, self.hash_val, self.expired
            )
        )
        self.assertEqual(hash_exists(self.hash_val), True)

    def test_hash_exists_return_false_for_not_existing_hash(self):
        self.assertEqual(hash_exists('xxxxxxxx'), False)

    def test_add_short_link_adds_link(self):
        count_of_specific_links = _run_sql(
            self.SQL_FORMAT_COUNT_OF_LINKS_WITH_SPECIFIC_HASH.format(
                self.hash_val, self.expired),
            True
        )[0][0]

        add_short_link_to_database(self.link_val, self.hash_val, self.expired)

        count_of_specific_links_upd = _run_sql(
            self.SQL_FORMAT_COUNT_OF_LINKS_WITH_SPECIFIC_HASH.format(
                self.hash_val, self.expired
            ),
            True
        )[0][0]
        self.assertEqual(
            count_of_specific_links + 1,
            count_of_specific_links_upd
        )

    def test_delete_link_deletes_specific_link(self):
        _run_sql(
            self.SQL_FORMAT_ADD_SHORT_LINK.format(
                self.link_val, self.hash_val, self.expired
            )
        )
        link_before_delete = _run_sql(
            self.SQL_FORMAT_RETRIEVE_LINK.format(self.hash_val),
            True
        )

        delete_link(self.hash_val)

        self.assertTrue(link_before_delete)
        self.assertFalse(_run_sql(
            self.SQL_FORMAT_RETRIEVE_LINK.format(self.hash_val),
            True
        ))

    def test_get_link_by_hash_returns_specific_link(self):
        _run_sql(
            self.SQL_FORMAT_ADD_SHORT_LINK.format(
                self.link_val, self.hash_val, self.expired
            )
        )
        sql_code = f"SELECT link FROM short_link WHERE hash = '{self.hash_val}'"

        self.assertEqual(
            _run_sql(sql_code, True)[0][0],
            get_link_by_hash(self.hash_val)
        )

    def test_delete_expired_links_deletes_expired_link(self):
        hash1 = '00000000'
        hash2 = '00000001'
        _run_sql(
            self.SQL_FORMAT_ADD_SHORT_LINK.format(
                self.link_val, hash1, datetime.now() + timedelta(days=2)
            )
        )
        _run_sql(
            self.SQL_FORMAT_ADD_SHORT_LINK.format(
                self.link_val, hash2, datetime.now() - timedelta(seconds=1)
            )
        )
        delete_expired_links()

        self.assertTrue(
            _run_sql(self.SQL_FORMAT_RETRIEVE_LINK.format(hash1), True)
        )
        self.assertFalse(
            _run_sql(self.SQL_FORMAT_RETRIEVE_LINK.format(hash2), True)
        )