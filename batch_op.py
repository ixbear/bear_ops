#!/usr/bin/python
__author__ = "https://zhukun.net"
import getpass
import sys
import StringIO
from optparse import OptionParser
from multiprocessing import Process
from multiprocessing import Queue

import traceback

try:
    import paramiko
except ImportError:
    sys.stderr.write('SYS: Import lib paramiko first.\n')
    sys.exit()


class RemoteTask(object):
    def __init__(self, ip, user, pwd_lst, cmd, timeout=5):
        self.ip = ip
        self.user = user
        self.pwd_lst = pwd_lst[:]
        self.cmd = cmd
        self.timeout = timeout


class TaskResult(object):
    def __init__(self, task):
        self.task = task
        self.sout = None
        self.serr = None
        self.rc = None

task_q = Queue()
result_q = Queue()

def work(task_q, result_q):
    while True:
        task = task_q.get()
        result = TaskResult(task)
        rc = 0
        sout = ''
        serr = ''
        try:
            rc, sout, serr = run_cmd(task)
        except Exception as e:
            s = StringIO()
            traceback.print_exc(file=s)
            rc = -1
            sout = ''
            serr = s.getvalue()
            s.close()
        finally:
            result = TaskResult(task)
            result.rc = rc
            result.sout = sout
            result.serr = serr
            result_q.put(result)


def run_cmd(task):
    connected = False
    ip = task.ip

    rc = -1
    sout = ''
    serr = ''

    for password in task.pwd_lst:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=ip, port=22, username=task.user, password=password)
            stdin, stdout, stderr = client.exec_command(cmd)
            connected = True
            break
        except paramiko.AuthenticationException as e:
            connected = False
            rc = -1
            serr = 'SSH authentication failed\n'
            continue
        except Exception as e:
            rc = -1
            serr = 'Run cmd exception %s\n' % e
            connected = False
            continue

    if connected == True:
        sout = stdout.read()
        serr = stderr.read()
        rc = stdout.channel.recv_exit_status()

    return rc, sout, serr


def process_result(result):
    #log_result(result)
    print_result(result)

def log_result(result):
    ip = result.task.ip
    try:
        rc_file = open('./log/%s.rc' % ip)
        rc_file.write('%s' % result.rc)
        rc_file.close()
    finally:
        pass

    try:
        out_file = open('./log/%s.out' % ip)
        out_file.write(result.sout)
        out_file.close()
    finally:
        pass

    try:
        err_file = open('./log/%s.err' % ip)
        err_file.write(result.out)
        err_file.close()
    finally:
        pass

def print_result(result):
    ip = result.task.ip
    rc = result.rc
    sout= result.sout
    serr = result.serr

    if rc != 0:
        sys.stderr.write('{ip}|exitcode|{rc}\n'.format(ip=ip, rc=rc))
    for line in sout.splitlines():
        print '{ip}|stdout|{line}'.format(ip=ip, line=line)

    for line in serr.splitlines():
        sys.stderr.write('{ip}|stderr|{line}\n'.format(ip=ip, line=line))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="ipfile",
                  help="IP list file", metavar="IPLIST")
    parser.add_option('-u', '--user', dest='user', default='admin',
                      help='Username to logon server', metavar='USER')
    parser.add_option('-b', '--trybest', dest='trybest', action='store_true', default=False,
                      help='Try best to finish task', metavar='TRYBEST')
    parser.add_option('-n', '--num_worker', dest='num_worker', default=16,
                      help='Number of worker', metavar='NUM_WORKER')

    options, args = parser.parse_args()
    if not options.ipfile:
        parser.error('IPFILE must be present.')

    ipfile = options.ipfile
    username = options.user
    try_best = options.trybest
    num_worker = options.num_worker

    cmd = ' '.join(args)

    password_lst = []
    index = 1
    while True:
        password = getpass.getpass(prompt='Password %s:' % index)
        index += 1
        if password != '':
            password_lst.append(password)
            continue
        else:
            break

    ip_list = []
    ip_list.extend([ x.strip() for x in open(ipfile).read().splitlines() ])

    pool = []
    for x in xrange(num_worker):
        worker = Process(target=work, args=(task_q, result_q))
        worker.daemon = True
        pool.append(worker)

    tasks = []
    for ip in ip_list:
        task = RemoteTask(ip, username, password_lst, cmd)
        task_q.put(task)

    for worker in pool:
        worker.start()

    res_num = 0
    while res_num < len(ip_list):
        result = result_q.get()
        process_result(result)
        res_num += 1

    for worker in pool:
        worker.terminate()

    for worker in pool:
        worker.join()
