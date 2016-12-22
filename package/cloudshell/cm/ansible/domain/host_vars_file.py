import os
from logging import Logger
from file_system_service import FileSystemService


class HostVarsFile(object):
    FOLDER_NAME = 'hosts_vars'
    ANSIBLE_USER = 'ansible_user'
    ANSIBLE_PASSWORD = 'ansible_ssh_pass'
    ANSIBLE_CONNECTION = 'ansible_connection'
    ANSIBLE_CONNECTION_FILE = 'ansible_ssh_private_key_file'

    def __init__(self, file_system, host_name, logger):
        """
        :type file_system: FileSystemService
        :type host_name: str
        :type logger: Logger
        """
        self.file_system = file_system
        self.logger = logger
        self.file_path = os.path.join(HostVarsFile.FOLDER_NAME, host_name)
        self.vars = {}

    def __enter__(self):
        self.logger.info('Creating \'%s\' vars file ...' % self.file_path)
        return self

    def __exit__(self, type, value, traceback):
        if not self.file_system.exists(HostVarsFile.FOLDER_NAME):
            self.file_system.create_folder(HostVarsFile.FOLDER_NAME)
        with self.file_system.create_file(self.file_path) as file_stream:
            lines = ['---']
            for key, value in sorted(self.vars.iteritems()):
                lines.append(str(key) + ': ' + str(value))
            file_stream.writelines(lines)
            self.logger.debug(os.linesep.join(lines))
        self.logger.info('Done.')

    def add_vars(self, vars):
        self.vars.update(vars)

    def add_connection_type(self, connection_type):
        self.vars[HostVarsFile.ANSIBLE_CONNECTION] = connection_type

    def add_conn_file(self, file_path):
        self.vars[HostVarsFile.ANSIBLE_CONNECTION_FILE] = file_path

    def add_username(self, username):
        self.vars[HostVarsFile.ANSIBLE_USER] = username

    def add_password(self, password):
        self.vars[HostVarsFile.ANSIBLE_PASSWORD] = password