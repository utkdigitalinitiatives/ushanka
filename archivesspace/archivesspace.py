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

    def get(self, repo_id, accession_id):
        """Get a specific accession.

        Args:
            repo_id (int): The id of the repository you are querying.
            accession_id (int): The id of the accession you are requesting.

        Returns:
            dict: A dict representing your resource.

        Examples:
            >>> Accession().get(2, 1)
            {'error': 'Resource not found'}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/accessions/{accession_id}",
            headers=self.headers,
        )
        return r.json()

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

    def create(self, repo_id, title, manuscript_id, extents=[]):
        """Create a resource / finding aid.

        Args:
            repo_id (int): The id for the repository.
            title (str): The title of your resource / finding aid.
            manuscript_id (str): The id for your finding aid.

        Returns:
            dict: Metadata and messaging stating whether your resource was created successfully or failed.

        Examples:
            >>> Resource().create(2, "Test finding aid", "MS.9999999")

        @todo: Currently only throws errors due to date and extent.

        """
        initial = {
            "jsonmodel_type": "resource",
            "external_ids": [],
            "subjects": [],
            "linked_events": [],
            "extents": extents,
            "lang_materials": [],
            "dates": [],
            "external_documents": [],
            "rights_statements": [],
            "linked_agents": [],
            "is_slug_auto": True,
            "restrictions": False,
            "revision_statements": [],
            "instances": [],
            "deaccessions": [],
            "related_accessions": [],
            "classifications": [],
            "notes": [],
            "title": title,
            "id_0": manuscript_id,
            "level": "item",
            "finding_aid_date": "",
            "finding_aid_series_statement": "",
            "finding_aid_language": "",
            "finding_aid_script": "",
            "finding_aid_note": "",
            "ead_location": "",
        }
        r = requests.post(
            url=f"{self.base_url}/repositories/{repo_id}/resources",
            headers=self.headers,
            data=json.dumps(initial),
        )
        return r.json()

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

    def link_digital_object(
        self, repo_id, resource_id, digital_object_id, is_representative=False
    ):
        """Link a digital object to a resource.

        Args:
            repo_id (int): The id of your repository.
            resource_id (int): The id of your resource.
            digital_object_id (int): The id of your digital object.
            is_representative (bool): Whether or not your digital object should be representative of the resource.

        Returns:
            dict: Success or error message with appropriate metadata.

        Examples:
            >>> Resource().link_digital_object(2, 18, 2)
            {'status': 'Updated', 'id': 18, 'lock_version': 1, 'stale': None, 'uri': '/repositories/2/resources/18',
            'warnings': []}

        """
        new_instance = {
            "is_representative": is_representative,
            "instance_type": "digital_object",
            "jsonmodel_type": "instance",
            "digital_object": {
                "ref": f"/repositories/2/digital_objects/{digital_object_id}"
            },
        }
        existing_collection = self.get(repo_id, resource_id)
        existing_collection["instances"].append(new_instance)
        r = requests.post(
            url=f"{self.base_url}/repositories/{repo_id}/resources/{resource_id}",
            headers=self.headers,
            data=json.dumps(existing_collection),
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

    def get(self, repo_id, digital_object_id):
        """Get a Resource by id.

        Args:
            repo_id (int): The id of the repository you are querying.
            digital_object_id (int): The id of the digital object you want.

        Returns:
            dict: The digital object as a dict.

        Examples:
            >>> DigitalObject().get(2, 2)
            {'error': 'DigitalObject not found'}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/digital_objects/{digital_object_id}",
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

    def add_badge(self, repo_id, digital_object_id, badge_uri):
        """Add an image to represent a digital object.

        Args:
            repo_id (int): The id of the repository you are querying.
            digital_object_id (int): The id of the digital object you want.
            badge_uri (str): The uri to image that represents the digital object.

        Returns:
            dict: A message stating whether or not your badge update was successful or an error.

        Examples
            >>> DigitalObject().add_badge(2, 2, "https://digital.lib.utk.edu/collections/islandora/object/knoxgardens%3A115/datastream/TN")
            {'status': 'Updated', 'id': 2, 'lock_version': 2, 'stale': None, 'uri': '/repositories/2/digital_objects/2',
            'warnings': []}

        """
        current = self.get(repo_id, digital_object_id)
        current["file_versions"].append(
            FileVersion().add(
                badge_uri, show_attribute="embed", is_representative=False
            )
        )
        r = requests.post(
            url=f"{self.base_url}/repositories/{repo_id}/digital_objects/{digital_object_id}",
            headers=self.headers,
            data=json.dumps(current),
        )
        return r.json()


