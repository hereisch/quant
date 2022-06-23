# -*- coding: utf-8 -*-#
from datetime import datetime,date,timedelta
import re
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import time
from BK_fund import Zrzt


class my_thread(QThread):
    send_signal = pyqtSignal(str)

    def run(self):
        while True:

            self.send_signal.emit('--')
            time.sleep(1)


class NewTableWidget(QWidget):
    sum = 0
    zrzt = Zrzt()
    def __init__(self):
        super(NewTableWidget, self).__init__()
        self.resize(2300, 1200)
        self.setWindowTitle('昨日涨停')

        # 表头标签
        self.headerlabels = ['code','name','最新价','涨跌幅','涨速','流通市值','主力净额', '主力净占比','超大单净额', '超大单净占比' ,'大单净额' ,'大单净占比', '中单净额',
                    '中单净占比', '小单净额', '小单净占比','最高','最低','今开','昨收','换手','振幅']
        # 行数和列数
        self.rowsnum, self.columnsnum = 60,len(self.headerlabels)

        self.TableWidget = QTableWidget(self.rowsnum, self.columnsnum)

        # todo 优化 2 设置水平方向表格为自适应的伸缩模式
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.TableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Todo 优化 5 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.TableWidget)
        QTableWidget.resizeRowsToContents(self.TableWidget)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.TableWidget.setHorizontalHeaderLabels(self.headerlabels)
        # Todo 优化1 设置垂直方向的表头标签
        # TableWidget.setVerticalHeaderLabels(['行1', '行2', '行3', '行4'])

        # 添加单元格初始化内容
        for i in range(self.rowsnum):
            for j in range(self.columnsnum):
                newItem = QTableWidgetItem()
                newItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, j, newItem)

        # 表格中不显示分割线
        # TableWidget.setShowGrid(False)

        # 隐藏垂直头标签
        # TableWidget.verticalHeader().setVisible(False)

        # 创建更新按钮
        self.switch_btn = QPushButton()
        self.switch_btn.setText("启动更新")

        # 实例化线程类
        self.myThread = my_thread()

        # 单击按钮, 以单击为发送信号
        self.switch_btn.clicked.connect(self.on_clicked)

        # 整体布局
        layout = QVBoxLayout()
        layout.addWidget(self.TableWidget)
        layout.addWidget(self.switch_btn)

        self.setLayout(layout)

        # 单击按钮的槽

    def on_clicked(self):
        self.sum += 1
        if self.sum % 2 == 0:
            self.myThread.send_signal.disconnect(self.switch_slot)
            self.switch_btn.setText("重新更新")
            self.myThread.terminate()
        else:
            self.myThread.send_signal.connect(self.switch_slot)
            self.switch_btn.setText("终止更新")
            self.myThread.start()

    # 连接信号的槽
    def switch_slot(self,):
        # 更新表格内容
        data = self.zrzt.run()
        if datetime.now() < datetime.strptime(str(datetime.now().date()) + '9:25', '%Y-%m-%d%H:%M'):
            for i in ['主力净额' ,'主力净占比' ,'超大单净额' ,'超大单净占比',
                            '大单净额', '大单净占比', '中单净额', '中单净占比', '小单净额' ,'小单净占比']:
                data[i] = data[i].replace('-',0)

        data['流通市值'] = round(data['流通市值'] / 100000000,2)
        data['主力净额'] = round(data['主力净额']/10000,2)
        data['超大单净额'] = round(data['超大单净额']/10000,2)
        data['大单净额'] = round(data['大单净额']/10000,2)
        data['中单净额'] = round(data['中单净额']/10000,2)
        data['小单净额'] = round(data['小单净额']/10000,2)
        data = data.drop_duplicates()
        data = data.sort_values(by=['涨跌幅',],ascending=False)
        data = data.reset_index(drop=True)
        # print(data)
        for idy, itemX in data.iterrows():
            for idx, itemY in enumerate(self.headerlabels):
                newItem = QTableWidgetItem(str(itemX[itemY]))
                if  itemY in ['涨跌幅','涨速','主力净额' ,'主力净占比' ,'超大单净额' ,'超大单净占比',
                            '大单净额', '大单净占比', '中单净额', '中单净占比', '小单净额' ,'小单净占比']:
                    if itemX[itemY] >= 0:
                        newItem.setForeground(QColor(255,0,0))
                    else:
                        newItem.setForeground(QColor(0, 150, 0))
                elif itemY in ['最新价','最高','最低','今开']:
                    if itemX[itemY] >= itemX['昨收'] :
                        newItem.setForeground(QColor(255,0,0))
                    else:
                        newItem.setForeground(QColor(0, 150, 0))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(idy, idx, newItem)


        self.TableWidget.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NewTableWidget()
    win.show()
    sys.exit(app.exec_())