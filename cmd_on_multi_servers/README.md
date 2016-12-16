# jd_ops

Run a command on multi servers and get their reponse. these servers may have a same or 2(even 3) diffenrt passwords.

You need to input all the possible passwords(only allow 3 different passwords, if all the server has same password, please press Enter for password 2/3) for these servers.

# Usage:

./batch_op.py -f IP_LIST_FILE COMMAND

or

./batch_op.py -f IP_LIST_FILE -u USERNAME COMMAND
then you need to input all the possible passwords(only allow 3 different passwords, if all the server has same password, please press Enter for password 2/3).

# Example:
./batch_op.py -f all_searcher -u admin 'cat /proc/meminfo|grep -i memtotal'
