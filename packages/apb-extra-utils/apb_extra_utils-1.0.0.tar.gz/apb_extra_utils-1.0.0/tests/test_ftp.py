import os
import unittest
from apb_extra_utils.ftp_manager import FtpManager

path_project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path_data = os.path.join(path_project, 'resources', 'data', 'sftp')


class MyTestFtp(unittest.TestCase):
    def setUp(self) -> None:
        self.host = os.getenv('TEST_HOST_FTP', 'gisnordldwf1.port.apb.es')
        self.user = os.getenv('TEST_USER_FTP', 'apbdades')
        self.psw = os.getenv('TEST_PSW_FTP', '7Y2EmuFAPzn8Xvo')
        self.port = os.getenv('TEST_PORT_FTP', 2222)
        self.path_data_remote_dir = os.getenv('TEST_PATH_REMOTE_SFTP', '/dades/test')
        self.ftp: FtpManager = FtpManager(hostname=self.host, username=self.user, password=self.psw, port=self.port)

    def test_connect_sftp(self):
        self.assertIsNotNone(self.ftp.connection)

    def test_listdir(self):
        listdir = [*self.ftp.listdir(self.path_data_remote_dir)]
        self.assertIsNotNone(listdir)

    def test_listdir_attrs(self):
        listdir_attrs = dict(self.ftp.listdir_attr(self.path_data_remote_dir))
        self.assertIsNotNone(listdir_attrs)

    def test_download_files(self):
        self.ftp.download(self.path_data_remote_dir, path_data)
        self.assertTrue(
            os.path.exists(os.path.join(path_data, os.path.basename(self.path_data_remote_dir)))
        )


if __name__ == '__main__':
    unittest.main()
