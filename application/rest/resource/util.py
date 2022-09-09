from flask import request

from domain.model import File, FileDict


def extract_all_files() -> FileDict:
    files = {}

    for upload in request.files.values():
        file = File(
            upload.filename,
            upload.mimetype,
            upload.stream
        )
        files[upload.name] = file

    return files
