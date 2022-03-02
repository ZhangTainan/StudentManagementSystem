import json
import re

IS_LOGINED = False  # 引入全局变量记录登录状态


class User:
    def __init__(self):
        self.users = self.get_users()

    def get_users(self):
        try:
            with open('users.json', 'r') as f:
                data = json.load(f)
                users = data['users']
        except FileNotFoundError:
            users=[]
        return users

    def register(self):
        user_name = input('请输入用户名(字母、数字,大于6位):')
        password = input('请输入密码(数字、字母,大于8位):')
        password_again = input('请再次输入密码:')
        if not re.match('^[\d\w]{6,}$', user_name):  # 简单地用正则表达式过滤一下用户名和密码
            print('用户名不符合规范!请重试！')
        elif user_name in map(lambda x: x['user_name'], self.users):
            print('用户名已存在,请重试！')
        elif password_again != password:
            print('两次密码不一致,请重试！')
        elif not re.match('^[\d\w]{8,}$', password):
            print('密码不符合规范')
        else:
            user_info = {'user_name': user_name, 'password': password}
            self.users.append(user_info)
            data = {'users': self.users}
            with open('users.json', 'w') as f:
                json.dump(data, f)
            print('注册成功！')
            return
        self.register()

    def login(self):
        global IS_LOGINED
        user_name = input('请输入用户名:')
        password = input('请输入密码:')
        for user in self.users:
            if user['user_name'] == user_name and user['password'] == password:
                IS_LOGINED = True
                print('登录成功！')
                break
        else:
            print('用户名或密码错误,请重试!')
            self.login()

    def login_authentication(self):  # 定义一个装饰器用于登录验证
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not IS_LOGINED:
                    print('您还未登录,请登录!')
                    self.login()

                return func(*args, **kwargs)

            return wrapper

        return decorator


if __name__ == '__main__':
    u = User()
    u.register()
