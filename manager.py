# -*- coding: gbk -*-
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
                        self.student_list.append(Student(*data.__next__()))  # �õ�������������
                    except StopIteration:
                        break
        except FileNotFoundError:
            print('�ļ������ڣ���ȥ������ݰɣ�')
    @user.login_authentication()
    def show_all(self):
        for student in self.student_list:
            student.show_info()

    @user.login_authentication()
    def add(self):
        number = input('������ѧ��:')
        if number in map(lambda x:x.get_info()['ѧ��'],self.student_list):
            print('��ѧ���Ѵ��ڣ�')
            return
        name = input('����������:')
        gender = input('�������Ա�:')
        age = int(input('����������:'))
        Chinese = int(input('���������ĳɼ�:'))
        math = int(input('��������ѧ�ɼ�:'))
        self.student_list.append(Student(number, name, gender, age, Chinese, math))

    @user.login_authentication()
    def delete(self):
        number = input('������Ҫ�޸ĵ�ѧ����ѧ��:')
        for student in self.student_list:
            if number == student.get_info()['ѧ��']:
                self.student_list.remove(student)
                print(self.student_list)
                break
        else:
            print('δ�ҵ���ѧ����')

    @user.login_authentication()
    def modify(self):
        number = input('������Ҫ�޸ĵ�ѧ����ѧ��:')
        for student in self.student_list:
            if number == student.get_info()['ѧ��']:
                student.show_info()
                student.get_info()['����'] = input('�������޸ĺ������:')
                student.get_info()['�Ա�'] = input('�������޸ĺ���Ա�:')
                student.get_info()['����'] = input('�������޸ĺ������:')
                student.get_info()['����'] = int(input('�������޸ĺ�����ĳɼ�:'))
                student.get_info()['��ѧ'] = int(input('�������޸ĺ����ѧ�ɼ�:'))
                student.get_info()['�ܷ�'] = student.get_info()['����'] + student.get_info()['��ѧ']
                break
        else:
            print('δ�ҵ���ѧ����')

    @user.login_authentication()
    def inquiry(self):
        number = input('������Ҫ��ѯ��ѧ����ѧ��:')
        for student in self.student_list:
            if number == student.get_info()['ѧ��']:
                student.show_info()
                break
        else:
            print('δ�ҵ���ѧ����')

    @user.login_authentication()
    def average(self):
        avg_Chinese = np.average(list(map(lambda x: x.get_info()['����'], self.student_list)))
        avg_math = np.average(list(map(lambda x: x.get_info()['��ѧ'], self.student_list)))
        avg_total = np.average(list(map(lambda x: x.get_info()['�ܷ�'], self.student_list)))
        print(f'���ĵ�ƽ����Ϊ:{avg_Chinese}')
        print(f'��ѧ��ƽ����Ϊ:{avg_math}')
        print(f'�ֵܷ�ƽ����Ϊ:{avg_total}')

    @user.login_authentication()
    def rank(self):
        order_list = sorted(self.student_list, key=lambda x: x.get_info()['�ܷ�'], reverse=True)
        for student in order_list:
            print(f'����:{student.get_info()["����"]}\t�ܷ�:{student.get_info()["�ܷ�"]}\t����:{order_list.index(student) + 1}')

    @user.login_authentication()
    def variance(self):
        var_Chinese = np.var(list(map(lambda x: x.get_info()['����'], self.student_list)))
        var_math = np.var(list(map(lambda x: x.get_info()['��ѧ'], self.student_list)))
        var_total = np.var(list(map(lambda x: x.get_info()['�ܷ�'], self.student_list)))
        print(f'���ĵķ���Ϊ:{var_Chinese}')
        print(f'��ѧ�ķ���Ϊ:{var_math}')
        print(f'�ֵܷķ���Ϊ:{var_total}')

    def save_data(self):
        with open('data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for student in self.student_list:
                row = list(student.get_info().values())[:-1]
                writer.writerow(row)

    def execute(self):
        try:
            while 1:
                cmd = yield  # ������
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
                    print('���˳���')
                    break

                else:
                    print('��������ȷ������')
            self.save_data()
        except ValueError:
            print('�����������䡢���ĺ���ѧ�ɼ����������֣�')
            self.main()
            '''
                �쳣����,���û���������Ϊ������ʱ��������,������ִ��������
            '''

    def main(self):
        exe = self.execute()
        exe.send(None)
        while 1:
            print('1��¼\t2ע��\n3���ѧ��\t4ɾ��ѧ��\n5�޸�ѧ��\t6�鿴ѧ��\n7��ʾȫ��\t8��ƽ��ֵ\n9���㷽��\t10����\nq�˳�\n�������������:')
            cmd = input()
            try:
                exe.send(cmd)  # Э��
            except StopIteration:
                break


if __name__ == '__main__':
    m = Manager()
    m.main()
