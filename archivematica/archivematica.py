import requests
import os
from dotenv import load_dotenv


class PackageRequest:
    def __init__(
        self,
        username,
        api_key,
        uri="https://localhost:8001/api/v2",
        temporary_storage="/tmp",
    ):
        self.uri = uri
        self.username = username
        self.api_key = api_key
        self.temporary_storage = temporary_storage

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

        We already have our AIPs compressed.  Therefore, this downloads the compressed AIP as is.  We do not compress
        DIPs in Archivematica.  Therefore, this compresses the DIPs as a tar.  If the package is an AIP, it is saved
        to temp storage as the original compressed file.  If it is a DIP, it is stored as the DIP's uuid with a .tar
        extension.

        Args:
            uuid (str): The uuid of the package you want to download.

        Returns:
            str: A message about where the file was serialized to disk.

        Examples:
            >>> PackageRequest("test", "my_api_key").download_package('2aaa349a-12a2-4338-90d1-5097bb989acc')
            "Wrote package to temp/Chronicling_COVID-19-20210215T185151Z-001-2aaa349a-12a2-4338-90d1-5097bb989acc.7z"
            >>> PackageRequest("test", "my_api_key").download_package('dea5c7af-2321-4102-be4b-93b3866c9c84')
            "Wrote package to temp/dea5c7af-2321-4102-be4b-93b3866c9c84.tar"

        """
        filename = ""
        details = self.get_package_details(uuid)
        if details["package_type"] == "DIP":
            filename = f"{uuid}.tar"
        else:
            filename = details["current_full_path"].split("/")[-1]
        with requests.get(
            f"{self.uri}/file/{uuid}/download/?username={self.username}&api_key={self.api_key}",
            stream=True,
        ) as r:
            r.raise_for_status()
            with open(f"{self.temporary_storage}/{filename}", "wb") as current_package:
                for chunk in r.iter_content(chunk_size=8192):
                    current_package.write(chunk)
        return f"Wrote package to {self.temporary_storage}/{filename}"

    def get_list_of_aips_and_dips(self):
        """Get a list of tuples with the AIP as index 0 and DIP as index 1.

        Returns:
            list: a list of tuples with AIP and DIP.

        Examples:
            >>> PackageRequest("test", "my_api_key").get_list_of_aips_and_dips()
            [('2aaa349a-12a2-4338-90d1-5097bb989acc', 'dea5c7af-2321-4102-be4b-93b3866c9c84'), ('5cf2ab4b-27d7-475d-aec5-5993bccabee1', '2b52c29b-2bec-4c69-925c-8cd0567df3fa')]

        """
        r = requests.get(
            f"{self.uri}/file/?username={self.username}&api_key={self.api_key}"
        )
        return [
            (package["uuid"], package["related_packages"][0].split("/")[-2])
            for package in r.json()["objects"]
            if package["package_type"] == "AIP"
        ]

    def get_descriptive_metadata(self, pair):
        # TODO This doesn't work.  It returns a 404.  I've tried giving it a full path and relative path, but no idea.
        path = f"{self.get_package_details(pair[1])['current_full_path'].split('/')[-1]}/METS.{pair[0]}.xml"
        print(path)
        r = requests.get(
            f"{self.uri}/file/{pair[1]}/extract_file/{path}?username={self.username}&api_key={self.api_key}"
        )
        return r.status_code


if __name__ == "__main__":
    load_dotenv()
    print(
        PackageRequest(
            username=os.getenv("username"),
            api_key=os.getenv("key"),
            uri=os.getenv("archivematica_uri"),
            temporary_storage="temp",
        ).get_descriptive_metadata(('33b86d0f-849c-40a9-818d-2dac9dace91b', '7f772d46-b005-42eb-8060-1ccc433dd0a8'))
    )
