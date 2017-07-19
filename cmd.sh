#!/bin/bash
searcher_ip_list=$1

IP_LIST=`cat $searcher_ip_list`
for dst_ip in ${IP_LIST[@]}; do
    echo -e "[ $dst_ip ]    \c"

    #ssh ${dst_ip} "/bin/sh /export/App/jd_search/merger/main_update/bin/start.sh update_server_zmonitor_stop"

    #scp main_update.conf admin@$dst_ip:/export/App/jd_search/searcher/main_update/conf/
    #rsync -avr searcher_common.ini ${dst_ip}:/export/App/jd_search/searcher/
    #rsync -avr searcher_common.sh ${dst_ip}:/export/App/jd_search/searcher/
    #rsync -avr nodes.xml ${dst_ip}:/export/App/jd_search/searcher/server/conf/

    #删除日志
    #ssh ${dst_ip} "cd /export/Logs/jd_search/searcher/ && \rm -rf * && ls"

	
    #ssh ${dst_ip} "md5sum /export/App/jd_search/searcher/server/bin/searcher_server"
    #ssh ${dst_ip} "md5sum /export/App/jd_search/searcher/server/conf/server.ini" 

    #ssh ${dst_ip} "curl localhost:10103/info 2>/dev/null | grep 上次全量更新数据的时间"
    #ssh ${dst_ip} 'curl localhost:10103/info 2>/dev/null | egrep "(当前全量|最新|so版本号|compile_date)" | md5sum'

    #设定crontab
    #ssh ${dst_ip} "crontab -l | grep -v update_main.sh | crontab -"   #删除全量更新脚本
    #ssh ${dst_ip} "(crontab -l ; echo '0 8 * * * /bin/sh /export/App/jd_search/searcher/main_update/bin/update_main.sh > /dev/null 2>&1') | crontab -"   #添加全量更新脚本
    
done
