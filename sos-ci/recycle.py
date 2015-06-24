import os
import subprocess

import log

from iniparse import INIConfig

fdir = os.path.dirname(os.path.realpath(__file__))
conf_dir = os.path.dirname(fdir)
cfg = INIConfig(open(conf_dir + '/sos-ci.conf'))

""" EZ-PZ just call our ansible playbook.

Would be great to write a playbook runner at some point, but
this is super straight forward and it works so we'll use it for now.

"""


def just_doit(instance_name):
    """ Do the dirty work, or let ansible do it. """

    logger = log.setup_logger('%s - ansible.out' % instance_name)
    logger.debug('Attempting ansible tasks on instance-name: %s', instance_name)
    vars = "instance_name=%s" % instance_name
    cmd = '/usr/bin/ansible-playbook -vvv --extra-vars '\
          '\"%s\" %s/stackit.yml' % (vars, cfg.Ansible.ansible_dir)

    logger.debug('Running ansible stackit command: %s', cmd)
    ansible_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = ansible_proc.communicate()[0]
    logger.debug('Response from ansible: %s', output)

    #do not teardown the error instances
    if output.find('Error') != -1:
        return output

    vars = "instance_name=%s" % instance_name
    cmd = '/usr/bin/ansible-playbook --extra-vars '\
          '\"%s\" %s/teardown.yml' % (vars, cfg.Ansible.ansible_dir)

    logger.debug('Running ansible teardown command: %s', cmd)
    ansible_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output += ansible_proc.communicate()[0]

    return output
    
if __name__ == '__main__':
    for i in xrange(10):
        instance_name = 'instance-' + str(i)
        just_doit(instance_name)
