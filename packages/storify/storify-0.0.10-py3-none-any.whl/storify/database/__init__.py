import msgpack
import os
import time
import shutil

from ..exceptions import *
from .backups import Backups
from ..model import Model

class Database:
    def __init__(self, name=None, path=None, root=None, log=None, rootdata={}, models=[]):
        if name is None and path is None and root is None:
            raise ValueError("At least 'path', or 'name' and 'root' must be provided.")
        
        self.name = name
        self._path = path
        self.root = root
        self.data = rootdata
        self.backups = None
        self.log = log
        self.models = models

        self.last_flush = time.time()
        self.destroyed = False
        self.defunct = False

        self.backups = Backups(self)

        self.load()

    @property
    def path(self):
        if self._path:
            return self._path

        return os.path.join(self.root, "%s.mpack" % self.name)

    def load(self, path=None):
        """
        Load the database from a file.

        :param path: The path to the database file. If not provided, defaults to the standard path based on the database name.
        :type path: str, optional
        :raises DatabaseLoadError: If the database cannot be loaded from the main file or any backups.

        Typically, you don't need to call this yourself. This method attempts to load the database from the specified file. 
        If the main file is corrupted, it tries to load from available backups. If all attempts fail, it raises a DatabaseLoadError.
        """
        if not path:
            path = self.path

        if os.path.exists(path):

            try:
                self.data = self.unpack(path)
            except:
                self.log.traceback("Database '%s' corrupted, reading from backup" % self.name)

                # Read from backups
                for backup_id in self.backups.list:
                    backup_path = self.backups.get_path_of_backup(backup_id)

                    try:
                        self.log.warning("Reading from backup '%s'" % backup_id)
                        self.data = self.unpack(backup_path)

                        self.log.warning("Successfully loaded backup '%s'" % backup_id)
                        return
                    except:
                        self.log.error("Failed to read backup")
                        continue

                self.log.error("Failed to load database, throwing DatabaseLoadError")
                raise DatabaseLoadError("Could not load db:%s" % self.name)
          
    def encode_type(self, data):
        if isinstance(data, dict):
            return {walk(key): walk(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [walk(item) for item in data]
        elif isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif isinstance(data, Model):
            return {data._keyname(): data._to_dict()}  # Serialize Model instances
        elif isinstance(data, type) and issubclass(data, Model):
            return {data._keyname(): data._to_dict()}  # Serialize subclassed Model instances
        
        return data
    
    def decode_type(self, data):
        if isinstance(data, dict):
            model_class = next((cls for cls in self.models if cls._keyname() in data), None)

            if model_class is None:
                return data

            try:
                return model_class()._from_dict(data[model_class._keyname()])
            except Exception as e:
                self.log.traceback(f"Failed to decode model: {data} with error: {str(e)}")
                return data
        
        return data
    
    def unpack(self, path, raw=False):
        try:
            with open(path, "rb") as f:
                blob = msgpack.unpackb(
                    f.read(),
                    object_hook=self.decode_type,
                    raw=raw
                )
        except UnicodeDecodeError:
            self.log.error("Failed to read database due to a UnicodeDecodeError. Attempting to read the database again with raw=True. Please ensure the database file is not corrupted or in an unsupported format.")
            return self.unpack(path, raw=True)

        # Walk the blob, fix bytes > str
        def walk(b):
            if isinstance(b, dict):
                new_dict = {}

                for key in b:
                    value = walk(b[key])

                    if isinstance(key, bytes):
                        key = key.decode("utf8")

                    if key in new_dict:
                        if isinstance(value, (str, bytes, list, dict)):
                            if len(value) < 1:
                                print("Skipping conflicting key %s because it's empty" % key)
                                continue

                    new_dict[key] = value

                return new_dict

            elif isinstance(b, list):
                return [walk(item) for item in b]

            elif isinstance(b, bytes):
                try:
                    return b.decode("utf8")
                except:
                    return b

            else:
                return b

        return walk(blob)
    
    def flush(self):
        """Flush the database to disk.

        Writes all pending changes in the database to disk storage. Creates a temporary file,
        writes the data, and then safely moves it to the final location. Before writing, creates
        a backup of the existing database file if one exists.

        If the database has been marked as destroyed or defunct, returns without performing
        any operations.

        :raises IOError: If there is an error writing the data to disk, typically due to insufficient storage space
        """
        if self.destroyed or self.defunct:
            return

        # Save code here
        final_path = self.path
        tmp_path = self.path + ".tmp"

        # Backup before flushing
        if os.path.exists(final_path):
            self.log.debug("Backing up db...")
            self.backups.backup()

        try:
            with open(tmp_path, "wb") as f:
                self.log.warning("Syncing data to disk")

                blob = msgpack.packb(
                    self.data,
                    default=self.encode_type
                )

                f.write(blob)

            shutil.copy(tmp_path, final_path)
            os.remove(tmp_path)

            self.last_flush = time.time()
        except IOError:
            self.log.traceback(
                "An error occurred while attempting to write data to disk. "
                "This may be due to insufficient storage space. Please ensure "
                "there is adequate space available before retrying the operation."
            )

            self.log.debug(f"tmp_path: {tmp_path}")
            self.log.debug(f"final_path: {final_path}")

            # Try to clean up
            try:
                os.remove(tmp_path)
            except:
                pass

    def close(self):
        """
        Close the database.
        
        Flushes the database to disk and marks it as defunct. After closing,
        the database can no longer be used.
        """
        self.flush()

        self.data = None
        self.defunct = True

    def destroy(self):
        """
        Destroy the database.
        
        Deletes the database file from disk. This operation cannot be undone,
        but backups are preserved.
        """
        self.close()

        path = os.path.join(self.root, "%s.mpack" % self.name)

        if os.path.exists(path):
            os.remove(
                path
            )

    def append(self, *args, **kwargs):
        self.data.append(*args, **kwargs)

    def remove(self, **kwargs):
        self.data.remove(**kwargs)

    def pop(self, i):
        return

    def __getitem__(self, index):
        if not (type(index) in (str, bytes)):
            raise ValueError("Expected str or bytes, got %s" % type(index))
        
        val = self.data[index]

        # TODO: Recursively fix any unneccessarily bytes types

        return val

    def __setitem__(self, index, value):
        if not (type(index) in (str, bytes)):
            raise ValueError("Expected str or bytes, got %s" % type(index))

        self.data[index] = value
        return self.data[index]

    def __delitem__(self, index):
        if not (type(index) in (str, bytes)):
            raise ValueError("Expected str or bytes, got %s" % type(index))

        del self.data[index]

    def __iter__(self):
        for i in self.data:
            yield i

    def __len__(self):
        return len(self.data)
