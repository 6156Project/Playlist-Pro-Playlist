import os
from resources.rds_data_service import RDSDataService
from resources.playlist_resource import PlaylistResource

# DATABASE CONFIGS
class RDSDataServiceConfig:
    def __init__(self, db_user, db_pw, db_host, db_port):
        self.db_user = db_user
        self.db_pw = db_pw
        self.db_host = db_host
        self.db_port = db_port


# RESOURCES CONFIGS
class PlaylistResourceConfig:
    def __init__(self, data_service, collection_name):
        self.data_service = data_service
        self.collection_name = collection_name

class ServiceFactory:
    def __init__(self):
        self.rds_svc_config = RDSDataServiceConfig(
            os.environ.get("RDS_USERNAME"),
            os.environ.get("RDS_PASSWORD"),
            os.environ.get("RDS_HOSTNAME"),
            os.environ.get("RDS_PORT")
        )
        self.rds_service = RDSDataService(self.rds_svc_config)
        # connect songs resource to rds
        self.playlists_service_config = PlaylistResourceConfig(self.rds_service, "Playlist.playlists")
        self.playlists_resource = PlaylistResource(self.playlists_service_config)

    def get(self, resource_name, default):
        if resource_name == "playlists":
            result = self.playlists_resource
        else:
            result = default
        return result
