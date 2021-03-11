import requests
import os
from dotenv import load_dotenv


class PackageRequest:
    def __init__(self, username, api_key, uri="https://localhost:8001/api/v2"):
        self.uri = uri
        self.username = username
        self.api_key = api_key

    def get_all_packages(self):
        """Get the uuids for all packages from Archivematica.

        Returns:
            list: List of uuids for all packages in Archivematica.

        Examples:
            >>> PackageRequest("test", "my_api_key").get_all_packages()
            ['2aaa349a-12a2-4338-90d1-5097bb989acc', 'dea5c7af-2321-4102-be4b-93b3866c9c84', '5cf2ab4b-27d7-475d-aec5-5993bccabee1', '2b52c29b-2bec-4c69-925c-8cd0567df3fa']

        """
        r = requests.get(
            f"{self.uri}/file/?username={self.username}&api_key={self.api_key}"
        )
        return [package["uuid"] for package in r.json()["objects"]]

    def get_package_details(self, uuid):
        """Get the details about a package.

        Args:
            uuid (str): The uuid of the package you want the details of.

        Returns:
            dict: The details about a package.

        Examples:
            >>> PackageRequest("test", "my_api_key").get_package_details('2aaa349a-12a2-4338-90d1-5097bb989acc')
            {'current_full_path': '/gwork/archivematica/AIPsStore/2aaa/349a/12a2/4338/90d1/5097/bb98/9acc/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z', 'current_location': '/api/v2/location/65da3b00-f1ff-4e7b-b56c-abaf894ce9b4/', 'current_path': '2aaa/349a/12a2/4338/90d1/5097/bb98/9acc/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z', 'encrypted': False, 'misc_attributes': {}, 'origin_pipeline': '/api/v2/pipeline/21c132a8-9106-42a3-9046-0b6e12aaf141/', 'package_type': 'AIP', 'related_packages': ['/api/v2/file/dea5c7af-2321-4102-be4b-93b3866c9c84/'], 'replicas': [], 'replicated_package': None, 'resource_uri': '/api/v2/file/2aaa349a-12a2-4338-90d1-5097bb989acc/', 'size': 81143107, 'status': 'UPLOADED', 'uuid': '2aaa349a-12a2-4338-90d1-5097bb989acc'}

        """
        r = requests.get(
            f"{self.uri}/file/{uuid}?username={self.username}&api_key={self.api_key}"
        )
        return r.json()

    def download_package(self, uuid):
        """Download a package.  If the package is not already compressed, compress it as a tar.

        Args:
            uuid (str): The uuid of the package you want to download.

        """
        # TODO: This streams file to disk, but still approaches serialization wrong.  Fix.
        with requests.get(
            f"{self.uri}/file/{uuid}/download/?username={self.username}&api_key={self.api_key}",
            stream=True,
        ) as r:
            r.raise_for_status()
            with open(f"temp/{uuid}", "wb") as current_package:
                for chunk in r.iter_content(chunk_size=8192):
                    current_package.write(chunk)
        return f"Wrote package to temp/{uuid}"


if __name__ == "__main__":
    load_dotenv()
    print(
        PackageRequest(
            username=os.getenv("username"),
            api_key=os.getenv("key"),
            uri=os.getenv("archivematica_uri"),
        ).download_package("dea5c7af-2321-4102-be4b-93b3866c9c84")
    )
