import uuid
from enum import Enum

import pytest
import requests_mock

from pythonik.models.files.file import FileCreate, FileType, FileStatus
from pythonik.client import PythonikClient
from pythonik.exceptions import UnexpectedStorageMethodForProxy
from pythonik.models.files.keyframe import Keyframe, Keyframes, Resolution
from pythonik.models.files.file import (
    FileSetsFilesResponse,
    Files,
    FileSets,
    FileSet,
    FileCreate,
    FileSetCreate,
    UploadUrlResponse,
    S3MultipartUploadResponse,
)
from pythonik.models.files.format import Component, Formats, Format, FormatCreate
from pythonik.models.files.proxy import Proxies, Proxy
from pythonik.models.files.storage import Storage
from pythonik.specs.files import (
    FilesSpec,
    GET_STORAGE_PATH,
    GET_STORAGES_PATH,
    GET_ASSET_KEYFRAME,
    GET_ASSET_KEYFRAMES,
    GET_ASSET_PROXY_PATH,
    GET_ASSETS_FILES_PATH,
    GET_ASSET_PROXIES_PATH,
    GET_ASSETS_FORMAT_PATH,
    DELETE_ASSETS_FILE_PATH,
    GET_ASSETS_FORMATS_PATH,
    GET_ASSETS_FILE_SETS_PATH,
    DELETE_ASSETS_FILE_SET_PATH,
    GET_ASSETS_FILE_SET_FILES_PATH,
    GET_ASSETS_FORMAT_COMPONENTS_PATH,
    GET_ASSET_PROXIES_MULTIPART_URL_PATH,
)
from pythonik.tests.utils import (
    generate_mock_gcs_upload_url,
    generate_mock_s3_multipart_upload_url,
    generate_mock_s3_multipart_upload_start_response,
)


# cannot extend enums, unfortunately
class StorageMethod(str, Enum):
    S3 = "S3"
    GCS = "GCS"
    NOT_REAL = "I_MADE_IT_UP"


def test_create_asset_format_component():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        format_id = str(uuid.uuid4())

        model = Component(id=str(uuid.uuid4()), type="assets", metadata={})
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSETS_FORMAT_COMPONENTS_PATH.format(asset_id, format_id)
        )
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_format_component(asset_id, format_id, body=model)


def test_get_asset_file_sets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        file_sets_id = str(uuid.uuid4())

        data = FileSetsFilesResponse().model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSETS_FILE_SET_FILES_PATH.format(asset_id, file_sets_id)
        )
        m.get(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_file_set_files(asset_id, file_sets_id)


def test_get_proxy_by_proxy_id():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        proxy_id = str(uuid.uuid4())

        model = Proxy()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSET_PROXY_PATH.format(asset_id, proxy_id)
        )

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_proxy(asset_id, proxy_id)


def test_update_keyframe():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        keyframe_id = str(uuid.uuid4())

        model = Keyframe(status="CLOSED")
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSET_KEYFRAME.format(asset_id, keyframe_id)
        )

        m.post(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().update_keyframe(asset_id, keyframe_id, body=model)


def test_partial_update_keyframe():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        keyframe_id = str(uuid.uuid4())

        model = Keyframe(status="CLOSED")
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSET_KEYFRAME.format(asset_id, keyframe_id)
        )

        m.patch(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().partial_update_keyframe(asset_id, keyframe_id, body=model)


def test_create_asset_keyframe():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Keyframe(
            storage_id=str(uuid.uuid4()), status="OPEN", name=str(uuid.uuid4())
        )
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSET_KEYFRAMES.format(asset_id))

        m.post(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_keyframe(asset_id, body=model)


def test_delete_asset_keyframe():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        keyframe_id = str(uuid.uuid4())

        mock_address = FilesSpec.gen_url(
            GET_ASSET_KEYFRAME.format(asset_id, keyframe_id)
        )

        m.delete(mock_address)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().delete_asset_keyframe(asset_id, keyframe_id)


def test_get_asset_keyframes():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Keyframes()
        # this will raise a Pydantic serialization warning because
        # the default value for TimeCode, Resolution are dicts
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSET_KEYFRAMES.format(asset_id))

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_keyframes(asset_id)


def test_get_asset_keyframe():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        keyframe_id = str(uuid.uuid4())

        model = Keyframe()
        # this will raise a Pydantic serialization warning because
        # the default value for TimeCode, Resolution are dicts
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSET_KEYFRAME.format(asset_id, keyframe_id)
        )

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_keyframe(asset_id, keyframe_id)


