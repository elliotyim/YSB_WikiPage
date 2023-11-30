from fastapi.testclient import TestClient
from starlette import status


class TestPostRouters:
    def test_get_posts(self, test_client: TestClient):
        response = test_client.get("/posts")
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 0
