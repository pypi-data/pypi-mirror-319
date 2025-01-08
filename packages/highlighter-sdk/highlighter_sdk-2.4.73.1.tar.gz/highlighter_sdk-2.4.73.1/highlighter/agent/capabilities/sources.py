import json
import os
import tempfile
from enum import Enum
from typing import Optional
from urllib.parse import urlparse

import cv2
import numpy as np
from PIL import Image

from highlighter.client import download_bytes
from highlighter.client.base_models import DataFile
from highlighter.client.io import _pil_open_image_bytes, _pil_open_image_path

from .base_capability import DataSourceCapability, DataSourceType

__all__ = [
    "ImageDataSource",
    "TextDataSource",
    "JsonArrayDataSource",
    "VideoDataSource",
]


class TextFrameIterator:

    def __init__(self, data_source: DataSourceType, byte_encoding="utf-8"):
        self.byte_encoding = byte_encoding
        if data_source.url.startswith("bytes"):
            self._read_text = lambda ds: ds.content.decode(self.byte_encoding)
        elif os.path.isfile(data_source.url):

            def read_text(p):
                with open(p, "r") as f:
                    return f.read()

            self._read_text = lambda ds: read_text(ds.url)
        elif all([urlparse(data_source.url), urlparse(data_source.url).netloc]):
            self._read_text = lambda ds: download_bytes(ds.url).decode(self.byte_encoding)
        else:
            raise ValueError(f"Invalid DataSource.url, expected local_path or url, got: {data_source.url}")

        self.ds = data_source
        self._complete = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._complete:
            raise StopIteration
        self._complete = True
        img = self._read_text(self.ds)
        data_file = DataFile(
            file_id=self.ds.id,
            content=img,
            content_type="text",
            media_frame_index=0,
        )
        return {"data_files": data_file, "entities": {}}


class TextDataSource(DataSourceCapability):
    """

    TODO: Check/update this

    Example:
        # process a single string
        hl agent run --data-source TextDataSource PIPELINE.json "tell me a joke."

        # process many text files
        ToDo

        # Read from stdin
        cat file | hl agent run --data-source TextDataSource -sp read_stdin=true PIPELINE.json
    """

    stream_media_type = "text"

    class DefaultStreamParameters(DataSourceCapability.DefaultStreamParameters):
        byte_encoding: Optional[str] = "utf-8"

    @property
    def byte_encoding(self) -> str:
        value, _ = self._get_parameter("byte_encoding")
        return value

    def frame_data_generator(self, data_sources):
        for ds in data_sources:
            for frame_data in TextFrameIterator(ds, self.byte_encoding):
                yield frame_data


class JsonArrayFrameIterator:
    def __init__(self, data_source: DataSourceType, key: str, byte_encoding="utf-8"):
        self.byte_encoding = byte_encoding

        if data_source.url.startswith("bytes"):
            _json = json.loads(data_source.content.decode(self.byte_encoding))
        elif os.path.isfile(data_source.url):
            with open(data_source.url, "r") as f:
                _json = json.load(f)
        elif all([urlparse(data_source.url), urlparse(data_source.url).netloc]):
            _json = json.loads(download_bytes(data_source.url).decode(self.byte_encoding))
        else:
            raise ValueError(f"Invalid DataSource.url, expected local_path or url, got: {data_source.url}")

        if key:
            for k in key.split("."):
                _json = _json[k]

        self._json_arr = iter([(data, i) for i, data in enumerate(_json)])

        self.ds = data_source
        self._complete = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            content, media_frame_index = next(self._json_arr)
            data_file = DataFile(
                file_id=self.ds.id,
                content=content,
                content_type="text",
                media_frame_index=media_frame_index,
            )
            return {"data_files": data_file, "entities": {}}
        except StopIteration:
            raise StopIteration


class JsonArrayDataSource(DataSourceCapability):

    stream_media_type = "text"

    class DefaultStreamParameters(DataSourceCapability.DefaultStreamParameters):
        key: str = ""

    @property
    def key(self) -> str:
        value, _ = self._get_parameter("key")
        return value

    def frame_data_generator(self, data_sources):
        for ds in data_sources:
            for frame_data in JsonArrayFrameIterator(ds, self.key):
                yield frame_data