def test_create_asset_proxy():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Proxy(
            asset_id=asset_id, storage_id=str(uuid.uuid4()), storage_method="S3"
        )
        # data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSET_PROXIES_PATH.format(asset_id))

        m.post(mock_address, json=model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_proxy(asset_id, body=model)


def test_update_asset_proxy():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        proxy_id = str(uuid.uuid4())

        model = Proxy(asset_id=asset_id, status="CLOSED", id=proxy_id)
        mock_address = FilesSpec.gen_url(
            GET_ASSET_PROXY_PATH.format(asset_id, proxy_id)
        )

        m.patch(mock_address, json=model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().update_asset_proxy(asset_id, proxy_id, body=model)


@pytest.mark.parametrize(
    "storage_method,exception",
    [
        # (StorageMethod.S3, True),
        (StorageMethod.GCS, False),
        (StorageMethod.NOT_REAL, True),
    ],
)
def test_get_upload_id_for_keyframe(storage_method, exception):
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        keyframe_id = str(uuid.uuid4())

        bucket_name = str(uuid.uuid4())
        object_key = f"{str(uuid.uuid4())}.mp4"

        if storage_method == StorageMethod.GCS:
            upload_url = generate_mock_gcs_upload_url(bucket_name, object_key)
            kf = Keyframe(
                asset_id=asset_id,
                id=keyframe_id,
                upload_url=upload_url,
                storage_method=storage_method,
            )

            # request to get upload ID
            m.post(
                upload_url,
                headers={
                    "X-GUploader-UploadID": "X-GUploader-UploadID",
                    "Location": "LOCATION",
                },
            )
        else:
            upload_url = generate_mock_s3_multipart_upload_url(bucket_name, object_key)
            kf = Keyframe(
                asset_id=asset_id,
                id=keyframe_id,
                multipart_upload_url=upload_url,
                storage_method=storage_method,
            )

            # request to get upload ID
            text = generate_mock_s3_multipart_upload_start_response(
                bucket_name, object_key
            )
            m.post(upload_url, text=text)

        # request to get proxy
        m.get(
            url=FilesSpec.gen_url(GET_ASSET_PROXY_PATH.format(asset_id, keyframe_id)),
            json=kf.model_dump(),
        )

        if exception:  # we expect an exception to be raised
            with pytest.raises(UnexpectedStorageMethodForProxy):
                client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
                client.files().get_upload_id_for_keyframe(keyframe=kf)
            return

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_upload_id_for_keyframe(keyframe=kf)


@pytest.mark.parametrize(
    "storage_method,exception",
    [
        (StorageMethod.S3, False),
        (StorageMethod.GCS, False),
        (StorageMethod.NOT_REAL, True),
    ],
)
def test_get_proxy_upload_id(storage_method, exception):
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        proxy_id = str(uuid.uuid4())

        bucket_name = str(uuid.uuid4())
        object_key = f"{str(uuid.uuid4())}.mp4"

        if storage_method == StorageMethod.GCS:
            upload_url = generate_mock_gcs_upload_url(bucket_name, object_key)
            proxy = Proxy(
                asset_id=asset_id,
                id=proxy_id,
                upload_url=upload_url,
                storage_method=storage_method,
            )

            # request to get upload ID
            m.post(upload_url, headers={"X-GUploader-UploadID": "X-GUploader-UploadID"})
        else:
            upload_url = generate_mock_s3_multipart_upload_url(bucket_name, object_key)
            proxy = Proxy(
                asset_id=asset_id,
                id=proxy_id,
                multipart_upload_url=upload_url,
                storage_method=storage_method,
            )

            # request to get upload ID
            text = generate_mock_s3_multipart_upload_start_response(
                bucket_name, object_key
            )
            m.post(upload_url, text=text)

        # request to get proxy
        m.get(
            url=FilesSpec.gen_url(GET_ASSET_PROXY_PATH.format(asset_id, proxy_id)),
            json=proxy.model_dump(),
        )

        if exception:  # we expect an exception to be raised
            with pytest.raises(UnexpectedStorageMethodForProxy):
                client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
                client.files().get_upload_id_for_proxy(asset_id, proxy_id)
            return

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_upload_id_for_proxy(asset_id, proxy_id)


def test_get_s3_presigned_url():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        proxy_id = str(uuid.uuid4())
        upload_id = str(uuid.uuid4())

        model = S3MultipartUploadResponse(objects=[UploadUrlResponse(number=1)])
        mock_address = FilesSpec.gen_url(
            GET_ASSET_PROXIES_MULTIPART_URL_PATH.format(asset_id, proxy_id)
        )

        m.get(mock_address, json=model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_s3_presigned_url(
            asset_id, proxy_id, upload_id=upload_id, part_number=1
        )


def test_get_proxies():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Proxies()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSET_PROXIES_PATH.format(asset_id))

        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_proxies(asset_id)


def test_get_asset_format():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        format_id = str(uuid.uuid4())

        model = Format()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            GET_ASSETS_FORMAT_PATH.format(asset_id, format_id)
        )
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_asset_format(asset_id, format_id)


def test_get_asset_formats():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Formats()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FORMATS_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_formats(asset_id, params=params)


def test_create_asset_file():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        name = str(uuid.uuid4())
        type = FileType.FILE.value
        status = FileStatus.CLOSED.value
        model = FileCreate(
            file_set_id=str(uuid.uuid4()),
            format_id=str(uuid.uuid4()),
            storage_id=str(uuid.uuid4()),
            name=name,
            original_name=name,
            size=41,
            type=type,
            status=status,
        )
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FILES_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_file(asset_id, body=model)


def test_create_asset_format():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FormatCreate(name="ORIGINAL")
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FORMATS_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_format(asset_id, body=model)


def test_create_asset_file_sets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FileSetCreate(
            name=str(uuid.uuid4()),
            format_id=str(uuid.uuid4()),
            storage_id=str(uuid.uuid4()),
        )
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FILE_SETS_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_file_sets(asset_id, body=model)


def test_create_asset_filesets_deprecated():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FileSetCreate(
            name=str(uuid.uuid4()),
            format_id=str(uuid.uuid4()),
            storage_id=str(uuid.uuid4()),
        )
        data = model.model_dump()

        mock_address = FilesSpec.gen_url(GET_ASSETS_FILE_SETS_PATH.format(asset_id))
        m.post(mock_address, json=data)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().create_asset_filesets(asset_id, body=model)


def test_get_asset_filesets():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = FileSets()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FILE_SETS_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_filesets(asset_id, params=params)


def test_get_asset_files():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())

        model = Files()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_ASSETS_FILES_PATH.format(asset_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        params = {"per_page": 20}
        client.files().get_asset_files(asset_id, params=params)


def test_get_storage():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        storage_id = str(uuid.uuid4())

        model = Storage()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_STORAGE_PATH.format(storage_id))
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_storage(storage_id)


