#关于Windows
import ctypes
import sys
import os
import re
from tkinter import *
from tkinter.scrolledtext import ScrolledText as stext
from tkinter.messagebox import showerror
import download

try:
    from win32com.client import Dispatch

except ImportError:
    import pip
    pip.main(["install", "--user", "pywin32"])

now = print('python: ',sys.version,'hyyToolbox : 1.0.4')
path = path_variable = os.getenv('PATH') or "Environment variable PATH is not set."

def Path():
    print(f"The current PATH environment variable contains:\n{path_variable}")

#获取管理员权限
def Obtain_administrator_privileges():
    print('Obtaining administrator privileges.')
    #判断是否有administrator（管理员）权限
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    #如果没有administrator（管理员）权限那就用administrator（管理员）权限重新打开程序.
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        print('Successfully obtained administrator privileges.')
        sys.exit()

#创建快捷方式，有一些BUG
def Shortcuts(target,name,poaition):
    def create_shortcut(targets, shortcut_name):
        """尝试创建 try:"""
        try:
            shortcut_path = poaition
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = targets  # 指向目标文件的路径
            shortcut.WorkingDirectory = os.path.dirname(targets)
            shortcut.save()

            target_file = target  # 目标文件路径
            shortcut_name = name  # 快捷方式名称
            print('Shortcuts 已创建完毕!')
            create_shortcut(target_file, shortcut_name)
            # 创建失败则触发 except Exception as e:
        except Exception as e:
            print('我们遇到了一点问题:',e)

#一个文本计算器
def __add__():

    def calculate(expression):
        # 移除非数字字符以外的内容
        expression = ''.join(filter(lambda x: x.isdigit() or x in '+-*/. ', expression))
        
        while '(' in expression and ')' in expression:
            paren_exp = re.findall(r'\([^()]*\)', expression)[0]
            inner_exp = paren_exp[1:-1]
            result = simple_calculate(inner_exp)
            expression = expression.replace(paren_exp, str(result))

        return float(simple_calculate(expression.strip()))

    def simple_calculate(exp):
        operations = {
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
        }

        exp = exp.replace(' ', '')
        tokens = []
        num_str = ''
        for char in exp:
            if char.isdigit() or char == '.':
                num_str += char
            elif num_str != '':
                tokens.append(float(num_str))
                num_str = ''
                tokens.append(char)
            else:
                tokens.append(char)

        if num_str != '':
            tokens.append(float(num_str))

        i = 0
        while '*' in tokens or '/' in tokens:
            try:
                idx_mul_div = next(i for i, token in enumerate(tokens) if isinstance(token, str) and (token == '*' or token == '/'))
            except StopIteration:
                break
                
            op = tokens[idx_mul_div]
            res = operations[op](tokens[idx_mul_div - 1], tokens[idx_mul_div + 1])
            
            del tokens[idx_mul_div - 1 : idx_mul_div + 2]
            tokens.insert(idx_mul_div - 1, res)
            i -= 1
        
        final_result = sum([(-1)**i*tokens[i] if type(tokens[i]) is not str else (-1)**(i+1)*tokens[i+1] for i in range(len(tokens))])

        return round(final_result, 2)


    user_input = input("请输入要计算的表达式Please enter the expression to be calculated:")
    print(f"结果是The result is {calculate(user_input)}")