class OutputType(str, Enum):
    numpy = "numpy"
    pillow = "pillow"


class ImageFrameIterator:
    def __init__(self, data_source: DataSourceType, output_type: OutputType):
        self.output_type = output_type
        if data_source.url.startswith("bytes"):
            self._read_image = lambda ds: _pil_open_image_bytes(ds.content)
        elif os.path.isfile(data_source.url):
            self._read_image = lambda ds: _pil_open_image_path(ds.url)
        elif all([urlparse(data_source.url), urlparse(data_source.url).netloc]):

            def _dl_pil_image(ds: DataSourceType):
                image_bytes = download_bytes(ds.url)
                assert image_bytes is not None
                image = _pil_open_image_bytes(image_bytes)
                return image

            self._read_image = _dl_pil_image
        elif data_source.url.startswith("hl-data-file-id"):
            raise NotImplementedError()
        else:
            raise ValueError(f"Invalid DataSource.url, expected local_path or url, got: {data_source.url}")

        self.ds = data_source
        self._complete = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._complete:
            raise StopIteration

        self._complete = True
        img = self._read_image(self.ds)
        if self.output_type == OutputType.numpy:
            img = np.array(img, dtype=np.uint8)

        data_file = DataFile(
            file_id=self.ds.id,
            content=img,
            content_type="image",
            media_frame_index=0,
        )
        return {"data_files": data_file, "entities": {}}


class ImageDataSource(DataSourceCapability):
    """

    Example:
        # process a single image
        hl agent run PIPELINE.json image.jpg

        # process many images
        find image/dir/ -n "*.jpg" | hl agent run PIPELINE.json
    """

    stream_media_type = "image"

    class DefaultStreamParameters(DataSourceCapability.DefaultStreamParameters):
        output_type: OutputType = OutputType.numpy

    @property
    def output_type(self) -> OutputType:
        value, _ = self._get_parameter("output_type")
        return value

    def frame_data_generator(self, data_sources):
        for ds in data_sources:
            for frame_data in ImageFrameIterator(ds, self.output_type):
                yield frame_data


class _AutoDeletingTempFile:
    def __init__(self, content_bytes):
        self.file = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = self.file.name
        self.file.write(content_bytes)
        self.file.flush()
        del content_bytes

    def __del__(self):
        if self.file_path and os.path.exists(self.file_path):
            os.remove(self.file_path)


class VideoFrameIterator:
    def __init__(self, data_source: DataSourceType, output_type: OutputType):

        self.output_type = output_type

        if data_source.url.startswith("bytes"):
            self._tmp_file = _AutoDeletingTempFile(data_source.content)
            video_path = self._tmp_file.file_path
        elif os.path.isfile(data_source.url):
            video_path = data_source.url
        elif all([urlparse(data_source.url), urlparse(data_source.url).netloc]):
            self._tmp_file = _AutoDeletingTempFile(download_bytes(data_source.url))
            video_path = self._tmp_file.file_path

        elif data_source.url.startswith("hl-data-file-id"):
            raise NotImplementedError()
        else:
            raise ValueError(f"Invalid DataSource.url, expected local_path or url, got: {data_source.url}")

        self.cap = cv2.VideoCapture(str(video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        self.video_path = video_path
        self.frame_index = 0
        self.ds = data_source

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame_img = self.cap.read()
        if not ret:  # No more frames to read
            self.cap.release()
            raise StopIteration

        frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

        if self.output_type == OutputType.pillow:
            frame_img = Image.fromarray(frame_img)

        data_file = DataFile(
            file_id=self.ds.id, content=frame_img, content_type="image", media_frame_index=self.frame_index
        )
        self.frame_index += 1
        return {"data_files": data_file, "entities": {}}

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        if hasattr(self, "_tmp_file"):
            del self._tmp_file


class VideoDataSource(DataSourceCapability):

    stream_media_type = "video"

    class DefaultStreamParameters(DataSourceCapability.DefaultStreamParameters):
        output_type: OutputType = OutputType.numpy

    @property
    def output_type(self) -> OutputType:
        value, _ = self._get_parameter("output_type")
        return value

    def frame_data_generator(self, data_sources):
        for ds in data_sources:
            for frame_data in VideoFrameIterator(ds, self.output_type):
                yield frame_data
