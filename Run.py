from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import Ui_login
from Emaill import *
import pymysql
import Ui_adm
import Ui_cus
import Ui_login
import Ui_zhuche
from md5 import *
import Ui_gengai
import Ui_gengai_pwd

id_list=[]
root_user_list=['1326387213@qq.com','root']
cus_na=''

#登录界面
class main(QMainWindow,Ui_login.Ui_login):
    show_cus_win_signal=pyqtSignal()
    show_zhuce_win_signal=pyqtSignal()
    show_adm_win_signal=pyqtSignal()

    def __init__(self):
        super(main,self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.go_zhuce)
        self.pushButton.clicked.connect(self.login)
    #登录
    def login(self):
        global cus_na
        self.user=self.lineEdit.text()
        cus_na=self.lineEdit.text()
        self.pwd=encrytion(self.lineEdit_2.text())
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 顾客密码 from 顾客 where 顾客用户名="%s"'''%(self.user)
        try:
            cursor.execute(sql)
            li=cursor.fetchall()
            #print(li)
            db.close()
            if li==():
                QMessageBox.warning(self,'错误','该用户不存在')
            else:
                npwd=li[0][0]
                #print(npwd)
                if npwd==self.pwd:
                    if self.user in root_user_list:
                        self.show_adm_win_signal.emit()#跳转管理员界面
                    else:
                        self.show_cus_win_signal.emit()#跳转客户界面
                else:
                    QMessageBox.warning(self,'错误','密码错误')                               
                npwd=''
        except:
            QMessageBox.warning(self,'错误','数据库调用失败')
        
    #跳转注册
    def go_zhuce(self):
        self.show_zhuce_win_signal.emit()


#注册界面
class zhuce(QMainWindow,Ui_zhuche.Ui_MainWindow):
    show_main_win_signal=pyqtSignal()
    yzm=''
    def __init__(self):
        super(zhuce,self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.go_main)
        self.pushButton.clicked.connect(self.zhuce)
        self.pushButton_3.clicked.connect(self.send_em)
    #返回主页
    def go_main(self):
        self.show_main_win_signal.emit()
    #发送验证码
    def send_em(self):
        self.user=self.lineEdit.text()
        self.yzm=email(self.user)    
    #判断账户是否存在
    def isuser(self):
        self.user=self.lineEdit.text()
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='select * from 顾客 where 顾客用户名="%s"'%(self.user)
        try:
            cursor.execute(sql)
            li=cursor.fetchall()
            db.close()
            if li==():
                #print(self.user)     
                return 1
            else:
                return 0
        except:
            db.close()
            print('1111')
            return -1
    #获取id
    def id_get(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 顾客ID from 顾客'''
        try:
            cursor.execute(sql)
            li=cursor.fetchall()
            print(li)
            db.close()
            for l in li:
                id_list.append(int(l[0]))
            Max=max(id_list)
            print(Max)
            id_list.clear()
            return str(Max+1)
        except:
            return None
                


    #注册功能
    def zhuce(self):
        self.user=self.lineEdit.text()
        self.name=self.lineEdit_7.text()
        self.phone=self.lineEdit_2.text()
        self.address=self.lineEdit_3.text()
        self.pwd=self.lineEdit_4.text()
        self.rpwd=self.lineEdit_5.text()
        self.secu=self.lineEdit_6.text()
        #print(self.user)
        if self.user==''or self.phone=='' or self.address=='' or self.pwd=='' or self.rpwd=='' or self.secu=='':
            QMessageBox.warning(self,'错误','请填写全部信息')
        else:
            isuser=self.isuser()
            if isuser==1:
                if self.rpwd==self.pwd:
                    secu=self.yzm
                    if secu==-1:
                        QMessageBox.warning('错误','QQ邮箱输入错误')
                    else:
                        if self.secu==secu:
                            self.id=self.id_get()
                            db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
                            cursor=db.cursor()
                            sql='''insert into 顾客 values('%s','%s','%s','%s','%s','%s');'''%(self.id,self.user,self.name,encrytion(self.pwd),self.phone,self.address)
                            #print(sql)
                            try:
                                cursor.execute(sql)
                                db.commit()
                                QMessageBox.information(self,'提示','用户创建成功')
                                db.close()
                                self.go_main()
                            except:
                                db.rollback()
                                QMessageBox.warning(self,'错误','数据库连接失败')
                        else:
                            QMessageBox.warning(self,'错误','验证码输入错误')
                else:
                    QMessageBox.warning(self,'错误','两次密码不同')
            elif isuser==0:
                QMessageBox.warning(self,'错误','用户已存在')
            else:
                QMessageBox.warning(self,'错误','数据库连接失败')

