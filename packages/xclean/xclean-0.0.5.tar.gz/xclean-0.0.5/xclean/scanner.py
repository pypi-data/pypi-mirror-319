import os
import shutil
import sqlite3
from typing import Optional, List


class Scanner:
    """Scan the file system for duplicate files"""

    def __init__(self, *, db_path: str, clean=False):
        """
        Scanner for duplicate file detection
        :param db_path: Path to the sqlite3 database file
        :param clean: If true then delete any existing database file before starting
        """
        print('xclean: File de-duplication utility')
        print()
        if clean is True:
            if os.path.exists(db_path):
                os.remove(db_path)
        self._con = sqlite3.connect(db_path)
        self._cur = self._con.cursor()
        self._cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS DirInfo
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
            ,path TEXT NOT NULL
            ,UNIQUE (path)
            )
            '''
        )
        self._con.commit()
        self._cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS FileInfo
            (file_size INTEGER NOT NULL
            ,dir_id INTEGER NOT NULL
            ,file_name TEXT NOT NULL
            ,PRIMARY KEY (dir_id, file_name)
            )
            '''
        )
        self._con.commit()
        self._cur.execute(
            '''
            CREATE INDEX IF NOT EXISTS FileSizeNdx ON FileInfo (file_size)
            '''
        )
        self._con.commit()
        self._cur.execute(
            'SELECT COALESCE(COUNT(*), 0) AS total FROM DirInfo'
        )
        total_dirs = int(self._cur.fetchone()[0])
        self._cur.execute(
            'SELECT COALESCE(COUNT(*), 0) AS total FROM FileInfo'
        )
        total_files = int(self._cur.fetchone()[0])
        print(f'{total_dirs} main directories, {total_files} main files')
        print()

    def scan(
            self, *,
            dir_path: str,
            include: Optional[List[str]]=None,
            exclude: Optional[List[str]]=None,
    ):
        """
        Scan directory and subdirectories for main files
        :param dir_path: Path to directory to start the scan in
        :param include: Optional filename extensions to scan
        """
        dir_path = os.path.realpath(dir_path)
        print(f'Scan {dir_path} for main files')
        file_count = 0
        total_size = 0
        for root_dir, dir_names, file_names in os.walk(dir_path):
            eligible_file_names = self._eligible_file_names(root_dir, file_names, include, exclude)
            if len(eligible_file_names) > 0:
                dir_id = self._record_main_directory(root_dir)
                for file_name in eligible_file_names:
                    file_path = os.path.join(root_dir, file_name)
                    stat_info = os.stat(file_path)
                    file_size = stat_info.st_size
                    file_count += 1
                    total_size += file_size
                    self._cur.execute(
                        '''INSERT INTO FileInfo (file_size, dir_id, file_name) VALUES (?,?,?)''',
                        (file_size, dir_id, file_name)
                    )
            self._con.commit()
        print()
        print(f'{file_count:,} files scanned with {total_size:,} bytes')
        print()
        return {
            'files': {
                'count': file_count,
                'size': total_size,
            }
        }

    def _record_main_directory(self, root_dir: str) -> int:
        dir_id = self._create_directory_entry(root_dir)
        self._remove_old_directory_files(dir_id)
        return dir_id

    def _remove_old_directory_files(self, dir_id):
        self._cur.execute(
            '''DELETE FROM FileInfo WHERE dir_id = ?''',
            (dir_id,)
        )

    def _create_directory_entry(self, root_dir):
        self._cur.execute(
            '''INSERT OR IGNORE INTO DirInfo (path) VALUES (?)''',
            (root_dir,)
        )
        self._cur.execute(
            '''SELECT id FROM DirInfo WHERE path = ?''',
            (root_dir,)
        )
        dir_id = self._cur.fetchone()[0]
        return dir_id

    @staticmethod
    def _eligible_file_names(
            root_dir: str,
            file_names: List[str],
            include: Optional[List[str]],
            exclude: Optional[List[str]],
    ):
        eligible_file_names = []
        for file_name in file_names:
            if include is not None:
                _f, _ext = os.path.splitext(file_name)
                if _ext.startswith('.'):
                    _ext = _ext[1:]
                if _ext.lower() not in include:
                    continue
            if exclude is not None:
                _f, _ext = os.path.splitext(file_name)
                if _ext.startswith('.'):
                    _ext = _ext[1:]
                if _ext.lower() in exclude:
                    continue
            file_path = os.path.join(root_dir, file_name)
            if os.path.islink(file_path):
                continue
            eligible_file_names.append(file_name)
        return eligible_file_names

    def clean(
            self, *,
            dir_path: str,
            include: Optional[List[str]]=None,
            exclude: Optional[List[str]]=None,
            remove_dups=False,
            trash_dups=False,
            check_xmp=False,
            check_aae=False,
            archive_to=None,
            unprotect=False,
    ):
        """
        Scan directory and subdirectories for duplicate files
        :param dir_path: Path to directory to start the scan in
        :param include: Optional filename extensions to scan
        :param remove_dups: If true then remove the duplicate files
        :param trash_dups: If true then send duplicates to the trash
        :param check_xmp: If true then check the xmp matches as well
        :param check_aae: If true then check the aae matches as well
        :param archive_to: Path to archive duplicate files to
        """
        dir_path = os.path.realpath(dir_path)
        print(f'Scan {dir_path} for duplicates')
        dups_count = 0
        dups_size = 0
        files_count = 0
        files_size = 0
        rollback = False
        for root_dir, dir_names, file_names in os.walk(dir_path):
            self._cur.execute(
                '''SELECT di.id FROM DirInfo di WHERE di.path = ?''',
                (root_dir,)
            )
            row = self._cur.fetchone()
            if row is not None:
                if not unprotect:
                    continue  # do not clean main directories
                dir_id = int(row[0])
            else:
                dir_id = None
            eligible_file_names = self._eligible_file_names(root_dir, file_names, include, exclude)
            if len(eligible_file_names) > 0:
                for file_name in eligible_file_names:
                    files_count += 1
                    target_file_path = os.path.join(root_dir, file_name)
                    stat_info = os.stat(target_file_path)
                    file_size = stat_info.st_size
                    files_size += file_size
                    self._cur.execute(
                        '''
                        SELECT di.path, fi.file_name 
                        FROM FileInfo fi 
                        JOIN DirInfo di ON di.id = fi.dir_id 
                        WHERE fi.file_size = ?
                        ''',
                        (file_size,)
                    )
                    main_files = self._cur.fetchall()
                    for row in main_files:
                        main_dir_path = str(row[0])
                        main_file_name = str(row[1])
                        if root_dir == main_dir_path:
                            if file_name == main_file_name:
                                continue  # ignore if the scanned file is the main file
                        main_file_path = os.path.join(main_dir_path, main_file_name)
                        if self._files_are_the_same(target_file_path, main_file_path, check_xmp=check_xmp):
                            dups_count += 1
                            print()
                            print(f'  Main {main_file_path}')
                            print(f'  Dup  {target_file_path}')
                            print(f'       {dups_count:,} : (size {file_size:,})')
                            if archive_to is not None:
                                self._archive_file(target_file_path, dir_path, archive_to)
                                if check_xmp is True:
                                    xmp_file_path = Scanner._find_xmp_file(target_file_path)
                                    if xmp_file_path is not None:
                                        self._archive_file(xmp_file_path, dir_path, archive_to)
                                if check_aae is True:
                                    aae_file_path = Scanner._find_aae_file(target_file_path)
                                    if aae_file_path is not None:
                                        self._archive_file(aae_file_path, dir_path, archive_to)
                            elif trash_dups is True:
                                self._trash_file(target_file_path)
                                if check_xmp is True:
                                    xmp_file_path = Scanner._find_xmp_file(target_file_path)
                                    if xmp_file_path is not None:
                                        self._trash_file(xmp_file_path)
                                if check_aae is True:
                                    aae_file_path = Scanner._find_aae_file(target_file_path)
                                    if aae_file_path is not None:
                                        self._trash_file(aae_file_path)
                            elif remove_dups is True:
                                self._remove_file(target_file_path)
                                if check_xmp is True:
                                    xmp_file_path = Scanner._find_xmp_file(target_file_path)
                                    if xmp_file_path is not None:
                                        self._remove_file(xmp_file_path)
                                if check_aae is True:
                                    aae_file_path = Scanner._find_aae_file(target_file_path)
                                    if aae_file_path is not None:
                                        self._remove_file(aae_file_path)
                            else:
                                rollback = True
                            if dir_id is not None:
                                self._cur.execute(
                                    'DELETE FROM FileInfo '
                                    'WHERE dir_id = ? '
                                    'AND file_name = ?',
                                    (dir_id, file_name)
                                )
                                if check_xmp:
                                    xmp_file_path = Scanner._find_xmp_file(target_file_path)
                                    if xmp_file_path is not None:
                                        xmp_file_name = os.path.basename(xmp_file_path)
                                        self._cur.execute(
                                            'DELETE FROM FileInfo '
                                            'WHERE dir_id = ? '
                                            'AND file_name = ?',
                                            (dir_id, xmp_file_name)
                                        )
                                if check_aae:
                                    aae_file_path = Scanner._find_aae_file(target_file_path)
                                    if aae_file_path is not None:
                                        aae_file_name = os.path.basename(aae_file_path)
                                        self._cur.execute(
                                            'DELETE FROM FileInfo '
                                            'WHERE dir_id = ? '
                                            'AND file_name = ?',
                                            (dir_id, aae_file_name)
                                        )
                            dups_size += file_size
                            break
        print()
        print(f'{dups_count:,} of {files_count:,} duplicate files occupying {dups_size:,} bytes')
        print()
        if rollback:
            self._con.rollback()
        else:
            self._con.commit()
        return {
            'duplicates': {
                'count': dups_count,
                'size': dups_size,
            },
            'files': {
                'count': files_count,
                'size': files_size,
            },
        }

    @staticmethod
    def _remove_file(target_file_path):
        print(f'  Remove duplicate file {target_file_path}')
        os.remove(target_file_path)

    def _trash_file(self, target_file_path: str):
        trash_files_path = self.trash_directory()
        if trash_files_path is not None:
            file_name = os.path.basename(target_file_path)
            trash_file_path = os.path.join(trash_files_path, file_name)
            print(f'  Trash duplicate file {target_file_path}')
            shutil.copy2(target_file_path, trash_file_path)
            if os.path.exists(trash_file_path):
                if os.stat(trash_file_path).st_size == os.stat(target_file_path).st_size:
                    os.remove(target_file_path)

    @staticmethod
    def trash_directory():
        home = os.getenv('HOME')
        local = os.path.join(home, '.local')
        share = os.path.join(local, 'share')
        trash = os.path.join(share, 'Trash')
        trash_files_path = os.path.join(trash, 'files')
        if os.path.exists(trash_files_path):
            return trash_files_path
        return None

    @staticmethod
    def _archive_file(target_file_path: str, dir_path: str, archive_to: str):
        target_file_suffix = target_file_path[len(dir_path):]
        while target_file_suffix.startswith('/'):
            target_file_suffix = target_file_suffix[1:]
        archive_file_path = os.path.join(archive_to, target_file_suffix)
        archive_dir_path = os.path.dirname(archive_file_path)
        if not os.path.exists(archive_dir_path):
            os.makedirs(archive_dir_path, mode=0o700, exist_ok=False)
        print(f'  Archive duplicate file to {archive_file_path}')
        shutil.copy2(target_file_path, archive_file_path)
        if os.path.exists(archive_file_path):
            if os.stat(archive_file_path).st_size == os.stat(target_file_path).st_size:
                os.remove(target_file_path)

    @staticmethod
    def _files_are_the_same(source_file_path: str, target_file_path: str, check_xmp=False) -> bool:
        source_fp = os.open(source_file_path, os.O_RDONLY)
        target_fp = os.open(target_file_path, os.O_RDONLY)
        source_bytes = os.read(source_fp, 1000)
        target_bytes = os.read(target_fp, 1000)
        while source_bytes == target_bytes and len(source_bytes) > 0:
            source_bytes = os.read(source_fp, 1000)
            target_bytes = os.read(target_fp, 1000)
        os.close(source_fp)
        os.close(target_fp)
        if source_bytes != target_bytes:
            return False
        if check_xmp is True:
            return Scanner._compare_xmp(source_file_path, target_file_path)
        return True

    @staticmethod
    def _compare_xmp(source_file_path: str, target_file_path: str) -> bool:
        xmp_source_file_path = Scanner._find_xmp_file(source_file_path)
        xmp_target_file_path = Scanner._find_xmp_file(target_file_path)
        if xmp_source_file_path is None:
            if xmp_target_file_path is None:
                return True
            return False
        if xmp_target_file_path is None:
            return False
        return Scanner._files_are_the_same(xmp_source_file_path, xmp_target_file_path)

    @staticmethod
    def _find_xmp_file(file_path: str) -> Optional[str]:
        xmp_file_path = f'{file_path}.xmp'
        if os.path.exists(xmp_file_path):
            return xmp_file_path
        xmp_file_path = f'{file_path}.XMP'
        if os.path.exists(xmp_file_path):
            return xmp_file_path
        prefix, extn = os.path.splitext(file_path)
        xmp_file_path = f'{prefix}.xmp'
        if os.path.exists(xmp_file_path):
            return xmp_file_path
        xmp_file_path = f'{prefix}.XMP'
        if os.path.exists(xmp_file_path):
            return xmp_file_path
        return None

    @staticmethod
    def _find_aae_file(file_path: str) -> Optional[str]:
        aae_file_path = f'{file_path}.aae'
        if os.path.exists(aae_file_path):
            return aae_file_path
        aae_file_path = f'{file_path}.AAE'
        if os.path.exists(aae_file_path):
            return aae_file_path
        prefix, extn = os.path.splitext(file_path)
        aae_file_path = f'{prefix}.aae'
        if os.path.exists(aae_file_path):
            return aae_file_path
        aae_file_path = f'{prefix}.AAE'
        if os.path.exists(aae_file_path):
            return aae_file_path
        return None