def test_get_storages():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())

        model = Storage()
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(GET_STORAGES_PATH)
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().get_storages()


def test_delete_asset_file():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        file_id = str(uuid.uuid4())

        mock_address = FilesSpec.gen_url(
            DELETE_ASSETS_FILE_PATH.format(asset_id, file_id)
        )

        m.delete(mock_address)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().delete_asset_file(asset_id, file_id)


def test_delete_asset_file_set_immediate():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        file_set_id = str(uuid.uuid4())

        mock_address = FilesSpec.gen_url(
            DELETE_ASSETS_FILE_SET_PATH.format(asset_id, file_set_id)
        )

        # Mock 204 response for immediate deletion
        m.delete(mock_address, status_code=204)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().delete_asset_file_set(asset_id, file_set_id)


def test_delete_asset_file_set_marked():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        file_set_id = str(uuid.uuid4())

        model = FileSet(id=file_set_id, status="deleted")
        data = model.model_dump()
        mock_address = FilesSpec.gen_url(
            DELETE_ASSETS_FILE_SET_PATH.format(asset_id, file_set_id)
        )

        # Mock 200 response with FileSet data
        m.delete(mock_address, json=data, status_code=200)

        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.files().delete_asset_file_set(asset_id, file_set_id)


def test_delete_asset_file_set_keep_source():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        file_set_id = str(uuid.uuid4())

        mock_address = FilesSpec.gen_url(
            DELETE_ASSETS_FILE_SET_PATH.format(asset_id, file_set_id)
        )

        # Mock 204 response
        m.delete(mock_address, status_code=204)


# def test_file_create_serialization_behavior():
#     file_data = FileCreate(
#         file_set_id="fs123",
#         format_id="fmt456",
#         storage_id="stor789",
#         name="test_file.txt",
#         original_name="original_test_file.txt",
#         size=1024,
#         type=FileType.FILE.value,  # This has a default value
#         directory_path="/path/to/dir",
#         status=FileStatus.CLOSED.value  # This has a default value
#     )

#     # With exclude_defaults=True
#     data_exclude_defaults = file_data.model_dump(exclude_defaults=True)
#     # Fields with defaults will be excluded even if explicitly set
#     # assert "type" not in data_exclude_defaults
#     assert "status" not in data_exclude_defaults

#     # With exclude_unset=True
#     data_exclude_unset = file_data.model_dump(exclude_unset=True)
#     # Fields that were explicitly set will be included, even if they match defaults
#     assert "type" in data_exclude_unset
#     assert "status" in data_exclude_unset
