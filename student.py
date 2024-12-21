class Student:
    def __init__(self, number, name, gender, age, Chinese, math):
        self.__info = {'学号': number, '姓名': name, '性别': gender,
                       '年龄': int(age), '语文': int(Chinese), '数学': int(math)}
        # 把学生信息私有化,使其只在内部被访问和修改
        self.__info['总分'] = self.__info['语文'] + self.__info['数学']

    def get_info(self):
        return self.__info

    def show_info(self):
        for key, value in self.__info.items():
            print(key, value, sep=':')
        print('===========================')


if __name__ == '__main__':
    s = Student(1, 2, 3, 4, 5, 6)
    s.show_info()
