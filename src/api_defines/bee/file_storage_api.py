from pathlib import Path
from datetime import datetime


def create_folder_year_month() -> Path:
    """
    在 'file_storage' 目录下，根据当前年月创建子文件夹（格式：file_storage/YYYY/MM）。
    如果目录已存在，则直接返回路径。

    Returns:
        Path: 指向 file_storage/YYYY/MM 目录的路径对象。
    """
    # 获取当前年月
    now = datetime.now()
    year_month_path = Path("file_storage") / str(now.year) / f"{now.month:02d}"
    
    # 创建目录（包括父目录）
    year_month_path.mkdir(parents=True, exist_ok=True)
    
    return year_month_path


def create_folder_file_ids() -> Path:
    """
    创建固定目录：file_storage/file_ids。
    如果目录已存在，则直接返回路径。

    Returns:
        Path: 指向 file_storage/file_ids 目录的路径对象。
    """
    folder_path = Path("file_storage") / "file_ids"
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def save_file(file_path: Path, file_content: bytes) -> None:
    """
    将字节内容写入指定路径的文件。

    Args:
        file_path (Path): 要写入的文件路径。
        file_content (bytes): 要写入的二进制内容。
    """
    with open(file_path, "wb") as file:
        file.write(file_content)


def read_file(file_path: Path) -> bytes:
    """
    从指定路径读取文件内容并返回字节数据。

    Args:
        file_path (Path): 要读取的文件路径。

    Returns:
        bytes: 文件的二进制内容。
    """
    with open(file_path, "rb") as file:
        return file.read()


async def upload(file_id: str, file_name: str, file_content: bytes) -> str:
    """
    上传文件并记录其 file_id 映射。

    文件保存在按年月组织的目录中，同时在 file_ids 目录下创建以 file_id 命名的元数据文件，
    其内容为实际文件的路径。

    Args:
        file_id (str): 文件的唯一标识符。
        file_name (str): 文件名（用于存储）。
        file_content (bytes): 文件的二进制内容。

    Returns:
        str: 返回传入的 file_id。
    """
    file_path = create_folder_year_month() / file_name
    file_id_path = create_folder_file_ids() / file_id
    save_file(file_path, file_content)
    save_file(file_id_path, str(file_path).encode())
    return file_id


async def delete(file_id: str) -> None:
    """
    删除指定 file_id 对应的文件及其元数据。

    先读取 file_id 对应的元数据文件获取实际文件路径，然后删除实际文件和元数据文件。
    如果文件或元数据不存在，则不做任何操作。

    Args:
        file_id (str): 要删除的文件唯一标识符。
    """
    file_id_path = create_folder_file_ids() / file_id
    if not file_id_path.exists():
        return
    
    file_path = Path(read_file(file_id_path).decode())
    file_id_path.unlink(missing_ok=True)  # 删除元数据文件
    
    if not file_path.exists():
        return
    
    file_path.unlink(missing_ok=True)  # 删除实际文件    


async def download(file_id: str) -> tuple[str,bytes]:
    """
    根据 file_id 下载对应的文件内容。

    通过 file_id 读取元数据文件，获取实际文件路径，再读取该文件内容返回。
    如果 file_id 无效或对应文件不存在，则返回空字节。

    Args:
        file_id (str): 文件的唯一标识符。

    Returns:
        file_path: 文件名称,若没找到，返回 not_found.
        bytes: 文件的二进制内容；若未找到则返回 b""。
    """
    file_id_path = create_folder_file_ids() / file_id
    if not file_id_path.exists():
        return "not_found","not_found".encode()
    
    file_path = Path(read_file(file_id_path).decode())
    
    if not file_path.exists():
        return "not_found","not_found".encode()
    
    file_name=file_path.name
    file_content=read_file(file_path)
    return file_name,file_content