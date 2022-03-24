from dotenv import load_dotenv

load_dotenv('env/.env')

from utils import delete_expired_links

if __name__ == '__main__':
    delete_expired_links()
