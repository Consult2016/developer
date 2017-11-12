#!/usr/bin/python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import fcntl
import getpass

from ansible.inventory.host import Host
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.action.copy import ActionModule as CopyActionModule
from ansible.plugins.connection.local import Connection as LocalConnection

class ActionModule(CopyActionModule):
    def _local_get_url (self, task_vars, task_args):
        loader = self._loader
        variable_manager = self._task._variable_manager
        inventory = variable_manager._inventory
        # host = inventory.get_host(task_vars['inventory_hostname'])
        play_context = self._play_context

        cached  = task_args.get('cached', None)
        play = self._task._role._play
        # local_connection = LocalConnection(play_context=play_context, new_stdin=None)
        host_connection = LocalConnection(play_context=play_context, new_stdin='/dev/null')

        # Update task_args
        new_task_args = task_args.copy()
        new_task_args.pop('cached')
        new_task_args['dest'] = cached

        # Save call-context
        old = dict()
        old['delegate_to'] = self._task.delegate_to
        # old['delegated_vars'] = task_vars.get('ansible_delegated_vars', None)
        old['_connection'] = self._connection # -> local-connection
        old['connection'] = play_context.connection # -> local
        old['remote_addr'] = play_context.remote_addr # -> localhost
        old['remote_user'] = play_context.remote_user # -> current-user

        try:
            # Set call-context
            self._task.delegate_to='localhost'
            self._connection = host_connection
            play_context.connection = 'local'
            play_context.remote_addr = 'localhost'
            play_context.remote_user = getpass.getuser()

            host = Host('localhost')
            new_task_vars = variable_manager.get_vars(play=play, host=host, task = self._task)
            module_ret = self._execute_module(module_name="get_url",
                                              module_args=new_task_args,
                                              task_vars=new_task_vars,
                                              tmp=None)
        finally:
            # Un-Set call-context
            self._task.delegate_to=old['delegate_to']
            self._connection = old['_connection']
            play_context.connection = old['connection']
            play_context.remote_addr = old['remote_addr']
            play_context.remote_user = old['remote_user']

        return module_ret

    def run(self, tmp=None, task_vars=None):
        ''' handler for file transfer operations '''
        if task_vars is None:
            task_vars = dict()

        orig_args = self._task.args.copy()
        # orig_args = copy.deepcopy(self._task.args)
        args = self._task.args
        args.pop('cached')

        cached  = orig_args.get('cached', None)
        b_cache_path = to_bytes(cached, errors='surrogate_or_strict')
        cache_exist = os.path.exists(b_cache_path)

        call_path = []
        cached_file_lock = cached + ".lock"
        if not cache_exist:
            lock_file = open(cached_file_lock, "w")
            lock_file.write("0")
            lock_file.close()

            try:
                lock_file = open(cached_file_lock, "r")
                lock_fd = lock_file.fileno()

                fcntl.flock(lock_fd, fcntl.LOCK_EX)
                cache_exist = os.path.exists(b_cache_path)
                if not cache_exist :
                    self._local_get_url(task_vars, orig_args)
                    call_path.append('local.get_url')
                    os.remove(cached_file_lock)
            finally:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_file.close()

        cache_exist = os.path.exists(b_cache_path)
        if cache_exist:
            args['src'] = cached
            args.pop('url')
            if args.has_key('headers'):
                args.pop('headers')
            result = super(ActionModule, self).run(tmp, task_vars)
            call_path.append('copy')
        else:
            result = self._execute_module(module_name="get_url",
                                              module_args=args,
                                              task_vars=task_vars,
                                              tmp=tmp)
            call_path.append('remote.get_url')
        path_msg = ", ".join(call_path)
        path_msg = result.get('msg', '') + "(Call-path: " + path_msg + ")"
        result['msg'] = path_msg
        result['_ansible_verbose_always'] = True
        return result
