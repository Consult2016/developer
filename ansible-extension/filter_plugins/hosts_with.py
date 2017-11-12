from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError

from ansible.plugins.filter import json_query
from jinja2 import filters
# - name: Gather Docker Nodes
#   set_fact:
#     # docker_nodes: '{{ hostvars.values() | json_query("[*].{host: inventory_hostname, docker_installed: docker_installed}") | selectattr("docker_installed", "equalto", "true") | list | json_query("[*].host") }}'
#     docker_nodes: '{{ hostvars.values() | json_query("[*].{host: inventory_hostname, docker_installed: docker_installed}")
#                       | selectattr("docker_installed", "equalto", true)
#                       | list | json_query("[*].host") }}'



def keys_of_prop(obj_list, id_prop, prop, val):
    # get a simple list
    make_simple_list = json_query.json_query(obj_list, "[*].{id: %s, %s: prop_name}" % (id_prop, unicode(prop)))
    select = filters.do_selectattr(make_simple_list, "prop_name", "equalto", val)
    new_list = filters.do_list(select)
    result = json_query.json_query(new_list, "[*].id")
    return result

def hosts_with(hostvars, prop, val):
    return keys_of_prop(hostvars.values(), id_prop='inventory_hostname', prop=prop, val=val)

class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'keys_of_prop': keys_of_prop,
            'hosts_with': hosts_with
        }
