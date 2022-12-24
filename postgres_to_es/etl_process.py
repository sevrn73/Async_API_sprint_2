from datetime import datetime
from extract import PSExtract
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from transform import *
from load import ESLoad
from state import State


class EtlProcess:
    ITER_MODEL_NAMES = ["film_work", "person", "genre"]

    def init_process(
        self, pg_conn: _connection, curs: DictCursor, es_connect: dict, state: State, model_name: str
    ) -> tuple:
        last_modified = state.get_state("last_modified")
        offset = state.get_state("offset")
        postgres_extractor = PSExtract(pg_conn, curs, offset, model_name)
        es_loader = ESLoad(**es_connect, model_name=model_name)
        return last_modified, postgres_extractor, es_loader

    def start(self, pg_conn: _connection, curs: DictCursor, es_connect: dict, state: State, model_name: str) -> None:
        last_modified, postgres_extractor, es_loader = self.init_process(pg_conn, curs, es_connect, state, model_name)
        self.check_and_update(last_modified, postgres_extractor, es_loader, state, model_name)

    def check_and_update(
        self, last_modified, postgres_extractor, es_loader, state: State, iter_model_name: str
    ) -> None:
        while True:
            data = postgres_extractor.extract_data(last_modified, iter_model_name)
            if data:
                transformed_data = self.transform_data(data)
                es_loader.send_data(transformed_data)

                postgres_extractor.offset += len(data)
                state.set_state("offset", postgres_extractor.offset)
                state.set_state(
                    "last_modified",
                    data[-1]["modified"].strftime("%Y-%m-%d")
                    if "modified" in data[-1]
                    else datetime.now().strftime("%Y-%m-%d"),
                )
            else:
                postgres_extractor.offset = 0
                state.set_state("offset", 0)
                break

    @staticmethod
    def transform_data(self, data):
        pass


class EtlProcessFilms(EtlProcess):
    def start(self, pg_conn: _connection, curs: DictCursor, es_connect: dict, state: State, model_name: str) -> None:
        last_modified, postgres_extractor, es_loader = self.init_process(pg_conn, curs, es_connect, state, model_name)
        for iter_model_name in EtlProcess.ITER_MODEL_NAMES:
            self.check_and_update(last_modified, postgres_extractor, es_loader, state, iter_model_name)

    def transform_data(self, data) -> list:
        return [parse_from_postgres_to_es(_) for _ in data]


class EtlProcessPersons(EtlProcess):
    def transform_data(self, data) -> list:
        return [parse_persons_postgres_to_es(_) for _ in data]


class EtlProcessGenres(EtlProcess):
    def transform_data(self, data) -> list:
        return [parse_genres_postgres_to_es(_) for _ in data]
