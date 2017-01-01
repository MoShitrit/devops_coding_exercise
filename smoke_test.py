#!/usr/bin/env python
"""
Smoke test for NCR Cloud Development Team - DevOps Coding Exercise
This script verifies that both Consul and Redis clusters are functioning properly by connecting to each running node
from the Vagrant file (by parsing the output of 'vagrant status' command) using vagrant ssh and running the following commands:

- consul members - to verify all nodes are members of the consul cluster and are alive.

- docker exec -it sentinel redis-cli -p 5000 SENTINEL get-master-addr-by-name mymaster - To query all
   sentinel containers and make sure they all see the same redis master.

ATTENTION: Make sure to run 'vagrant up' before running the script!
"""

import argparse
import subprocess
import re

__author__ = 'Moshe Shitrit'
__creation_date__ = '1/1/17'

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.parse_args()

CHECKS_DICT = {'consul': 'consul members',
               'redis': 'docker exec -it sentinel redis-cli -p 5000 SENTINEL get-master-addr-by-name mymaster'}

FAILED_TESTS = dict()

# =========================== END GLOBAL =========================== #


class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def run_shell_cmd(cmd):
    """
    :param cmd: command to run
    :return: command output
    Run the cmd using subprocess.Popen method and return the output.
    """
    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = dict()
    output['ret_code'] = subprocess.Popen.wait(process)
    output['stdout'] = process.stdout.read().rstrip()
    output['stderr'] = process.stderr.read().rstrip()
    return output


def get_nodes():
    """
    Run 'vagrant status' command, parse the output to creat the list of running nodes.
    :return: running_nodes list.
    """

    print "{0}{1}{2}Getting the list of nodes and their status from vagrant..{3}".format(Color.BOLD,
                                                                                         Color.UNDERLINE,
                                                                                         Color.PURPLE,
                                                                                         Color.END)
    raw_results = run_shell_cmd("vagrant status")

    # Make sure that the vagrant status command succeeded, otherwise exit with error
    if raw_results['ret_code'] != 0:
        print "{0}{1}vagrant status command ended with error:\n{2}: {3}. \n" \
              "Make sure that you run the script from the same location of Vagrantfile.\n" \
              "Otherwise, act according to the aforementioned error message{4}.".format(Color.BOLD,
                                                                                        Color.RED,
                                                                                        raw_results['ret_code'],
                                                                                        raw_results['stderr'],
                                                                                        Color.END)
        exit(2)

    final_list = list()
    # Parse the stdout of the command, to make sure all nodes are running, otherwise exit with error
    for line in raw_results['stdout'].split('\n'):
        if re.search('^node[0-9]*', line):
            if not re.search('running', line):
                print "{0}{1}{2}{3} is NOT running!\n" \
                      "Make sure all nodes are up and run the test again.{4}".format(Color.RED,
                                                                                     Color.BOLD,
                                                                                     Color.UNDERLINE,
                                                                                     line.split(' ')[0],
                                                                                     Color.END)
                exit(3)
            else:
                final_list.append(line.split(' ')[0])
    banner('List of nodes to process:')
    for node in final_list:
        print node

    print
    return final_list


def run_health_check(node, check):
    """
    :param node: The node to check
    :param check: The key to checks_dict, from which the relevant command will be taken.
    :return:
    """
    print "{0}{1}{2}Running {3} check on {4}..{5}\n".format(Color.BOLD,
                                                            Color.UNDERLINE,
                                                            Color.PURPLE,
                                                            check,
                                                            node,
                                                            Color.END)
    command = 'vagrant ssh {0} -c "{1}"'.format(node, CHECKS_DICT[check])
    output = run_shell_cmd(command)
    if output['ret_code'] == 0:
        print output['stdout']
    else:
        print '{0}{1}Command exited with ERROR: {2}, {3}{4}'.format(Color.BOLD,
                                                                    Color.YELLOW,
                                                                    output['stdout'],
                                                                    output['stderr'],
                                                                    Color.END)
        if node not in FAILED_TESTS.keys():
            FAILED_TESTS[node] = dict()
        FAILED_TESTS[node][check] = output


def banner(message, border='-'):
    """Get a message as an argument, print it with borders.."""
    line = '+' + border * (len(message) + 2) + '+'
    print (line)
    print('| ' + message + ' |')
    print(line)


def main():
    try:
        banner("Smoke test for NCR Cloud Development Team - DevOps Coding Exercise")
        nodes_list = get_nodes()
        for node in nodes_list:
            banner('Starting check sequence on {0}'.format(node))
            for key in CHECKS_DICT.keys():
                run_health_check(node, key)
                print '\n{0}\n'.format('='*30)

        banner("Smoke test complete")
        print
        # Check if there are any failed tests, if there are - print them
        if bool(FAILED_TESTS):
            print "{0}{1}{2}Smoke test ended with some failures, " \
                  "below are the results of FAILED checks:{3}\n".format(Color.BOLD,
                                                                      Color.UNDERLINE,
                                                                      Color.YELLOW,
                                                                      Color.END)
            for node in FAILED_TESTS.keys():
                print "{0}{1}{2}{3}{4}".format(Color.BOLD, Color.UNDERLINE,
                                               Color.PURPLE, node, Color.END)
                for check in FAILED_TESTS[node]:
                    print '{0}: {1}'. format(check, FAILED_TESTS[node][check])
                print
        else:
            print "{0}{1}{2}ALL CHECKS PASSED!{3}".format(Color.BOLD,
                                                          Color.UNDERLINE,
                                                          Color.GREEN,
                                                          Color.END)
    except KeyboardInterrupt:
        print ("\n{0}{1}CTRL + C was pressed, exiting..{2}".format(Color.BOLD, Color.YELLOW, Color.END))
        exit(77)

    finally:
        print
        banner('Goodbye!')
        print

if __name__ == '__main__':
    main()
