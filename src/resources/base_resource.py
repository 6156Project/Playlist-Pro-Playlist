from abc import ABC, abstractmethod


class BaseResource(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_full_collection_name(self):
        pass

    @abstractmethod
    def get_data_service(self):
        pass

    @abstractmethod
    def get_resource_by_id(self, id):
        pass

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        """

        :param relative_path: path to resource
        :param path_parameters: path parameters to identify the resource instance
        :param template: dict for where clause
        :param field_list: fields to return
        :param limit:
        :param offset:
        :param order_by:
        :return:
        """
        final_path_parameters = {} if path_parameters is None else path_parameters
        final_template = {} if template is None else template
        full_template = {**final_path_parameters, **final_template}

        d_service = self.get_data_service()
        result = d_service.get_by_template(
            self.get_full_collection_name(),
            full_template,
            field_list
        )

        return result

    def create_resource(self, resource_data):
        d_service = self.get_data_service()
        return d_service.create_resource(self.get_full_collection_name(), resource_data)

    def delete_resource(self, template):
        d_service = self.get_data_service()
        return d_service.delete_resource(self.get_full_collection_name(), template)

    def update_resource(self, values, template):
        d_service = self.get_data_service()
        return d_service.update_resource(self.get_full_collection_name(), values, template)

    def get_resource_columns(self):
        d_service = self.get_data_service()
        return d_service.list_columns(self.config.collection_name)