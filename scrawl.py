#coding=utf-8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import datetime
#email 构造邮件
#smtplib 发送邮件
# 输入Email地址和口令:
from_addr = '***********@aliyun.com'
password = '************'
# 输入收件人地址:
to_addr = '**********@qq.com'
# 输入SMTP服务器地址:
smtp_server = 'smtp.aliyun.com'
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def sleeptime(h, m, s):
    return 3600 * h + 60 * m + s
def strcmp(s1, s2):
	i = 0
	while i < len(s1):
		#print(s1[i] + "   " + s2[i])
		if s1[i] < s2[i]:
			return -1
		elif s1[i] > s2[i]:
			return 1
		i += 1
	if i == len(s1):
		return 0
second = sleeptime(0, 0, 2);
i = 0
j = 0
link = [
			["http://int.bupt.edu.cn/list/list.php?p=1_3_1", '.h35','网研院官网'],
			["http://yzb.bupt.edu.cn/list/list.php?p=2_1_1", '.h28','北邮研招网']
]
t1 = '2000-03-31'
t2 = '2000-03-31'
flag = 1
while 1==1:
	time.sleep(second)
	now = datetime.datetime.now()
	today = now.strftime('%Y-%m-%d')
	current = now.strftime('%Y-%m-%d %H:%M:%S')
	for item in link:
		flag += 1
		pref = item[0]
		tag = item[1]
		website = item[2]
		res = requests.get(pref)
		soup = BeautifulSoup(res.text, "html.parser")
		#print(soup.select('.marr10').size)
		notification = soup.select(tag)
		#print(notification)
		day = notification[0].select('.rt')[0].text
		title = notification[0].get('title')

		server = smtplib.SMTP(smtp_server,25)
		#server.set_debuglevel(1)
		server.login(from_addr, password)
		print("day "+ day + "today: " + today )
		if day == today:
			if flag % 2 == 0:
				print("***网研院")
				if strcmp(t1, day) == 0:
					print("网研院：发过了")
					continue
				elif strcmp(t1, day) < 0:
					print("网研院：没发过 要发，更新t1")
					t1 = today
			if flag % 2 != 0:
				print("***北邮研招网")
				if strcmp(t2, day) == 0:
					print("北邮研招网:发过了")
					continue
				elif strcmp(t2, day) < 0:
					print("北邮研招网：没发过 要发，更新t2")
					t2 = today					
			temp = '%s\nThere is a new message from TecentYun and this is %s times mail\n\t%s'%(title, j, current)
			msg = MIMEText(temp, 'plain', 'utf-8')
			msg['From'] = _format_addr('TencentCloud <%s>' % from_addr)
			msg['To'] = _format_addr('管理员 <%s>' % to_addr)
			msg['Subject'] = Header(website, 'utf-8').encode()
			server.sendmail(from_addr, [to_addr], msg.as_string())
			server.quit()
			print('Sent\nj = ' + str(j) + " times      ----------------YES\t" + str(current))
			j += 1
		else:
			print("NoSent")
			print('i = ' + str(i))
			i += 1
