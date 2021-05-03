import requests
from uuid import uuid4
import json


class ArchiveSpace:
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        self.base_url = url
        self.headers = {"X-ArchivesSpace-Session": self.__authenticate(user, password)}

    def __authenticate(self, username, password):
        r = requests.post(
            url=f"{self.base_url}/users/{username}/login?password={password}"
        )
        return r.json()["session"]


class Repository(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)

    def get(self, repo_id):
        """Get a repository.

        Args:
            repo_id (int): The id of the repository you are querying.

        Returns:
            dict: Metadata about the repository or an error saying it does not exits

        Examples:
            >>> Repository().get(2)
            {'lock_version': 0, 'repo_code': 'UTK', 'name': 'Betsey B. Creekmore Special Collections and University
            Archives', 'created_by': 'admin', 'last_modified_by': 'admin', 'create_time': '2021-04-29T16:08:29Z',
            'system_mtime': '2021-04-29T16:08:29Z', 'user_mtime': '2021-04-29T16:08:29Z', 'publish': True,
            'oai_is_disabled': False, 'jsonmodel_type': 'repository', 'uri': '/repositories/2', 'display_string':
            'Betsey B. Creekmore Special Collections and University Archives (UTK)', 'agent_representation': {'ref':
            '/agents/corporate_entities/1'}}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}",
            headers=self.headers,
        )
        return r.json()


class Accession(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)

    def get_list_of_ids(self, repo_id):
        """Get a list of ids for Accessions in a Repository.

        Args:
            repo_id (int): The id of the repository you are querying.

        Returns:
            list: A list of ints that represent each Accession in the repository.

        Examples:
            >>> Accession().get_list_of_ids(2)
            [1, 2]

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/accessions?all_ids=true",
            headers=self.headers,
        )
        return r.json()

    def get_accessions_on_page(self, repo_id, page=1, page_size=10):
        """Get Accessions on a page.

        Args:
            repo_id (int): The id of the repository you are querying.
            page (int): The page of accessions you want to get.
            page_size (int): The size of the page you want returned.

        Returns:
            dict: A dict with information about the results plus all matching Accessions.

        Examples:
            >>> Accession().get_accessions_on_page(2, 2, 10)
            {'first_page': 1, 'last_page': 1, 'this_page': 2, 'total': 2, 'results': []}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/accessions?page={page}&page_size={page_size}",
            headers=self.headers,
        )
        return r.json()


class Resource(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)

    def get_list_of_ids(self, repo_id):
        """Get a list of ids for Resources in a Repository.

        Args:
            repo_id (int): The id of the repository you are querying.

        Returns:
            list: A list of ints that represent each Resource in the repository.

        Examples:
            >>> Resource().get_list_of_ids(2)
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/resources?all_ids=true",
            headers=self.headers,
        )
        return r.json()

    def get_resources_by_page(self, repo_id, page=1, page_size=10):
        """Get Resources on a page.

        Args:
            repo_id (int): The id of the repository you are querying.
            page (int): The page of resources you want to get.
            page_size (int): The size of the page you want returned.

        Returns:
            dict: A dict with information about the results plus all matching Resources.

        Examples:
            >>> Resource().get_resources_by_page(2, 2, 10)
            {'first_page': 1, 'last_page': 1, 'this_page': 2, 'total': 2, 'results': []}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/resources?page={page}&page_size={page_size}",
            headers=self.headers,
        )
        return r.json()

    def get(self, repo_id, resource_id):
        """Get a specific resource.

        Args:
            repo_id (int): The id of the repository you are querying.
            resource_id (int): The id of the resource you are requesting.

        Returns:
            dict: A dict representing your resource.

        Examples:
            >>> Resource().get(2, 18)
            {'error': 'Resource not found'}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/resources/{resource_id}",
            headers=self.headers,
        )
        return r.json()


class DigitalObject(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)

    def get_list_of_ids(self, repo_id):
        """Get a list of ids for Digital Objects in a Repository.

        Args:
            repo_id (int): The id of the repository you are querying.

        Returns:
            list: A list of ints that represent each Digital Object in the repository.

        Examples:
            >>> DigitalObject().get_list_of_ids(2)
            []

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/digital_objects?all_ids=true",
            headers=self.headers,
        )
        return r.json()

    def get_by_page(self, repo_id, page=1, page_size=10):
        """Get Digital Objects on a page.

        Args:
            repo_id (int): The id of the repository you are querying.
            page (int): The page of digital objects you want to get.
            page_size (int): The size of the page you want returned.

        Returns:
            dict: A dict with information about the results plus all matching Digital Objects.

        Examples:
            >>> DigitalObject().get_by_page(2, 2, 10)
            {'first_page': 1, 'last_page': 1, 'this_page': 1, 'total': 0, 'results': []}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/digital_objects?page={page}&page_size={page_size}",
            headers=self.headers,
        )
        return r.json()

    def create(self, title, repo_id, specified_properties={}, file_versions=[]):
        """Creates a Digital Object in ArchivesSpace using specified properties and defaults.

        Args:
            title (str): A title for your new digital object.
            repo_id (int): The repo_id for the repository of which your digital object belongs.
            specified_properties (dict): Any properties to override properties set in initial object.
            file_versions (list): A list of file versions, if any, to add to your new digital object.

        Returns:
            dict: A dict with information about your new object and whether it was successfully created.

        Examples:
            >>> DigitalObject().create("Test with no versions", 2))
            {'status': 'Created', 'id': 1, 'lock_version': 0, 'stale': None, 'uri': '/repositories/2/digital_objects/1',
            'warnings': []}
            >>> DigitalObject().create("Tulip Tree", 2, file_versions=[FileVersion().add("https://digital.lib.utk.edu/collections/islandora/object/knoxgardens%3A115")])
            {'status': 'Created', 'id': 2, 'lock_version': 0, 'stale': None, 'uri': '/repositories/2/digital_objects/2',
            'warnings': []}

        """
        initial_object = {
            "jsonmodel_type": "digital_object",
            "external_ids": [],
            "subjects": [],
            "linked_events": [],
            "external_documents": [],
            "rights_statements": [],
            "linked_agents": [],
            "is_slug_auto": True,
            "publish": True,
            "file_versions": [],
            "restrictions": False,
            "notes": [],
            "linked_instances": [],
            "title": "Initialized object",
            "digital_object_id": str(uuid4()),
        }
        for key, value in specified_properties.items():
            initial_object[key] = value
        initial_object["title"] = title
        for file_version in file_versions:
            initial_object["file_versions"].append(file_version)
        r = requests.post(
            url=f"{self.base_url}/repositories/{repo_id}/digital_objects",
            headers=self.headers,
            data=json.dumps(initial_object),
        )
        return r.json()


class FileVersion:
    @staticmethod
    def add(uri, published=True, is_representative=True):
        return {
            "jsonmodel_type": "file_version",
            "is_representative": is_representative,
            "file_uri": uri,
            "xlink_actuate_attribute": "onRequest",
            "xlink_show_attribute": "new",
            "publish": published,
        }


if __name__ == "__main__":
    print(Resource().get(2, 299))
