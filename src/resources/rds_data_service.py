import pymysql
from resources.base_data_service import BaseDataService


class RDSDataService(BaseDataService):

    def __init__(self, config_info):
        super().__init__(config_info)

    def _get_connection(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                user=self.config_info.db_user,
                password=self.config_info.db_pw,
                host=self.config_info.db_host,
                port=int(self.config_info.db_port),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        return self.connection

    def _close_connection(self):
        if self.connection:
            self.connection.close()

    def _get_collection(self, collection_name):
        pass

    def get_by_template(self,
                        collection_name,
                        template=None,
                        field_list=None
                        ):
        select_cols = "*" if field_list is None else ','.join(field_list)

        # template = self.__clear_template(template)
        sql = "SELECT %s FROM %s" % (select_cols, collection_name)
        if template:
            sql += " WHERE " + self.__dict_to_sql(template, 'where')

        conn = self._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql)
        if res >= 1:
            result = cursor.fetchall()
        else:
            result = None

        return result

    def list_resources(self):
        pass

    def list_columns(self, collection_name):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {collection_name} LIMIT 1")
        return [i[0] for i in cursor.description]

    def create_resource(self, collection_name, resource_data):
        columns = ','.join(resource_data.keys())
        str_values = [str(i) for i in resource_data.values()]
        values = ','.join('"' + item + '"' for item in str_values)

        conn = self._get_connection()
        cursor = conn.cursor()
        result = {}
        try:
            res = cursor.execute(f"INSERT INTO {collection_name} ({columns}) VALUES ({values})")
        except pymysql.IntegrityError as e:
            result['text'] = "Resource already exists."
            result['status'] = 409
        except pymysql.OperationalError as e:
            result['text'] = repr(e)
            result['status'] = 409
        else:
            if res == 1:
                result['text'] = "Resource created."
                result['status'] = 201

        self.connection.commit()

        return result

    def delete_resource(self, collection_name, template):
        conn = self._get_connection()
        cursor = conn.cursor()
        result = {}
        res = cursor.execute(f"DELETE FROM {collection_name} WHERE {self.__dict_to_sql(template, 'where')}")
        if res == 1:
            result['text'] = "Resource deleted."
            result['status'] = 201
        else:
            result['text'] = "Resource not found"
            result['status'] = 404
        self.connection.commit()

        return result

    def update_resource(self, collection_name, values, template):
        conn = self._get_connection()
        cursor = conn.cursor()
        result = {}
        set_statement = self.__dict_to_sql(values, 'set')
        where_statement = self.__dict_to_sql(template, 'where')
        sql = f"UPDATE {collection_name} SET {set_statement} WHERE {where_statement}"
        res = cursor.execute(sql)
        if res == 1:
            result['text'] = "Resource updated."
            result['status'] = 201
        self.connection.commit()

        return result


    def __dict_to_sql(self, values, statement):
        """
        Helper function that converts a python dictionary to sql syntax,
        For set and where statements.
        :return: sql: string of dictionary key-value pairs.
        """
        sql_list = []
        for key, val in values.items(): 
                sql_list.append(f"{key}=\"{val}\"")
        if statement == 'where':
            sql = " AND ".join(sql_list)
        elif statement == 'set':
            sql = ", ".join(sql_list)

        return sql

    # def __clear_template(self, template):
    #     clean_template = { key : value for (key, value) in template if key in self.list_columns() }
    #     return clean_template