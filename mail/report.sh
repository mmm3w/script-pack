#!/bin/bash
email_reciver="psnhewzc@gmail.com"
#发送者邮箱
email_sender="877062007@qq.com"
#邮箱用户名
email_username="LinuxReport"
#邮箱密码
#使用qq邮箱进行发送需要注意：首先需要开启：POP3/SMTP服务，其次发送邮件的密码需要使用在开启POP3/SMTP服务时候腾讯提供的第三方客户端登陆码。
email_password="mschpvoiusmfbdjf"
#smtp服务器地址
email_smtphost="smtp.qq.com"
email_title="iOS客户端更新"
email_content="谢谢!"

sendEmail -f 877062007@qq.com -t psnhewzc@gmail.com -s smtp.qq.com -u test -xu LinuxReport -xp mschpvoiusmfbdjf -m content -o message-charset=utf-8
