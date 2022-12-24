import time
from contextlib import closing
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from state import JsonFileStorage, State
from etl_process import EtlProcessFilms, EtlProcessGenres, EtlProcessPersons
from logger import logger
from config import DbSettings, ElasticSettings

load_dotenv()


def main(ps_connect: dict, es_connect: dict):
    """
    Функция запуска внутренних компонентов ETL
    """
    while True:
        try:
            with closing(
                psycopg2.connect(**ps_connect, cursor_factory=DictCursor)
            ) as pg_conn, pg_conn.cursor() as curs:
                for model_name in ["movies", "persons", "genres"]:
                    storage = JsonFileStorage(f"{model_name}.json")
                    state = State(storage)

                    if model_name == "movies":
                        etl_process = EtlProcessFilms()
                        etl_process.start(pg_conn, curs, es_connect, state, model_name)
                    elif model_name == "persons":
                        etl_process = EtlProcessPersons()
                        etl_process.start(pg_conn, curs, es_connect, state, model_name)
                    elif model_name == "genres":
                        etl_process = EtlProcessGenres()
                        etl_process.start(pg_conn, curs, es_connect, state, model_name)

        except psycopg2.OperationalError:
            logger.error("Error connecting to Postgres database")

        time.sleep(1)


if __name__ == "__main__":
    ps_connect = DbSettings().dict()
    es_connect = ElasticSettings().dict()
    main(ps_connect, es_connect)
