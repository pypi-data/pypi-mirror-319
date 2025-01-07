import abc
import requests
import logging

from spaceone.core.connector import BaseConnector
from spaceone.inventory.error.file_upload import *


__all__ = ["FileUploadConnector", "AWSS3UploadConnector", "FilesUploadConnector"]

_LOGGER = logging.getLogger(__name__)


class FileUploadConnector(BaseConnector):

    @abc.abstractmethod
    def upload_file(self, file_path: str, options: dict):
        pass


class FilesUploadConnector(FileUploadConnector):
    @staticmethod
    def _make_request_header(token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/octet-stream",
        }
        return headers

    def upload_file(self, file_path: str, options: dict):
        endpoint = self.config.get("endpoint")
        url = f"{endpoint}/files/user/upload"
        file_name = file_path.rsplit("/", 1)[-1]
        _LOGGER.debug(
            f"[upload_file] Upload File ({endpoint}/user/upload): {file_name}"
        )

        headers = self._make_request_header(self.transaction.get_meta("token"))

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            response = requests.post(url, files=files, headers=headers)

            if response.status_code in [200, 204]:
                _LOGGER.debug(
                    f"[upload_file] File has been uploaded: {response.status_code} OK"
                )
                return response.json()
            else:
                _LOGGER.error(
                    f"[upload_file] File Upload Error: {response.status_code} {response.json()}"
                )
                raise ERROR_FILE_UPLOAD_FAILED(reason=response.json())


class AWSS3UploadConnector(FileUploadConnector):

    def upload_file(self, file_path: str, url: str, options: dict):
        file_name = file_path.rsplit("/", 1)[-1]
        _LOGGER.debug(f"[upload_file] Upload File ({url}): {file_name}")

        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            response = requests.post(url, data=options, files=files)

            if response.status_code in [200, 204]:
                _LOGGER.debug(
                    f"[upload_file] File has been uploaded: {response.status_code} OK"
                )
            else:
                _LOGGER.error(
                    f"[upload_file] File Upload Error: {response.status_code} {response.json()}"
                )
                raise ERROR_FILE_UPLOAD_FAILED(reason=response.json())
