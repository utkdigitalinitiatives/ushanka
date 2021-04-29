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

    def get(self, repo_code):
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_code}",
            headers=self.headers,
        )
        return r.json()


if __name__ == "__main__":
    print(Repository().get("2"))
