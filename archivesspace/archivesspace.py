import requests


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


if __name__ == "__main__":
    print(Resource().get_resources_by_page(2, 2, 10))
