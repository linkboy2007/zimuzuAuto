#!/bin/bash
#zimuzu.tv自动签到程序

curl -c cookie.txt http://www.zimuzu.tv/User/Login/ajaxLogin --data-urlencode "account=${1}" --data "password=${2}&remember=1&url_back=http%3A%2F%2Fwww.zimuzu.tv%2F" http://www.zimuzu.tv/User/Login/ajaxLogin

curl -b cookie.txt -c cookie2.txt http://www.zimuzu.tv/user/sign
sleep 16

curl -b cookie2.txt http://www.zimuzu.tv/user/sign/dosign
sleep 5

rm cookie.txt cookie2.txt

exit 1