class ArchivalObject(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)

    def get(self, repo_id, archival_object_id):
        """Get an archival object by id.

        Args:
            repo_id (int): The id of the repository you are querying.
            archival_object_id (int): The id of the archival object you want.

        Returns:
            dict: The archival object as a dict.

        Examples:
            >>> ArchivalObject().get(2, 37371)
            {'lock_version': 0, 'position': 0, 'publish': True, 'ref_id': 'ref13_6ap', 'title':
            '<title ns2:type="simple" render="doublequote">As You Came from the Holy Land,</title>', 'display_string':
            '<title ns2:type="simple" render="doublequote">As You Came from the Holy Land,</title>, undated',
            'restrictions_apply': False, 'created_by': 'admin', 'last_modified_by': 'admin', 'create_time':
            '2019-08-08T20:19:18Z', 'system_mtime': '2020-12-02T17:04:13Z', 'user_mtime': '2019-08-08T20:19:18Z',
            'suppressed': False, 'level': 'file', 'jsonmodel_type': 'archival_object', 'external_ids': [{'external_id':
            '209519', 'source': 'Archivists Toolkit Database::RESOURCE_COMPONENT', 'created_by': 'admin',
            'last_modified_by': 'admin', 'create_time': '2019-08-08T20:19:19Z', 'system_mtime': '2019-08-08T20:19:19Z',
            'user_mtime': '2019-08-08T20:19:19Z', 'jsonmodel_type': 'external_id'}], 'subjects': [], 'linked_events':
            [], 'extents': [], 'dates': [{'lock_version': 0, 'expression': 'undated', 'created_by': 'admin',
            'last_modified_by': 'admin', 'create_time': '2019-08-08T20:19:18Z', 'system_mtime': '2019-08-08T20:19:18Z',
            'user_mtime': '2019-08-08T20:19:18Z', 'date_type': 'single', 'label': 'creation', 'jsonmodel_type': 'date'}
            ], 'external_documents': [], 'rights_statements': [], 'linked_agents': [], 'ancestors': [{'ref':
            '/repositories/2/archival_objects/37369', 'level': 'series'}, {'ref': '/repositories/2/resources/598',
            'level': 'collection'}], 'instances': [{'lock_version': 0, 'created_by': 'admin', 'last_modified_by':
            'admin', 'create_time': '2019-08-08T20:19:19Z', 'system_mtime': '2019-08-08T20:19:19Z', 'user_mtime':
            '2019-08-08T20:19:19Z', 'instance_type': 'mixed_materials', 'jsonmodel_type': 'instance',
            'is_representative': False, 'sub_container': {'lock_version': 0, 'indicator_2': '1', 'created_by': 'admin',
            'last_modified_by': 'admin', 'create_time': '2019-08-08T20:19:19Z', 'system_mtime': '2019-08-08T20:19:19Z',
            'user_mtime': '2019-08-08T20:19:19Z', 'type_2': 'folder', 'jsonmodel_type': 'sub_container',
            'top_container': {'ref': '/repositories/2/top_containers/2961'}}}], 'notes': [{'content': [
            '(Labeled<emph render="doublequote">CP141- 3,</emph>i.e. Collected Poems, Robert Fitzgerald, ed., p. 141)'],
             'jsonmodel_type': 'note_singlepart', 'label': 'General Physical Description note', 'type': 'physdesc',
             'persistent_id': 'abf0fe13a03e23754e1faa666670442d', 'publish': True}], 'uri':
             '/repositories/2/archival_objects/37371', 'repository': {'ref': '/repositories/2'}, 'resource': {'ref':
             '/repositories/2/resources/598'}, 'parent': {'ref': '/repositories/2/archival_objects/37369'},
             'has_unpublished_ancestor': False}

        """
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_id}/archival_objects/{archival_object_id}",
            headers=self.headers,
        )
        return r.json()


class FileVersion:
    @staticmethod
    def add(uri, published=True, is_representative=True, show_attribute="new"):
        return {
            "jsonmodel_type": "file_version",
            "is_representative": is_representative,
            "file_uri": uri,
            "xlink_actuate_attribute": "onRequest",
            "xlink_show_attribute": show_attribute,
            "publish": published,
        }


class Extent:
    def __init__(self):
        self.valid_portions = ("whole", "part")
        self.valid_extent_type = (
            "cassettes",
            "cubic feet",
            "gigabytes",
            "megabytes",
            "terrabytes",
            "leaves",
            "linear feet",
            "photographic prints",
            "photographic slides",
            "reels",
            "sheets",
            "volumes",
            "boxes",
            "files",
        )

    def create(self, number, type_of_unit, portion, container_summary="", physical_details="", dimensions=""):
        """Creates extent information following the ArchivesSpace schema.

        Schema described here: https://github.com/archivesspace/archivesspace/blob/82c4603fe22bf0fd06043974478d4caf26e1c646/common/schemas/extent.rb

        Args:
            number (str): A numeric value for indicating the number of units in the extent statement, e.g, 5, 11.5, 245.
                Used in conjunction with Extent Type to provide a structured extent statement.
            type_of_unit (str): A term indicating the type of unit used to measure the extent of materials described.
            portion (str): Used to specify whether an extent statement relates to the whole or part of a given described.

        Returns:
            dict: The appropriate extent information following the ArchivesSpace schema.

        Examples:
            >>> Extent().create(number="35", type_of_unit="cassettes", portion="whole")
            {"jsonmodel_type": "extent", "portion": "whole", "number": "35", "extent_type": "cassettes",}

        """
        if portion in self.valid_portions and type_of_unit in self.valid_extent_type:
            model = {
                "jsonmodel_type": "extent",
                "portion": portion,
                "number": number,
                "extent_type": type_of_unit,
            }
            if container_summary != "":
                model["container_summary"] = container_summary
            if physical_details != "":
                model["physical_details"] = physical_details
            if dimensions != "":
                model["dimensions"] = dimensions
            return model

        else:
            raise Exception("Invalid extent information.")


if __name__ == "__main__":
    extents = [Extent().create(number="35", type_of_unit="cassettes", portion="whole")]
    print(Resource().create(2, "Test finding aid", "MS.9999999", extents))
