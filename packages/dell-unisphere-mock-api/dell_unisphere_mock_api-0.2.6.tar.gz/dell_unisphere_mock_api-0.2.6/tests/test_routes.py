import pytest

from dell_unisphere_mock_api.main import app


class TestStorageResourceRoutes:
    def setup_method(self):
        self.last_created_resource = None

    @pytest.fixture
    def sample_resource_data(self):
        return {
            "name": "test_resource",
            "description": "Test storage resource",
            "type": "LUN",
            "pool": "pool_1",
            "isThinEnabled": True,
            "isCompressionEnabled": False,
            "isAdvancedDedupEnabled": False,
            "sizeTotal": 1024 * 1024 * 1024 * 100,  # 100GB
        }

    def test_create_storage_resource(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        response = test_client.post(
            "/api/types/storageResource/instances",
            json=sample_resource_data,
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_resource_data["name"]
        assert data["type"] == sample_resource_data["type"]
        assert "id" in data
        self.last_created_resource = data  # Store for other tests
        assert self.last_created_resource is not None

    def test_get_storage_resource(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a resource
        self.test_create_storage_resource(test_client, auth_headers, sample_resource_data)

        # Then get it
        response = test_client.get(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}",
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.last_created_resource["id"]

    def test_list_storage_resources(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        # Create a resource first
        self.test_create_storage_resource(test_client, auth_headers, sample_resource_data)

        # List all resources
        response = test_client.get("/api/types/storageResource/instances", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert isinstance(data, list)

    def test_update_storage_resource(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a resource
        self.test_create_storage_resource(test_client, auth_headers, sample_resource_data)

        # Update it
        update_data = {
            "description": "Updated description",
            "isCompressionEnabled": True,
        }
        response = test_client.patch(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}",
            json=update_data,
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == update_data["description"]
        assert data["isCompressionEnabled"] == update_data["isCompressionEnabled"]

    def test_delete_storage_resource(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a resource
        self.test_create_storage_resource(test_client, auth_headers, sample_resource_data)

        # Delete it
        response = test_client.delete(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}",
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200

        # Verify it's gone
        response = test_client.get(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}",
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 404

    def test_host_access_management(self, test_client, auth_headers, sample_resource_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a resource
        self.test_create_storage_resource(test_client, auth_headers, sample_resource_data)

        # Modify host access
        host_access = {"host": "host1", "accessType": "Production"}
        response = test_client.post(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}/action/modifyHostAccess",
            json=host_access,
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "hostAccess" in data

    def test_unauthorized_access(self, test_client, sample_resource_data):
        # Try to create without auth
        response = test_client.post("/api/types/storageResource/instances", json=sample_resource_data)
        assert response.status_code == 401

    def test_create_lun_action(self, test_client, auth_headers):
        headers, _ = auth_headers
        lun_data = {"name": "test_lun_1", "lunParameters": {"pool": {"id": "pool_1"}, "size": 1073741824}}  # 1GB
        response = test_client.post("/api/types/storageResource/action/createLun", json=lun_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "@base" in data
        assert "updated" in data
        assert "links" in data
        assert "content" in data
        assert "storageResource" in data["content"]
        assert "id" in data["content"]["storageResource"]
        self.last_created_resource = {"id": data["content"]["storageResource"]["id"]}

    def test_create_lun_action_missing_fields(self, test_client, auth_headers):
        headers, _ = auth_headers
        # Test missing name
        lun_data = {"lunParameters": {"pool": {"id": "pool_1"}, "size": 1073741824}}
        response = test_client.post("/api/types/storageResource/action/createLun", json=lun_data, headers=headers)
        assert response.status_code == 400

        # Test missing lunParameters
        lun_data = {"name": "test_lun_1"}
        response = test_client.post("/api/types/storageResource/action/createLun", json=lun_data, headers=headers)
        assert response.status_code == 400

    def test_modify_lun_action(self, test_client, auth_headers):
        headers, _ = auth_headers
        # First create a LUN
        self.test_create_lun_action(test_client, auth_headers)

        # Modify the LUN
        modify_data = {"description": "Modified Lun.", "lunParameters": {"size": 3221225472}}  # 3GB
        response = test_client.post(
            f"/api/types/storageResource/{self.last_created_resource['id']}/action/modifyLun",
            json=modify_data,
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify changes
        response = test_client.get(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Modified Lun."
        assert data["sizeTotal"] == 3221225472

    def test_expand_lun_action(self, test_client, auth_headers):
        headers, _ = auth_headers
        # First create a LUN
        self.test_create_lun_action(test_client, auth_headers)

        # Expand the LUN
        expand_data = {"size": 4294967296}  # 4GB
        response = test_client.post(
            f"/api/types/storageResource/{self.last_created_resource['id']}/action/expandLun",
            json=expand_data,
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify changes
        response = test_client.get(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sizeTotal"] == expand_data["size"]

    def test_expand_lun_action_smaller_size(self, test_client, auth_headers):
        headers, _ = auth_headers
        # First create a LUN
        self.test_create_lun_action(test_client, auth_headers)

        # Try to expand with smaller size
        expand_data = {"size": 536870912}  # 512MB (smaller than original 1GB)
        response = test_client.post(
            f"/api/types/storageResource/{self.last_created_resource['id']}/action/expandLun",
            json=expand_data,
            headers=headers,
        )
        assert response.status_code == 400
        data = response.json()
        assert "must be larger than current size" in data["detail"]

    def test_expand_lun_action_missing_size(self, test_client, auth_headers):
        headers, _ = auth_headers
        # First create a LUN
        self.test_create_lun_action(test_client, auth_headers)

        # Try to expand without size
        expand_data = {}
        response = test_client.post(
            f"/api/types/storageResource/{self.last_created_resource['id']}/action/expandLun",
            json=expand_data,
            headers=headers,
        )
        assert response.status_code == 400
        data = response.json()
        assert "Missing required field: size" in data["detail"]

    def test_delete_storage_resource_action(self, test_client, auth_headers):
        headers, _ = auth_headers
        # First create a LUN
        self.test_create_lun_action(test_client, auth_headers)

        # Delete using action endpoint
        response = test_client.post(
            f"/api/types/storageResource/{self.last_created_resource['id']}/action/delete", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # Verify deletion
        response = test_client.get(
            f"/api/types/storageResource/instances/{self.last_created_resource['id']}", headers=headers
        )
        assert response.status_code == 404


class TestFilesystemRoutes:
    def setup_method(self):
        self.last_created_filesystem = None

    @pytest.fixture
    def sample_filesystem_data(self):
        return {
            "name": "test_filesystem",
            "description": "Test filesystem",
            "nasServer": "nas_1",
            "size": 1024 * 1024 * 1024 * 100,  # 100GB
            "protocol": "NFS",
        }

    def test_create_filesystem(self, test_client, auth_headers, sample_filesystem_data):
        headers, _ = auth_headers  # Unpack the tuple
        response = test_client.post(
            "/api/types/filesystem/instances",
            json=sample_filesystem_data,
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_filesystem_data["name"]
        assert "id" in data
        self.last_created_filesystem = data  # Store for other tests
        assert self.last_created_filesystem is not None

    def test_get_filesystem(self, test_client, auth_headers, sample_filesystem_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a filesystem
        self.test_create_filesystem(test_client, auth_headers, sample_filesystem_data)

        # Then get it
        response = test_client.get(
            f"/api/instances/filesystem/{self.last_created_filesystem['id']}",
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.last_created_filesystem["id"]


class TestNasServerRoutes:
    def setup_method(self):
        self.last_created_nas = None

    @pytest.fixture
    def sample_nas_data(self):
        return {
            "name": "test_nas",
            "description": "Test NAS server",
            "pool": "pool_1",
            "currentUnixDirectoryService": "None",
            "isMultiprotocolEnabled": False,
            "currentPreferredIPv4Interface": None,
        }

    def test_create_nas_server(self, test_client, auth_headers, sample_nas_data):
        headers, _ = auth_headers  # Unpack the tuple
        response = test_client.post("/api/types/nasServer/instances", json=sample_nas_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_nas_data["name"]
        assert "id" in data
        self.last_created_nas = data  # Store for other tests
        assert self.last_created_nas is not None

    def test_get_nas_server(self, test_client, auth_headers, sample_nas_data):
        headers, _ = auth_headers  # Unpack the tuple
        # First create a NAS server
        self.test_create_nas_server(test_client, auth_headers, sample_nas_data)

        # Then get it
        response = test_client.get(
            f"/api/instances/nasServer/{self.last_created_nas['id']}",
            headers=headers,  # Use only the headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.last_created_nas["id"]
