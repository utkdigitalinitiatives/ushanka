import requests
import os
from dotenv import load_dotenv
import xmltodict
from pathlib import Path


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

    def download_package(self, uuid, store_directory="object_1"):
        """Download a package.  If the package is not already compressed, compress it as a tar.

        We already have our AIPs compressed.  Therefore, this downloads the compressed AIP as is.  We do not compress
        DIPs in Archivematica.  Therefore, this compresses the DIPs as a tar.  If the package is an AIP, it is saved
        to temp storage as the original compressed file.  If it is a DIP, it is stored as the DIP's uuid with a .tar
        extension.

        Args:
            uuid (str): The uuid of the package you want to download.
            store_directory (str): The subdirectory where you want to download your package to.

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
            with open(
                f"{self.temporary_storage}/{store_directory}/{details['package_type']}/{filename}",
                "wb",
            ) as current_package:
                for chunk in r.iter_content(chunk_size=8192):
                    current_package.write(chunk)
        return f"Wrote package to {self.temporary_storage}/{store_directory}/{filename}"

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
        """Parses the descriptive metadata from the METS.

        Args:
            pair (tuple): A tuple with an AIP uuid and DIP uuid.

        Returns:
            OrderedDict: An ordered dict of descriptive metadata elements from the originating SIP.

        Examples:
            >>> PackageRequest("test", "my_api_key").get_descriptive_metadata(("33b86d0f-849c-40a9-818d-2dac9dace91b","7f772d46-b005-42eb-8060-1ccc433dd0a8",))
            OrderedDict([('dcterms:dublincore', OrderedDict([('@xmlns:dc', 'http://purl.org/dc/elements/1.1/'), ('@xmlns:dcterms', 'http://purl.org/dc/terms/'), ('@xsi:schemaLocation', 'http://purl.org/dc/terms/ https://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd'), ('dc:title', 'Chronocling Covid'), ('dc:description', 'This test deposit includes objects submitted as part of the Chronicling Covid-19 project.'), ('dc:publisher', 'University of Tennessee'), ('dc:date', '2020'), ('dc:language', 'English'), ('dc:rights', 'Copyright Not Evaluated')]))])

        """
        path = f"{self.get_package_details(pair[1])['current_path'].split('/')[-1]}/METS.{pair[0]}.xml"
        r = requests.get(
            f"{self.uri}/file/{pair[1]}/extract_file/?username={self.username}&api_key={self.api_key}&relative_path_to_file={path}"
        )
        return xmltodict.parse(r.content)["mets:mets"]["mets:dmdSec"][0]["mets:mdWrap"][
            "mets:xmlData"
        ]

    def parse_metadata(self, pair):
        """Reads descriptive metadata and formats as a simple dict.

        Args:
            pair (tuple): A tuple with an AIP uuid and a DIP uuid.

        Returns:
            dict: A dict with keys and values it can make sense of.

        Examples:
            >>> PackageRequest("test", "my_api_key").parse_metadata(("33b86d0f-849c-40a9-818d-2dac9dace91b", "7f772d46-b005-42eb-8060-1ccc433dd0a8"))
            {'title': 'Chronocling Covid', 'abstract': 'This test deposit includes objects submitted as part of the Chronicling Covid-19 project.', 'publisher': 'University of Tennessee', 'date': '2020', 'language': 'English', 'rights': 'Copyright Not Evaluated'}
            >>> PackageRequest("test", "my_api_key").parse_metadata(('2aaa349a-12a2-4338-90d1-5097bb989acc', 'dea5c7af-2321-4102-be4b-93b3866c9c84'))
            {'title': '', 'abstract': '', 'date': '', 'language': '', 'publisher': '', 'rights': ''}

        """
        metadata = {
            "title": "",
            "abstract": "",
            "date": "",
            "language": "",
            "publisher": "",
            "rights": "",
        }
        try:
            x = self.get_descriptive_metadata(pair)["dcterms:dublincore"]
        except KeyError:
            x = {}
        for k, v in x.items():
            if k == "dc:title":
                metadata["title"] = v
            if k == "dc:description":
                metadata["abstract"] = v
            if k == "dc:date":
                metadata["date"] = v
            if k == "dc:language":
                metadata["language"] = v
            if k == "dc:publisher":
                metadata["publisher"] = v
            if k == "dc:rights":
                metadata["rights"] = v
        return metadata


class ArchivematicaBundler(PackageRequest):
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
        super().__init__(username, api_key, uri, temporary_storage)

    def __serialize_metadata(self, pair):
        with open(
            f"{self.temporary_storage}/{pair[0]}/metadata.py", "w"
        ) as metadata_file:
            metadata_file.write(str(self.parse_metadata(pair)))
        return

    def __download_a_thumbnail(self, pair, store_directory="object_1"):
        """Leverage the METS to identify a thumbnail to represent the object."""
        path = f"{self.get_package_details(pair[1])['current_path'].split('/')[-1]}/METS.{pair[0]}.xml"
        r = requests.get(
            f"{self.uri}/file/{pair[1]}/extract_file/?username={self.username}&api_key={self.api_key}&relative_path_to_file={path}"
        )
        thumbnails = [
            amd_sec["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"][
                "premis:objectIdentifier"
            ]["premis:objectIdentifierValue"]
            for amd_sec in xmltodict.parse(r.content)["mets:mets"]["mets:amdSec"]
            if amd_sec["mets:techMD"]["mets:mdWrap"]["mets:xmlData"]["premis:object"][
                "premis:objectCharacteristics"
            ]["premis:format"]["premis:formatDesignation"]["premis:formatName"]
            == "JPEG"
        ]
        with requests.get(
            f"{self.uri}/file/{pair[1]}/extract_file/?username={self.username}&api_key={self.api_key}&relative_path_to_file={self.get_package_details(pair[1])['current_path'].split('/')[-1]}/thumbnails/{thumbnails[0]}.jpg",
            stream=True,
        ) as thumbnail:
            thumbnail.raise_for_status()
            with open(
                f"{self.temporary_storage}/{store_directory}/TN.jpg",
                "wb",
            ) as current_package:
                for chunk in thumbnail.iter_content(chunk_size=8192):
                    current_package.write(chunk)
        return f"Wrote thumbnail to {self.temporary_storage}/{store_directory}/TN.jpg"

    def build_bundles(self):
        """Serializes Bundles of Archivematica packages to disk.

        Returns:
            str: A message including the number of bundles serialized to disk.py

        Examples:
            >>> PackageRequest("test", "my_api_key").build_bundles()
            "Serialized 3 bundles from Archivematica to disk."

        """
        bundles = self.get_list_of_aips_and_dips()
        for bundle in bundles:
            Path(f"{self.temporary_storage}/{bundle[0]}/DIP").mkdir(
                parents=True, exist_ok=True
            )
            Path(f"{self.temporary_storage}/{bundle[0]}/AIP").mkdir(
                parents=True, exist_ok=True
            )
            self.download_package(bundle[0], bundle[0])
            self.download_package(bundle[1], bundle[0])
            self.__serialize_metadata(bundle)
            self.__download_a_thumbnail(bundle, bundle[0])
        return f"Serialized {len(bundles)} bundles from Archivematica to disk."


if __name__ == "__main__":
    load_dotenv()
    ArchivematicaBundler(
        username=os.getenv("username"),
        api_key=os.getenv("key"),
        uri=os.getenv("archivematica_uri"),
        temporary_storage="data",
    ).build_bundles()
