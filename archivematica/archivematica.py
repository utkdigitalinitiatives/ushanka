import requests
import os
from dotenv import load_dotenv


class PackageRequest:
    def __init__(self, username, api_key, uri="https://localhost:8001/api/v2"):
        self.uri = uri
        self.username = username
        self.api_key = api_key

    def get_all_packages(self):
        """Get all packages from Archivematica.

        Returns:
            dict: The results of the request as a dict.

        Examples:
            >>> PackageRequest("test", "my_api_key").get_all_packages()
            {'meta': {'limit': 20, 'next': None, 'offset': 0, 'previous': None, 'total_count': 4}, 'objects': [{'current_full_path': '/gwork/archivematica/AIPsStore/2aaa/349a/12a2/4338/90d1/5097/bb98/9acc/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z', 'current_location': '/api/v2/location/65da3b00-f1ff-4e7b-b56c-abaf894ce9b4/', 'current_path': '2aaa/349a/12a2/4338/90d1/5097/bb98/9acc/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z', 'encrypted': False, 'misc_attributes': {}, 'origin_pipeline': '/api/v2/pipeline/21c132a8-9106-42a3-9046-0b6e12aaf141/', 'package_type': 'AIP', 'related_packages': ['/api/v2/file/dea5c7af-2321-4102-be4b-93b3866c9c84/'], 'replicas': [], 'replicated_package': None, 'resource_uri': '/api/v2/file/2aaa349a-12a2-4338-90d1-5097bb989acc/', 'size': 81143107, 'status': 'UPLOADED', 'uuid': '2aaa349a-12a2-4338-90d1-5097bb989acc'}, {'current_full_path': '/gwork/archivematica/DIPsStore/dea5/c7af/2321/4102/be4b/93b3/866c/9c84/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc', 'current_location': '/api/v2/location/e972dc35-7733-42c2-be1f-989a30c25f89/', 'current_path': 'dea5/c7af/2321/4102/be4b/93b3/866c/9c84/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc', 'encrypted': False, 'misc_attributes': {}, 'origin_pipeline': '/api/v2/pipeline/21c132a8-9106-42a3-9046-0b6e12aaf141/', 'package_type': 'DIP', 'related_packages': ['/api/v2/file/2aaa349a-12a2-4338-90d1-5097bb989acc/'], 'replicas': [], 'replicated_package': None, 'resource_uri': '/api/v2/file/dea5c7af-2321-4102-be4b-93b3866c9c84/', 'size': 32584789, 'status': 'UPLOADED', 'uuid': 'dea5c7af-2321-4102-be4b-93b3866c9c84'}, {'current_full_path': '/gwork/archivematica/AIPsStore/5cf2/ab4b/27d7/475d/aec5/5993/bcca/bee1/ChroniclingCOVID-19-20210304T183735Z-001-5cf2ab4b-27d7-475d-aec5-5993bccabee1.7z', 'current_location': '/api/v2/location/65da3b00-f1ff-4e7b-b56c-abaf894ce9b4/', 'current_path': '5cf2/ab4b/27d7/475d/aec5/5993/bcca/bee1/ChroniclingCOVID-19-20210304T183735Z-001-5cf2ab4b-27d7-475d-aec5-5993bccabee1.7z', 'encrypted': False, 'misc_attributes': {}, 'origin_pipeline': '/api/v2/pipeline/21c132a8-9106-42a3-9046-0b6e12aaf141/', 'package_type': 'AIP', 'related_packages': ['/api/v2/file/2b52c29b-2bec-4c69-925c-8cd0567df3fa/'], 'replicas': [], 'replicated_package': None, 'resource_uri': '/api/v2/file/5cf2ab4b-27d7-475d-aec5-5993bccabee1/', 'size': 81142978, 'status': 'UPLOADED', 'uuid': '5cf2ab4b-27d7-475d-aec5-5993bccabee1'}, {'current_full_path': '/gwork/archivematica/DIPsStore/2b52/c29b/2bec/4c69/925c/8cd0/567d/f3fa/ChroniclingCOVID-19-20210304T183735Z-001-5cf2ab4b-27d7-475d-aec5-5993bccabee1', 'current_location': '/api/v2/location/e972dc35-7733-42c2-be1f-989a30c25f89/', 'current_path': '2b52/c29b/2bec/4c69/925c/8cd0/567d/f3fa/ChroniclingCOVID-19-20210304T183735Z-001-5cf2ab4b-27d7-475d-aec5-5993bccabee1', 'encrypted': False, 'misc_attributes': {}, 'origin_pipeline': '/api/v2/pipeline/21c132a8-9106-42a3-9046-0b6e12aaf141/', 'package_type': 'DIP', 'related_packages': ['/api/v2/file/5cf2ab4b-27d7-475d-aec5-5993bccabee1/'], 'replicas': [], 'replicated_package': None, 'resource_uri': '/api/v2/file/2b52c29b-2bec-4c69-925c-8cd0567df3fa/', 'size': 32589480, 'status': 'UPLOADED', 'uuid': '2b52c29b-2bec-4c69-925c-8cd0567df3fa'}]}

        """
        r = requests.get(
            f"{self.uri}/file/?username={self.username}&api_key={self.api_key}"
        )
        return r.json()


if __name__ == "__main__":
    load_dotenv()
    print(
        PackageRequest(
            username=os.getenv("username"),
            api_key=os.getenv("key"),
            uri=os.getenv("archivematica_uri"),
        ).get_all_packages()
    )
