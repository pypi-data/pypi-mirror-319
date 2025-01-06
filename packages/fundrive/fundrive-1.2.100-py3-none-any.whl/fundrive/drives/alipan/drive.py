import subprocess
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fundrive.core import BaseDrive, DriveFile
from funsecret import read_secret
from funutil import getLogger

logger = getLogger("fundrive")


class AlipanDrive(BaseDrive):
    def __init__(self, *args, **kwargs):
        super(AlipanDrive, self).__init__(*args, **kwargs)
        from aligo import Aligo

        self.drive = Aligo()

    def login(
        self, server_url=None, refresh_token=None, is_resource=False, *args, **kwargs
    ) -> bool:
        refresh_token = refresh_token or read_secret(
            "fundrive", "drives", "alipan", "refresh_token"
        )
        try:
            from aligo import Aligo
        except Exception as e:
            logger.error(e)
            subprocess.check_call(["pip", "install", "fundrive-alipan"])
            from aligo import Aligo
        self.drive = Aligo(refresh_token=refresh_token)
        if is_resource:
            logger.info("使用资源盘")
            self.drive.default_drive_id = self.drive.v2_user_get().resource_drive_id
        return True

    def mkdir(self, fid, name, return_if_exist=True, *args, **kwargs) -> str:
        dir_map = dict([(file.name, file.fid) for file in self.get_dir_list(fid=fid)])
        if name in dir_map:
            logger.info(f"name={name} exists, return fid={fid}")
            return dir_map[name]
        return self.drive.create_folder(parent_file_id=fid, name=name).file_id

    def delete(self, fid, *args, **kwargs) -> bool:
        self.drive.move_file_to_trash(file_id=fid)
        return True

    def exist(self, fid, *args, **kwargs) -> bool:
        return self.drive.get_file(file_id=fid) is not None

    def get_file_list(self, fid="root", *args, **kwargs) -> List[DriveFile]:
        result = []
        for file in self.drive.get_file_list(parent_file_id=fid):
            if file.type == "file":
                result.append(
                    DriveFile(
                        fid=file.file_id,
                        name=file.name,
                        size=file.size,
                        ext=file.to_dict(),
                    )
                )
        return result

    def get_dir_list(self, fid="root", *args, **kwargs) -> List[DriveFile]:
        result = []
        for file in self.drive.get_file_list(parent_file_id=fid):
            if file.type == "folder":
                result.append(
                    DriveFile(fid=file.file_id, name=file.name, size=file.size)
                )
        return result

    def get_file_info(self, fid, *args, **kwargs) -> DriveFile:
        res = self.drive.get_file(file_id=fid)
        return DriveFile(fid=res.file_id, name=res.name, size=res.size)

    def get_dir_info(self, fid, *args, **kwargs) -> DriveFile:
        res = self.drive.get_file(file_id=fid)
        return DriveFile(fid=res.file_id, name=res.name, size=res.size)

    def download_file(self, fid, local_dir, overwrite=False, *args, **kwargs) -> bool:
        self.drive.download_file(file_id=fid, local_folder=local_dir)
        return True

    def upload_file(
        self, local_path, fid, recursion=True, overwrite=False, *args, **kwargs
    ) -> bool:
        self.drive.upload_file(
            file_path=local_path,
            parent_file_id=fid,
            check_name_mode="overwrite" if overwrite else "refuse",
        )
        return True

    def share(self, *fids: str, password: str, expire_days: int = 0, description=""):
        now = datetime.now(timezone.utc) + timedelta(days=expire_days)
        expiration = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

        self.drive.share_files(
            [fid for fid in fids], share_pwd=password, expiration=expiration
        )

    def save_shared(self, shared_url: str, fid: str, password: Optional[str] = None):
        r = self.drive.share_link_extract_code(shared_url)
        r.share_pwd = password or r.share_pwd
        self.drive.share_file_save_all_to_drive(share_token=r, to_parent_file_id=fid)
