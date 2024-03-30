#系统复制有延迟！所以在执行完复制操作后，要加上sleep()一小段时间，再获取剪切板内容
#sleep()的时间经测试，0.01s不行，0.05大部分时间可以有时候不行，现在用的是0.1s

#exe会闪退，所以用了while来解决

#控制台按ctrl+c会退出，但是程序又要ctrl+c来复制，所以用的时候不能把光标移到控制台上

#主循环监听结构值得借鉴: wait()某个键后执行操作

#将触发键从字母键x改成了功能键CAPSLOCK，就不会出现将选中内容覆盖写成x的bug
from keyboard import press
from keyboard import release
from keyboard import wait
from pyperclip import paste
from getMeaning import Key2result
from time import sleep


def Copy():
    press("ctrl")
    press("c")
    release("c")
    release("ctrl")


def Output(Keyword,result):
    print("            ",end="")
    for i in range(len(Keyword)):
        print("-",end="")
    print("")
    print("            "+Keyword)
    print("            ",end="")
    for i in range(len(Keyword)):
        print("-",end="")
    print("")
    if len(result)==1:
        print("Fail...")
    else:
        if result[0][0]!=0:
            for h in result[0]:
                print(h)
        for i in result[1:]:
            print(i[0])
            print("        "+i[1])
    print("\n")
            

def Trigger():
    Copy()
    sleep(0.1)#暂停一会因为复制有延时
    Keyword=paste()
    result=Key2result(Keyword)
    Output(Keyword,result)


if __name__=="__main__":
    print("[英译中2.0]\n CAPSLOCK 键将选中的英文翻译成中文\n\n")
    while True:
        wait("CAPSLOCK")#'CAPSLOCK'为触发键
        Trigger()
    print("--Quit--")
    
