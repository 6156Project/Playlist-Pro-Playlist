from resources.base_resource import BaseResource
import uuid


class PlaylistResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = None
        self.columns = ['name']

    def get_full_collection_name(self):
        return self.config.collection_name

    def get_data_service(self):
        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, id):
        template = {'id': id}
        response = self.get_by_template(template=template)
        if response['status'] == 200:
            response['links'] = [
                    {
                        "href": f"api/playlists/{id}",
                        "rel": "self",
                        "type" : "PUT"
                    },{
                        "href": f"api/playlists/{id}",
                        "rel": "self",
                        "type" : "DELETE"
                    }
                    ]
        return response

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        rsp = super().get_by_template(relative_path, path_parameters, template, field_list,
                                         limit, offset, order_by)
        if rsp:
            response['status'] = 200
            response['text'] = 'OK'
            response['body'] = rsp
        else:
            response['status'] = 404
            response['text'] = 'Resource not found.'
        return response

    def create_resource(self, resource_data):
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        if not resource_data:
            response['status'] = 400
            response['text'] = 'Empty data'
        elif not all(columns in resource_data for columns in self.columns):
            response['status'] = 400
            response['text'] = 'Missing data required'
        else:
            data = {
                'id': uuid.uuid4().int,
                'name': resource_data['name']
                }
            rsp = super().create_resource(data)
            if rsp['status'] == 201:
                response['status'] = rsp['status']
                response['text'] = 'Resource created.' 
                response['body'] = {'id': data['id']}
                response['links'] = [
                    {
                        "href": f"api/playlists/{data['id']}",
                        "rel": "self",
                        "type" : "GET"
                    },{
                        "href": f"api/playlists/{data['id']}",
                        "rel": "self",
                        "type" : "PUT"
                    },{
                        "href": f"api/playlists/{data['id']}",
                        "rel": "self",
                        "type" : "DELETE"
                    }
                    ]
        return response

    def delete_resource(self, resource_data):
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        data = {'id': resource_data}
        response = super().delete_resource(data)
        return response

    def update_resource(self, id, resource_data):
        template = {'id': id}

        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        if not resource_data or 'name' not in resource_data:
            response['status'] = 400
            response['text'] = 'Missing data required'
        else:
            rsp = super().update_resource(resource_data, template)
            if rsp['status'] == 201:
                response['status'] = rsp['status']
                response['text'] = 'Resource updated.' 
                response['body'] = {
                    'id': template['id'],
                    'playlist_name': resource_data['name']
                    }
                response['links'] = [
                    {
                        "href": f"api/playlists/{template['id']}",
                        "rel": "self",
                        "type" : "GET"
                    },{
                        "href": f"api/playlists/{template['id']}",
                        "rel": "self",
                        "type" : "DELETE"
                    }
                    ]

        return response