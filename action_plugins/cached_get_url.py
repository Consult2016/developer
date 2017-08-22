from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.action.copy import ActionModule as CopyActionModule

class ActionModule(CopyActionModule):
    def  run(self, tmp=None, task_vars=None):
        ''' handler for file transfer operations '''
        if task_vars is None:
            task_vars = dict()

        cached  = self._task.args.get('cached', None)
        b_cache_path = to_bytes(cached, errors='surrogate_or_strict')

        args = self._task.args
        args.pop('cached')
        if os.path.exists(b_cache_path):
            args['src'] = cached
            args.pop('url')
            if args.has_key('headers'):
                args.pop('headers')
            result = super(ActionModule, self).run(tmp, task_vars)
            return result
        else:
            task_vars_local = dict(task_vars)
            module_ret = self._execute_module(module_name="get_url",
                                              module_args=args, task_vars=task_vars, tmp=tmp)
            return module_ret
