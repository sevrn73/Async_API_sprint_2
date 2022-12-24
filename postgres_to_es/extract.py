from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from backoff import backoff


class PSExtract:
    LIMIT_ROWS = 100

    def __init__(self, pg_conn: _connection, curs: DictCursor, offset: int, model_name: str) -> None:
        self.pg_conn = pg_conn
        self.curs = curs
        self.offset = offset
        self.model_name = model_name

    @staticmethod
    @backoff()
    def extract(query: str, curs: DictCursor):
        """
        Метод загрузки данных из Postgres

        Parameters
        ----------
        :param query: запрос к БД
        :param curs: курсор Postgres
        ----------
        """
        curs.execute(query)
        data = curs.fetchall()
        return data

    def extract_data(self, last_modified: str, iter_model_name: str):
        if self.model_name == "movies":
            return self.extract_filmwork_data(last_modified, iter_model_name)
        elif self.model_name == "persons":
            return self.extract_person_data(last_modified)
        elif self.model_name == "genres":
            return self.extract_genre_data(last_modified)

    def extract_filmwork_data(self, last_modified: str, iter_model_name: str) -> list:
        if iter_model_name == "film_work":
            where = f"WHERE fw.modified > '{last_modified}' "
        elif iter_model_name == "person":
            where = f"WHERE p.modified > '{last_modified}' "
        elif iter_model_name == "genre":
            where = f"WHERE g.modified > '{last_modified}' "
        query = (
            "SELECT fw.id as fw_id, fw.title, fw.description, "
            "fw.rating, fw.type, fw.created, fw.modified, "
            "COALESCE ( \
                json_agg( \
                    DISTINCT jsonb_build_object( \
                        'person_id', p.id, \
                        'role', pfw.role, \
                        'full_name', p.full_name \
                    ) \
                ) FILTER (WHERE p.id is not null), \
                '[]' \
            ) as persons, "
            "array_agg(DISTINCT g.name) as genres "
            "FROM content.film_work fw "
            "LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id "
            "LEFT JOIN content.person p ON p.id = pfw.person_id "
            "LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id "
            "LEFT JOIN content.genre g ON g.id = gfw.genre_id "
            f"{where}"
            "GROUP BY fw.id "
            "ORDER BY modified "
            f"LIMIT {self.LIMIT_ROWS} OFFSET {self.offset};"
        )
        data = self.extract(query, self.curs)

        return data

    def extract_person_data(self, last_modified: str) -> list:
        where = f"WHERE p.modified > '{last_modified}' "
        query = (
            "SELECT p.id , p.full_name as name "
            "FROM content.person p "
            f"{where}"
            "GROUP BY p.id "
            "ORDER BY modified "
            f"LIMIT {self.LIMIT_ROWS} OFFSET {self.offset};"
        )
        data = self.extract(query, self.curs)
        return data

    def extract_genre_data(self, last_modified: str) -> list:
        where = f"WHERE g.modified > '{last_modified}' "
        query = (
            "SELECT g.id, g.name as genre, g.description "
            "FROM content.genre g "
            f"{where}"
            "GROUP BY g.id "
            "ORDER BY modified "
            f"LIMIT {self.LIMIT_ROWS} OFFSET {self.offset};"
        )
        data = self.extract(query, self.curs)

        return data
