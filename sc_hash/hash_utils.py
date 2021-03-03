#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

#  The MIT License (MIT)
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import csv
import hashlib
import logging
import os


class HashUtils:
    DEFAULT_HASH_NAME = "sha1"
    DEFAULT_EXTENSION = '.jar'

    @staticmethod
    def generate_hash(lib_paths, hash_name=DEFAULT_HASH_NAME):
        report_file = 'lib-hash.csv'
        logging.getLogger(__name__).info('generating hash...')
        with open(report_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['File Name', hash_name])
            for lib_path in lib_paths:
                hash_values = HashUtils.scan_directory(lib_path, hash_name=hash_name)
                for file_and_hash in hash_values:
                    filename = file_and_hash['filename']
                    hash_value = file_and_hash[hash_name]
                    writer.writerow([filename, hash_value])
        logging.getLogger(__name__).info('generate hash done')

    @staticmethod
    def calculate_hash(hash_name, file_path_or_handle):
        """
        Calculate a hash for the given file.

        :param hash_name: name of the hash algorithm in hashlib
        :type hash_name: str
        :param file_path_or_handle: source file name (:py:obj:`str`) or file
            handle (:py:obj:`file-like`) for the hash algorithm.
        :type file_path_or_handle: str
        :return: the calculated hash
        :rtype: str
        """

        def _hash(_fd):
            h = hashlib.new(hash_name)
            while True:
                str_read = _fd.read(8096)
                if not str_read:
                    break
                else:
                    h.update(str_read)
            return h.hexdigest()

        if hasattr(file_path_or_handle, 'read'):
            return _hash(file_path_or_handle)
        else:
            with open(file_path_or_handle, 'rb') as fd:
                return _hash(fd)

    @staticmethod
    def scan_directory(root_directory, *, calculate_hash=True, hash_name=DEFAULT_HASH_NAME):
        results = []
        normalized_directory = os.path.normpath(root_directory)
        logging.getLogger(__name__).info('scan directory %s', normalized_directory)
        try:
            directories = os.scandir(normalized_directory)
            for directory in directories:
                if directory.is_dir():
                    continue
                logging.getLogger(__name__).info('%s is a file', directory.name)
                if os.path.splitext(directory.name.lower())[1] == HashUtils.DEFAULT_EXTENSION:
                    logging.getLogger(__name__).info('found a dependency %s', directory.name)
                    checksum = ""
                    if calculate_hash:
                        checksum = HashUtils.calculate_hash(hash_name, directory.path)
                    results.append({
                        'filename': directory.path,
                        hash_name: checksum,
                        'simple_name': directory.name,
                    })
        except Exception as e:
            logging.getLogger(__name__).exception("Failed to scan directory %s", normalized_directory, exc_info=e)
        return results
