import os
import psycopg2

conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['DB_DATABASE'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
)
conn.autocommit = True


def hash_exists(hash_url):
    with conn.cursor() as cur:
        cur.execute(f'''
           SELECT EXISTS(
               SELECT 1 FROM short_link
               WHERE hash = '{hash_url}'
           )
        ''')
        return cur.fetchone()[0]


def add_short_link(link, hash_url):
    with conn.cursor() as cur:
        cur.execute(
            f'''
           INSERT INTO short_link (link, hash)
           VALUES ('{link}', '{hash_url}')
           '''
        )


def delete_link(hash_url):
    with conn.cursor() as cur:
        cur.execute(
            f'''
            DELETE FROM short_link
            WHERE hash = '{hash_url}'
            '''
        )


def get_link_by_hash(hash_url):
    with conn.cursor() as cur:
        cur.execute(
            f'''
            SELECT link FROM short_link
            WHERE hash = '{hash_url}'
            '''
        )
        return cur.fetchone()[0]