def __guiadd__():
    
    class TK(Tk):
        def __init__(self):
            super().__init__(className='calculator')
            self.geometry('250x250')
            self.resizable(0,0)
    
            f1=Frame(self)
            self.sc = stext(f1, height=3, state='disabled')
            self.sc.pack()
    
            f2=Frame(self)
            Button(f2, text='7', width=5, height=2, command=lambda: self.insert('7')).grid(row=0, column=0)
            Button(f2, text='8', width=5, height=2, command=lambda: self.insert('8')).grid(row=0, column=1)
            Button(f2, text='9', width=5, height=2, command=lambda: self.insert('9')).grid(row=0, column=2)
            Button(f2, text='4', width=5, height=2, command=lambda: self.insert('4')).grid(row=1, column=0)
            Button(f2, text='5', width=5, height=2, command=lambda: self.insert('5')).grid(row=1, column=1)
            Button(f2, text='6', width=5, height=2, command=lambda: self.insert('6')).grid(row=1, column=2)
            Button(f2, text='(', width=5, height=2, command=lambda: self.insert('(')).grid(row=1, column=3)
            Button(f2, text=')', width=5, height=2, command=lambda: self.insert(')')).grid(row=1, column=4)
            Button(f2, text='1', width=5, height=2, command=lambda: self.insert('1')).grid(row=2, column=0)
            Button(f2, text='2', width=5, height=2, command=lambda: self.insert('2')).grid(row=2, column=1)
            Button(f2, text='3', width=5, height=2, command=lambda: self.insert('3')).grid(row=2, column=2)
            Button(f2, text='+', width=5, height=2, command=lambda: self.insert('+')).grid(row=2, column=3)
            Button(f2, text='-', width=5, height=2, command=lambda: self.insert('-')).grid(row=2, column=4)
            Button(f2, text='0', width=5, height=2, command=lambda: self.insert('0')).grid(row=3, column=0)
            Button(f2, text='.', width=5, height=2, command=lambda: self.insert('.')).grid(row=3, column=1)
            Button(f2, text='×', width=5, height=2, command=lambda: self.insert('×')).grid(row=3, column=3)
            Button(f2, text='÷', width=5, height=2, command=lambda: self.insert('÷')).grid(row=3, column=4)
    
            Button(f2, text='CE', width=5, height=2, command=self.CE).grid(row=0, column=3)
            Button(f2, text='->', width=5, height=2, command=self.backspace).grid(row=0, column=4)
            Button(f2, text='=', width=5, height=2, command=self.get_res).grid(row=3, column=2)
    
            f1.pack()
            f2.pack()
    
        def CE(self):
            self.sc.config(state='normal')
            self.sc.delete('1.0',END)
            self.sc.config(state='disabled')
    
        def backspace(self):
            self.sc.config(state='normal')
            self.sc.delete('end - 2 chars','end - 1 char')
            self.sc.config(state='disabled')
    
        def insert(self,char):
            self.sc.config(state='normal')
            self.sc.insert(END,char)
            self.sc.config(state='disabled')
    
        def get_res(self):
            self.sc.config(state='normal')
            s=self.sc.get('1.0',END)
            s2=''
            for i in s:
                if i=='×':
                    s2+='*'
                elif i=='÷':
                    s2+='/'
                else:
                    s2+=i
    
            try:
                res=eval(s2)
                self.CE()
                for i in str(res):
                    self.insert(i)
            except:
                showerror('错误','请检查算式是否正确。')
            finally:
                self.sc.config(state='disabled')
    
    TK().mainloop() # 将TK实例化

"""已被废弃

#激活Windows专业版系统
def Activation_Windows专业版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX')#激活密钥
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))#查看密钥

#激活Windows企业版系统
def Activation_Windows企业版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43')#激活密钥
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))#查看密钥

#激活Windows家庭版系统
def Activation_Windows家庭版():
    #获取管理员权限
    Obtain_administrator_privileges()
    #通过命令行激活
    os.system('slmgr /ipk TX9XD-9SN7V-6WMQ6-BX7FG-H8Q99')#激活密钥
    os.system('slmgr /skms kms.03k.org')
    os.system('slmgr /ato')
    print('激活时长：'+os.system('slmgr /xpr'))#查看密钥\

"""

def download_pycharm(destination, Savelocation):
    print('正在(download)下载...')
    download.download_get(url='https://download-cdn.jetbrains.com.cn/python/pycharm-community-2024.3.1.1.exe',destination=destination,Savelocation=Savelocation)
    print('(download good!)下载成功！ 路径:',Savelocation+'/',destination)

def download_VSCode(destination, Savelocation):
    print('正在(download)下载...')
    download.download_get(url='https://vscode.download.prss.microsoft.com/dbazure/download/stable/fabdb6a30b49f79a7aba0f2ad9df9b399473380f/VSCodeUserSetup-x64-1.96.2.exe',destination=destination,Savelocation=Savelocation)
    print('(download good!)下载成功！ 路径:',Savelocation+'/',destination)

print('hyyToolbox - Windows')