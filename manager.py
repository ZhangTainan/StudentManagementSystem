import csv
from os import system
import numpy as np
from user import User
from student import Student


class Manager:
    user = User()

    def __init__(self):
        self.student_list = []
        try:
            with open('data.csv', 'r') as f:
                data = csv.reader(f)
                while 1:
                    try:
                        self.student_list.append(
                            Student(*data.__next__()))  # 用迭代器访问数据
                    except StopIteration:
                        break
        except FileNotFoundError:
            print('文件不存在！快去添加数据吧！')

    @user.login_authentication()
    def show_all(self):
        for student in self.student_list:
            student.show_info()

    @user.login_authentication()
    def add(self):
        number = input('请输入学号:')
        if number in map(lambda x: x.get_info()['学号'], self.student_list):
            print('该学生已存在！')
            return
        name = input('请输入姓名:')
        gender = input('请输入性别:')
        age = int(input('请输入年龄:'))
        Chinese = int(input('请输入语文成绩:'))
        math = int(input('请输入数学成绩:'))
        self.student_list.append(
            Student(number, name, gender, age, Chinese, math))

    @user.login_authentication()
    def delete(self):
        number = input('请输入要修改的学生的学号:')
        for student in self.student_list:
            if number == student.get_info()['学号']:
                self.student_list.remove(student)
                print(self.student_list)
                break
        else:
            print('未找到该学生！')

    @user.login_authentication()
    def modify(self):
        number = input('请输入要修改的学生的学号:')
        for student in self.student_list:
            if number == student.get_info()['学号']:
                student.show_info()
                student.get_info()['姓名'] = input('请输入修改后的姓名:')
                student.get_info()['性别'] = input('请输入修改后的性别:')
                student.get_info()['年龄'] = input('请输入修改后的年龄:')
                student.get_info()['语文'] = int(input('请输入修改后的语文成绩:'))
                student.get_info()['数学'] = int(input('请输入修改后的数学成绩:'))
                student.get_info()['总分'] = student.get_info()[
                    '语文'] + student.get_info()['数学']
                break
        else:
            print('未找到该学生！')

    @user.login_authentication()
    def inquiry(self):
        number = input('请输入要查询的学生的学号:')
        for student in self.student_list:
            if number == student.get_info()['学号']:
                student.show_info()
                break
        else:
            print('未找到该学生！')

    @user.login_authentication()
    def average(self):
        avg_Chinese = np.average(
            list(map(lambda x: x.get_info()['语文'], self.student_list)))
        avg_math = np.average(
            list(map(lambda x: x.get_info()['数学'], self.student_list)))
        avg_total = np.average(
            list(map(lambda x: x.get_info()['总分'], self.student_list)))
        print(f'语文的平均分为:{avg_Chinese}')
        print(f'数学的平均分为:{avg_math}')
        print(f'总分的平均分为:{avg_total}')

    @user.login_authentication()
    def rank(self):
        order_list = sorted(self.student_list, key=lambda x: x.get_info()[
                            '总分'], reverse=True)
        for student in order_list:
            print(
                f'姓名:{student.get_info()["姓名"]}\t总分:{student.get_info()["总分"]}\t排名:{order_list.index(student) + 1}')

    @user.login_authentication()
    def variance(self):
        var_Chinese = np.var(
            list(map(lambda x: x.get_info()['语文'], self.student_list)))
        var_math = np.var(
            list(map(lambda x: x.get_info()['数学'], self.student_list)))
        var_total = np.var(
            list(map(lambda x: x.get_info()['总分'], self.student_list)))
        print(f'语文的方差为:{var_Chinese}')
        print(f'数学的方差为:{var_math}')
        print(f'总分的方差为:{var_total}')

    def save_data(self):
        with open('data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for student in self.student_list:
                row = list(student.get_info().values())[:-1]
                writer.writerow(row)

    def execute(self):
        try:
            while 1:
                cmd = yield  # 生成器
                if cmd == '1':
                    self.user.login()
                    system('pause')
                elif cmd == '2':
                    self.user.register()
                    system('pause')
                elif cmd == '3':
                    self.add()
                    system('pause')
                elif cmd == '4':
                    self.delete()
                    system('pause')
                elif cmd == '5':
                    self.modify()
                    system('pause')
                elif cmd == '6':
                    self.inquiry()
                    system('pause')
                elif cmd == '7':
                    self.show_all()
                    system('pause')
                elif cmd == '8':
                    self.average()
                    system('pause')
                elif cmd == '9':
                    self.variance()
                    system('pause')
                elif cmd == '10':
                    self.rank()
                    system('pause')
                elif cmd == 'q':
                    print('已退出！')
                    break

                else:
                    print('请输入正确的命令')
            self.save_data()
        except ValueError:
            print('出错啦！年龄、语文和数学成绩必须是数字！')
            self.main()
            '''
                异常捕获,当用户输入年龄为非数字时给出反馈,并重新执行主函数
            '''

    def main(self):
        exe = self.execute()
        exe.send(None)
        while 1:
            print('''
==============================
1用户登录       2用户注册
3添加学生       4删除学生
5修改学生       6查看学生
7显示全部       8算平均值
9计算方差       10学生排名
Q退出
请输入命令序号后回车:''')
            cmd = input()
            try:
                exe.send(cmd)  # 协程
            except StopIteration:
                break


if __name__ == '__main__':
    m = Manager()
    m.main()
