import smtplib
import random
import time
from email.header import Header
from email.mime.text import MIMEText
import re

string = 'ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz'

def email(T_QQ):
    def QQ_mail(T_QQ, F_user, T_user, subject, message):
        sender = 'krismile_ibelieve@qq.com'  # 配置发送邮件地址,显示--由xxx@xxx.com代发
        password = "sprzntsgpowkbfgb"  # 客户端登录专用密码
        receivers = [T_QQ]  # 邮件接收地址
        SMTP_server = "smtp.qq.com"

        port = 465

        # MIME设置
        post_message = MIMEText(message, "html", "utf-8")
        post_message["From"] = Header(F_user, "utf-8", header_name="linjm@krcon.cn")  # 显示--发件人:这是发件人
        post_message["To"] = Header(T_user, "utf-8")  # 显示--收件人:这是收件人
        post_message["Subject"] = Header(subject, "utf-8")

        # 邮件发送
        try:
            flag = True
            server = smtplib.SMTP_SSL(SMTP_server, port)
            server.login(sender, password)  # 登录邮件服务器
            server.sendmail(sender, receivers, post_message.as_string())  # 发送邮件
            server.quit()
        except Exception as e:
            flag = False
        if flag:
            print('邮件发送成功')
        else:
            print('邮件发送失败')


    security_code = ''
    for i in range(6):
        L = list(string)
        security_code += random.choice(L)

    while True:
        ex = "^\w+[-_.]*[a-zA-Z0-9]+@qq+\.[a-zA-Z]{2,3}$"
        if re.findall(ex, T_QQ, re.S):
            QQ_mail(T_QQ, '商店管理系统', T_QQ, '验证码', '你好,你的验证码为:' + security_code)
            break
        else:
            return -1
    return security_code