"""Frontend for working with data"""

import funcnodes as fn
import requests
import os
import base64
from dataclasses import dataclass
from typing import List

__version__ = "0.2.3"


class FileDownloadNode(fn.Node):
    """
    Downloads a file from a given URL and returns the file's content as bytes.
    """

    node_id = "files.dld"
    node_name = "File Download"

    url = fn.NodeInput(id="url", type="str")
    timeout = fn.NodeInput(id="timeout", type="float", default=10)

    data = fn.NodeOutput(id="data", type=bytes)

    serperate_thread = True

    async def func(self, url: str, timeout: float) -> None:
        """
        Downloads a file from a given URL and sets the "data" output to the file's content as bytes.

        Args:
          url (str): The URL of the file to download.
          timeout (float): The timeout in seconds for the download request.
        """
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                # set user agent to avoid 403 forbidden error
                "User-Agent": "Mozilla/5.0",
                # allow download of files
                "Accept": "*/*",
            },
        )
        self.outputs["data"].value = response.content


class FileUpload(str):
    pass


class FileUploadNode(fn.Node):
    """
    Uploads a file
    """

    node_id = "files.upl"
    node_name = "File Upload"

    input_data = fn.NodeInput(id="input_data", type=FileUpload)
    data = fn.NodeOutput(id="data", type=fn.types.databytes)
    filename = fn.NodeOutput(id="filename", type=str)
    path = fn.NodeOutput(id="path", type=str)

    async def func(self, input_data: FileUpload) -> None:
        """
        Uploads a file to a given URL.

        Args:
          url (str): The URL to upload the file to.
          file (str): The path to the file to upload.
        """
        if self.nodespace is None:
            raise Exception("Node not in a nodespace")

        fp = self.nodespace.get_file_path(input_data)
        if fp is None or not os.path.exists(fp):
            raise Exception(f"File not found: {input_data}")

        with open(fp, "rb") as file:
            filedata = file.read()

        self.outputs["data"].value = filedata
        self.outputs["filename"].value = os.path.basename(fp)
        self.outputs["path"].value = fp


class FolderUpload(list[FileUpload]):
    pass


class FolderUploadNode(fn.Node):
    """
    Uploads a file
    """

    node_id = "files.upl_folder"
    node_name = "Folder Upload"

    input_data = fn.NodeInput(id="input_data", type=FolderUpload)
    dates = fn.NodeOutput(id="dates", type=List[fn.types.databytes])
    filenames = fn.NodeOutput(id="filenames", type=List[str])
    paths = fn.NodeOutput(id="paths", type=List[str])

    async def func(self, input_data: FolderUpload) -> None:
        """
        Uploads a file to a given URL.

        Args:
          url (str): The URL to upload the file to.
          file (str): The path to the file to upload.
        """

        if self.nodespace is None:
            raise Exception("Node not in a nodespace")

        filepaths = [self.nodespace.get_file_path(file) for file in input_data]
        for fp in filepaths:
            if fp is None or not os.path.exists(fp):
                raise Exception(f"File not found: {fp}")

        filedatas = []
        for fp in filepaths:
            with open(fp, "rb") as file:
                filedatas.append(file.read())

        filenames = [os.path.basename(fp) for fp in filepaths]

        self.outputs["dates"].value = filedatas
        self.outputs["filenames"].value = filenames
        self.outputs["paths"].value = filepaths


@dataclass
class FileDownload:
    filename: str
    content: str

    @property
    def bytedata(self):
        return fn.types.databytes(base64.b64decode(self.content))

    def __str__(self) -> str:
        return f"FileDownload(filename={self.filename})"

    def __repr__(self) -> str:
        return self.__str__()


class FileDownloadLocal(fn.Node):
    """
    Downloads a file the funcnodes stream to a local file
    """

    node_id = "files.dld_local"
    node_name = "File Download Local"

    output_data = fn.NodeOutput(id="output_data", type=FileDownload)
    data = fn.NodeInput(id="data", type=fn.types.databytes)
    filename = fn.NodeInput(id="filename", type=str)

    async def func(self, data: fn.types.databytes, filename: str) -> None:
        """
        Downloads a file from a given URL and sets the "data" output to the file's content as bytes.

        Args:
          url (str): The URL of the file to download.
          timeout (float): The timeout in seconds for the download request.
        """
        self.outputs["output_data"].value = FileDownload(
            filename=filename,
            content=base64.b64encode(data).decode("utf-8"),
        )


NODE_SHELF = fn.Shelf(
    name="Files",  # The name of the shelf.
    nodes=[FileDownloadNode, FileUploadNode, FolderUploadNode, FileDownloadLocal],
    description="Nodes for working with data and files.",
    subshelves=[],
)


REACT_PLUGIN = {
    "module": os.path.join(os.path.dirname(__file__), "react_plugin", "js", "main.js"),
}
