import requests


class FedoraObject:
    def __init__(
        self, fedora_url="http://localhost:8080", auth=("fedoraAdmin", "fedoraAdmin")
    ):
        self.fedora_url = fedora_url
        self.auth = auth

    def ingest(
        self,
        namespace,
        label,
        state="A",
    ):
        r = requests.post(
            f"{self.fedora_url}/fedora/objects/new?namespace={namespace}&label={label}&state={state}",
            auth=self.auth,
        )
        if r.status_code == 201:
            return r.content
        else:
            raise Exception(f"Request to ingest object with label `{label}` failed with {r.status_code}.")


if __name__ == "__main__":
    x = FedoraObject().ingest(namespace="test", label="This is a test")
