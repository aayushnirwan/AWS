#!/bin/sh
#
# Startup script for the Apache Web Server
#
# chkconfig: 345 85 15
# description: Apache is a World Wide Web server.  It is used to serve 
#          HTML files and CGI.
# processname: httpd
# pidfile: /var/run/httpd.pid
# config: /etc/httpd/conf/httpd.conf
 
# Source function library.
./etc/rc.d/init.d/functions
 
# See how we were called.
case "$1" in
start)
echo -n "Starting httpd: "
daemon httpd -DSSL
echo
touch /var/lock/subsys/httpd
;;
stop)
echo -n "Shutting down httpd: "
killproc httpd
echo
rm -f /var/lock/subsys/httpd
rm -f /var/run/httpd.pid
;;
status)
status httpd
;;
restart)
$0 stop
$0 start
;;
reload)
echo -n "Reloading httpd: "
killproc httpd -HUP
echo
;;
*)
echo "Usage: $0 {start|stop|restart|reload|status}"
exit 1
esac
 
exit 0
