import requests


class ArchiveSpace:
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {"X-ArchivesSpace-Session": self.authenticate()}

    def authenticate(self):
        r = requests.post(
            url=f"{self.base_url}/users/{self.username}/login?password={self.password}"
        )
        return r.json()["session"]


class Repository(ArchiveSpace):
    def __init__(self, url="http://localhost:8089", user="admin", password="admin"):
        super().__init__(url, user, password)
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {"X-ArchivesSpace-Session": self.authenticate()}

    def get(self, repo_code):
        r = requests.get(
            url=f"{self.base_url}/repositories/{repo_code}",
            headers=self.headers,
        )
        return r.json()


if __name__ == "__main__":
    print(Repository().get("1"))