#管理员界面
class adm(QMainWindow,Ui_adm.Ui_MainWindow):
    show_Main_win_signal=pyqtSignal()
    def __init__(self):
        super(adm,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_p)
        self.pushButton_2.clicked.connect(self.on_p1)
        self.pushButton_3.clicked.connect(self.on_p2)
        self.pushButton_7.clicked.connect(self.go_Main)
        self.get_shop_list()
        self.firstshop()
        self.comboBox.currentIndexChanged.connect(self.changeshop)
        self.pushButton_4.clicked.connect(self.insert_pro)
        self.pushButton_5.clicked.connect(self.del_pro)
        self.pushButton_6.clicked.connect(self.update_pro)

        
    #返回主页
    def go_Main(self):
        self.show_Main_win_signal.emit()
#--------------------------
    #绑定第一页
    def on_p(self):
        self.stackedWidget.setCurrentIndex(0)


#--------------------------
    #绑定第二页
    def on_p1(self):
        self.stackedWidget.setCurrentIndex(1)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 订单'
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.model=QStandardItemModel(self.row,8)
        self.model.setHorizontalHeaderLabels(['订单号','顾客ID','商店ID','时间','产品UPC','产品名称','数量','价格'])
        self.tableView_2.setModel(self.model)
        self.get_dingdan()
    #获取订单信息
    def get_dingdan(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select * from 订单'''
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        j=0
        for i in li:
            self.dingdanid=QStandardItem(i[0])
            self.gukeid=QStandardItem(i[1])
            self.shangdianid=QStandardItem(i[2])
            self.time=QStandardItem(i[3])
            self.changpinid=QStandardItem(i[4])
            self.changpinname=QStandardItem(i[5])
            self.number=QStandardItem(i[6])
            self.price=QStandardItem(i[7])
            self.model.setItem(j,0,self.dingdanid)
            self.model.setItem(j,1,self.gukeid)
            self.model.setItem(j,2,self.shangdianid)
            self.model.setItem(j,3,self.time)
            self.model.setItem(j,4,self.changpinid)
            self.model.setItem(j,5,self.changpinname)
            self.model.setItem(j,6,self.number)
            self.model.setItem(j,7,self.price)
            j+=1


#----------------------------
    #绑定第三页
    def on_p2(self):
        self.stackedWidget.setCurrentIndex(2)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 顾客'
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.mod=QStandardItemModel(self.row,5)
        self.mod.setHorizontalHeaderLabels(['顾客编号','顾客用户名','顾客姓名','顾客电话','顾客地址'])
        self.tableView_3.setModel(self.mod)
        self.get_guke()
    
    #获取顾客信息
    def get_guke(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select * from 顾客'''
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        j=0
        for i in li:
            self.guke_id=QStandardItem(i[0])
            self.guke_user=QStandardItem(i[1])
            self.guke_name=QStandardItem(i[2])
            self.guke_phone=QStandardItem(i[4])
            self.guke_address=QStandardItem(i[5])
            self.mod.setItem(j,0,self.guke_id)
            self.mod.setItem(j,1,self.guke_user)
            self.mod.setItem(j,2,self.guke_name)
            self.mod.setItem(j,3,self.guke_phone)
            self.mod.setItem(j,4,self.guke_address)
            j+=1       



#-----------------------------
    #获取产品信息
    def get_pro(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 产品.产品UPC代码,产品尺寸,产品名称,产品包装,产品价格,产品数量 from 产品,商店销售 where 产品.产品UPC代码=商店销售.产品UPC代码 and 商店认证码="%s"'''%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        j=0
        for i in li:
            self.iid=QStandardItem(i[0])
            self.psize=QStandardItem(i[1])
            self.name=QStandardItem(i[2])
            self.bz=QStandardItem(i[3])
            self.price=QStandardItem(i[4])
            self.num=QStandardItem(i[5])
            self.modal.setItem(j,0,self.iid)
            self.modal.setItem(j,1,self.psize)
            self.modal.setItem(j,2,self.name)
            self.modal.setItem(j,3,self.bz)
            self.modal.setItem(j,4,self.price)
            self.modal.setItem(j,5,self.num)
            j+=1

    #获取表格选择内容
    def get_text(self):
        row=self.tableView.currentIndex().row()
        self.pid=self.tableView.model().item(row,0).text()
        self.psize=self.tableView.model().item(row,1).text()
        self.pna=self.tableView.model().item(row,2).text()
        self.ppackage=self.tableView.model().item(row,3).text()
        self.pri=self.tableView.model().item(row,4).text()
        self.pnum=self.tableView.model().item(row,5).text()
        self.lineEdit.setText(self.pid)
        self.lineEdit_2.setText(self.pna)
        self.lineEdit_3.setText(self.pri)
        self.lineEdit_4.setText(self.pnum)
        self.lineEdit_5.setText(self.psize)
        self.lineEdit_6.setText(self.ppackage)
    

    #获取超市列表
    def get_shop_list(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 商店名称 from 商店'''
        try:
            cursor.execute(sql)
            li=cursor.fetchall()
            db.close()
        except:
            QMessageBox.warning(self,'错误','数据库连接失败')
        
        for l in li:
            self.comboBox.addItem(l[0])


    #起始加载超市
    def firstshop(self):
        self.shopnum='Shop00001'
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 商店销售 where 商店认证码="%s"'%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.modal=QStandardItemModel(self.row,6)
        self.modal.setHorizontalHeaderLabels(['产品UPC代码','产品尺寸','产品名称','产品包装','产品价格','产品数量'])
        #关联产品列表
        self.tableView.setModel(self.modal)
        self.get_pro()
        self.tableView.clicked.connect(self.get_text)
    
    
    #更改超市
    def changeshop(self):
        self.shopnum='Shop00001'
        text=self.comboBox.currentText()
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 商店认证码 from 商店 where 商店名称="%s"'''%text
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.shopnum=li[0][0]
        print('_'+self.shopnum)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 商店销售 where 商店认证码="%s"'%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.modal=QStandardItemModel(self.row,6)
        self.modal.setHorizontalHeaderLabels(['产品UPC代码','产品尺寸','产品名称','产品包装','产品价格','产品数量'])
        #关联产品列表
        self.tableView.setModel(self.modal)
        self.get_pro()
        self.tableView.clicked.connect(self.get_text)
#添加商品----------------------------------
    #产品信息写入
    def insert_pro(self):
        pid=self.lineEdit.text()
        print(pid)
        pna=self.lineEdit_2.text()
        pri=self.lineEdit_3.text()
        pnum=self.lineEdit_4.text()
        shopnum=self.shopnum
        ppackage=self.lineEdit_6.text()
        psize=self.lineEdit_5.text()
        pan=self.isinpro(pid)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''insert into 产品 values('%s','%s','%s','%s','%s');'''%(pid,psize,pna,ppackage,pri)
        sql1='''insert into 商店销售 values('%s','%s','%s')'''%(shopnum,pid,pnum)
        if pan==1:
            self.insert(sql)
            self.insert(sql1)
            QMessageBox.information(self,'提示','添加成功')
        else:
            QMessageBox.warning(self,'错误','该产品已存在')

    #插入功能
    def insert(self,data):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        try:
            cursor.execute(data)
            db.commit()
            db.close()
        except:
            db.rollback()
            QMessageBox.warning(self,'错误','添加失败')

    #判断是否存在
    def isinpro(self,pid):
        cu=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=cu.cursor()
        sql='''select * from 产品 where 产品UPC代码="%s"'''%pid
        cursor.execute(sql)
        li=cursor.fetchall()
        if li==():
            return 1
        else:
            return 0
#移除商品-----------------------------------------    
    
    def del_pro(self):
        pid=self.lineEdit.text()
        shopnum=self.shopnum        
        sql='''delete from 产品 where 产品UPC代码="%s"'''%pid
        sql1='''delete from 商店销售 where 商店认证码="%s" and 产品UPC代码="%s"'''%(shopnum,pid)
        self.del_p(sql)
        self.del_p(sql1)
        QMessageBox.information(self,'提示','移除成功')
    
    def del_p(self,sql):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
        except:
            db.rollback()
            QMessageBox.warning(self,'错误','移除失败')

#更新商品----------------------------------
    def update_pro(self):
        pid=self.lineEdit.text()
        print(pid)
        pna=self.lineEdit_2.text()
        pri=self.lineEdit_3.text()
        pnum=self.lineEdit_4.text()
        shopnum=self.shopnum
        ppackage=self.lineEdit_6.text()
        psize=self.lineEdit_5.text()
        sql='''update 产品 set 产品尺寸="%s",产品名称="%s",产品包装="%s",产品价格="%s" where 产品UPC代码="%s"'''%(psize,pna,ppackage,pri,pid)
        sql1='''update 商店销售 set 产品数量="%s" where 商店认证码="%s" and 产品UPC代码="%s"'''%(pnum,shopnum,pid)
        self.update_p(sql)
        self.update_p(sql1)
        QMessageBox.information(self,'提示','更改成功')

    def update_p(self,sql):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
        except:
            db.rollback()
            QMessageBox.warning(self,'错误','更改失败')






#客户界面
class cus(QMainWindow,Ui_cus.Ui_MainWindow):
    show_Main_win_signal=pyqtSignal()
    show_cus_store_win_signal=pyqtSignal()
    def __init__(self):
        super(cus,self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.on_p)
        self.pushButton_4.clicked.connect(self.on_p1)
        self.pushButton_5.clicked.connect(self.on_p2)
        self.pushButton_7.clicked.connect(self.go_Main)
        self.get_shop_list()
        self.firstshop()
        self.comboBox.currentIndexChanged.connect(self.changeshop)
        self.pushButton.clicked.connect(self.pur_pro)
        self.pushButton_2.clicked.connect(self.updata)
        self.pushButton_6.clicked.connect(self.update_pwd)

    

    def go_Main(self):
        self.show_Main_win_signal.emit()
    def on_p(self):
        self.stackedWidget.setCurrentIndex(0)
    def on_p1(self):
        global cus_na
        self.stackedWidget.setCurrentIndex(1)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''explain select * from 订单 where 顾客ID=(select 顾客ID from 顾客 where 顾客用户名="%s")'''%(cus_na)
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.model=QStandardItemModel(self.row,8)
        self.model.setHorizontalHeaderLabels(['订单号','顾客ID','商店ID','时间','产品UPC','产品名称','数量','价格'])
        self.tableView_2.setModel(self.model)
        self.get_dingdan()
    #获取订单信息
    def get_dingdan(self):
        global cus_na
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select * from 订单 where 顾客ID=(select 顾客ID from 顾客 where 顾客用户名="%s")'''%(cus_na)
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        j=0
        for i in li:
            self.dingdanid=QStandardItem(i[0])
            self.gukeid=QStandardItem(i[1])
            self.shangdianid=QStandardItem(i[2])
            self.time=QStandardItem(i[3])
            self.changpinid=QStandardItem(i[4])
            self.changpinname=QStandardItem(i[5])
            self.number=QStandardItem(i[6])
            self.price=QStandardItem(i[7])
            self.model.setItem(j,0,self.dingdanid)
            self.model.setItem(j,1,self.gukeid)
            self.model.setItem(j,2,self.shangdianid)
            self.model.setItem(j,3,self.time)
            self.model.setItem(j,4,self.changpinid)
            self.model.setItem(j,5,self.changpinname)
            self.model.setItem(j,6,self.number)
            self.model.setItem(j,7,self.price)
            j+=1



    def on_p2(self):
        self.stackedWidget.setCurrentIndex(2)
        self.get_guke()



    def updata(self):
        self.gen=gengai()
        self.gen.show()
        
    def update_pwd(self):
        self.gen_pwd=gengai_pwd()
        self.gen_pwd.show()

        



    #获取顾客信息
    def get_guke(self):
        global cus_na
        print(cus_na)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select * from 顾客 where 顾客用户名 = "%s"'''%cus_na
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.label_12.setText(li[0][0])
        self.label_13.setText(li[0][1])
        self.label_17.setText(li[0][2])
        self.label_14.setText(li[0][4])
        self.label_15.setText(li[0][5])

    #获取产品信息
    def get_pro(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 产品.产品UPC代码,产品尺寸,产品名称,产品包装,产品价格,产品数量 from 产品,商店销售 where 产品.产品UPC代码=商店销售.产品UPC代码 and 商店认证码="%s"'''%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        j=0
        for i in li:
            self.iid=QStandardItem(i[0])
            self.psize=QStandardItem(i[1])
            self.name=QStandardItem(i[2])
            self.bz=QStandardItem(i[3])
            self.price=QStandardItem(i[4])
            self.num=QStandardItem(i[5])
            self.modal.setItem(j,0,self.iid)
            self.modal.setItem(j,1,self.psize)
            self.modal.setItem(j,2,self.name)
            self.modal.setItem(j,3,self.bz)
            self.modal.setItem(j,4,self.price)
            self.modal.setItem(j,5,self.num)
            j+=1


    #获取表格选择内容
    def get_text(self):
        row=self.tableView.currentIndex().row()
        self.pid=self.tableView.model().item(row,0).text()
        self.psize=self.tableView.model().item(row,1).text()
        self.pna=self.tableView.model().item(row,2).text()
        self.ppackage=self.tableView.model().item(row,3).text()
        self.pri=self.tableView.model().item(row,4).text()
        self.pnum=self.tableView.model().item(row,5).text()
        self.label_2.setText(self.pna)
        self.label_4.setText(self.pri)
        self.label_6.setText(self.pnum)

    #获取超市列表
    def get_shop_list(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 商店名称 from 商店'''
        try:
            cursor.execute(sql)
            li=cursor.fetchall()
            db.close()
        except:
            QMessageBox.warning(self,'错误','数据库连接失败')
        
        for l in li:
            self.comboBox.addItem(l[0])
    
    #起始加载超市
    def firstshop(self):
        self.shopnum='Shop00001'
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 商店销售 where 商店认证码="%s"'%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.modal=QStandardItemModel(self.row,6)
        self.modal.setHorizontalHeaderLabels(['产品UPC代码','产品尺寸','产品名称','产品包装','产品价格','产品数量'])
        #关联产品列表
        self.tableView.setModel(self.modal)
        self.get_pro()
        self.tableView.clicked.connect(self.get_text)

    #更改超市
    def changeshop(self):
        self.shopnum='Shop00001'
        text=self.comboBox.currentText()
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 商店认证码 from 商店 where 商店名称="%s"'''%text
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.shopnum=li[0][0]
        print('_'+self.shopnum)
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='explain select * from 商店销售 where 商店认证码="%s"'%self.shopnum
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        self.row=li[0][9]
        self.modal=QStandardItemModel(self.row,6)
        self.modal.setHorizontalHeaderLabels(['产品UPC代码','产品尺寸','产品名称','产品包装','产品价格','产品数量'])
        #关联产品列表
        self.tableView.setModel(self.modal)
        self.get_pro()
        self.tableView.clicked.connect(self.get_text)

#------------------------
    #购买产品
    def pur_pro(self):
        global cus_na
        self.num=self.lineEdit.text()
        self.onum=self.label_6.text()
        self.name=self.label_2.text()
        self.ddid=self.get_dingdanid()
        self.ndid=self.income_dingdanid(self.ddid)
        self.guke_id=self.get_cusid()
        if int(self.num)>float(self.onum):
            QMessageBox.warning(self,'错误','超出数量')
        else:
            sql='''update 商店销售 set 产品数量="%s" where 产品UPC代码=(select 产品UPC代码 from 产品 where 产品名称="%s")'''%(str(float(self.onum)-float(self.num)),self.name)
            sql1='''insert into 订单 values('%s','%s','%s',current_timestamp,'%s','%s','%s','%s')'''%(self.ndid,self.guke_id,self.shopnum,self.pid,self.pna,self.num,str(float(self.pri)*float(self.num)))
            self.update_pro(sql)
            self.update_pro(sql1)
            QMessageBox.information(self,'提示','购买成功')

    #获取用户ID
    def get_cusid(self):
        global cus_na
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 顾客ID from 顾客 where 顾客用户名="%s"'''%(cus_na)
        cursor.execute(sql)
        li=cursor.fetchall()
        return li[0][0]

    #编写订单ID
    def income_dingdanid(self,ddid):
        ndid='P0000'+str(ddid+1)
        return ndid

    #获取订单ID
    def get_dingdanid(self):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 订单号 from 订单'''
        cursor.execute(sql)
        li=cursor.fetchall()
        l=[]
        for i in li:
            l.append(int(i[0][1:]))
        db.close()
        return max(l)
    
    #购买产品更新
    def update_pro(self,sql):
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
        except:
            db.rollback()
            QMessageBox.warning(self,'错误','数据库连接失败')



#更改用户信息
class gengai(QWidget,Ui_gengai.Ui_Form):
    def __init__(self):
        super(gengai,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.updata)
    
    def updata(self):
        global cus_na
        self.guke_na=self.lineEdit.text()
        self.guke_phone=self.lineEdit_2.text()
        self.guke_add=self.lineEdit_3.text()
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''update 顾客 set 顾客姓名="%s",电话号码="%s",地址="%s" where 顾客用户名="%s"'''%(self.guke_na,self.guke_phone,self.guke_add,cus_na)
        cursor.execute(sql)
        db.commit()
        db.close()
        QMessageBox.information(self,'提示','修改成功')


#更改用户密码
class gengai_pwd(QWidget,Ui_gengai_pwd.Ui_Form):
    def __init__(self):
        super(gengai_pwd,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.updata)

    def updata(self):
        global cus_na
        self.ord_pwd=self.lineEdit.text()
        self.pwd=self.lineEdit_2.text()
        self.npwd=self.lineEdit_3.text()
        if self.pwd==self.npwd:
            opwd=self.get_pwd()
            oopwd=encrytion(self.ord_pwd)
            if opwd==oopwd:
                self.update_pwd()
                QMessageBox.information(self,'提示','修改成功')
            else:
                QMessageBox.warning(self,'错误','原密码输入错误')
        else:
            QMessageBox.warning(self,'错误','两次密码不相同')
        
    def update_pwd(self):
        global cus_na
        pwd=encrytion(self.lineEdit_2.text())
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''update 顾客 set 顾客密码="%s" where 顾客用户名="%s"'''%(pwd,cus_na)
        cursor.execute(sql)
        db.commit()
        db.close()
    
    def get_pwd(self):
        global cus_na
        db=pymysql.connect(host='106.52.121.163',user='root',password='@plmnbvcxzaq0921',db='competition')
        cursor=db.cursor()
        sql='''select 顾客密码 from 顾客 where 顾客用户名="%s"'''%(cus_na)
        cursor.execute(sql)
        li=cursor.fetchall()
        db.close()
        return li[0][0]



#跳转至注册界面
def show_zhuce():
    zhuce_win.show()
    Main.hide()

#注册界面跳转至主界面
def show_Main():
    Main.show()
    zhuce_win.hide()

#跳转至管理员界面
def show_adm():
    adm_win.show()
    Main.hide()

#跳转至客户界面
def show_cus():
    cus_win.show()
    Main.hide()

def show_adm_main():
    Main.show()
    adm_win.hide()

def show_cus_main():
    Main.show()
    cus_win.hide()


if __name__=='__main__':
    app=QApplication(sys.argv)
    Main=main()
    Main.show()
    zhuce_win=zhuce()
    adm_win=adm()
    cus_win=cus()
    Main.show_zhuce_win_signal.connect(show_zhuce)
    Main.show_cus_win_signal.connect(show_cus)
    Main.show_adm_win_signal.connect(show_adm)
    zhuce_win.show_main_win_signal.connect(show_Main)
    adm_win.show_Main_win_signal.connect(show_adm_main)
    cus_win.show_Main_win_signal.connect(show_cus_main)
    sys.exit(app.exec_())