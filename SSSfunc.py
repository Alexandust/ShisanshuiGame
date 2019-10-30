import requests
import json
from itertools import combinations,permutations

#登录
def Login(username,password):
  data={
    "username": str(username),
     "password": str(password)
   }
  header={'Content-Type':'application/json;charset=UTF-8'}
  response = requests.post('http://api.revth.com/auth/login', json=data,headers=header)
  return response.json()

#注销
def Logout(Token):
  header={'X-Auth-Token':str(Token)}
  response=requests.post('http://api.revth.com/auth/logout',headers=header)
  return response.json()


#登录验证
def Validate(Token):
  header={'X-Auth-Token':str(Token)}
  response=requests.get('http://api.revth.com/auth/validate',headers=header)
  return response.json()

#注册
def Register(username,password):
  data={
    'username':str(username),
    'password':str(password)
  }
  header={'Content-Type':'application/json'}
  response = requests.post('http://api.revth.com/register', json=data, headers=header)
  return response.json()

#注册加绑定
def Register2(username,password,student_number,student_password):
  data={
    "username":str(username),
    "password":str(password),
    "student_number":str(student_number),
    "student_password":str(student_password)
  }
  header={'content-type':'application/json'}
  response=requests.post('http://www.revth.com:12300/auth/register2',headers=header,json=data)
  return response.json()

#绑定
def Bind(Token,student_number,student_password):
  header={
    'content-type':'application/json',
    'x-auth-token':str(Token)
  }
  data={
    "student_number":str(student_number),
    "student_password":str(student_password)
  }
  response=requests.post('http://api.revth.com/auth/bind',headers=header,json=data)
  return response.json()

#开始对战
def StartGame(Token):
  header={'x-auth-token':str(Token)}
  response=requests.post('http://api.revth.com/game/open',headers=header)
  return response.json()

#出牌，注意ID是int
def Play(ID,Token,poker):

  def Tonghuashun(poker):
    ok = 1
    for i in range(1, 5):
      if poker[i] % 10 != poker[i - 1] % 10:
        ok = 0
        break
    for i in range(1, 5):
      if poker[i] // 10 != poker[i - 1] // 10 + 1:
        ok = 0
        break
    if ok == 1:
      return True
    else:
      return False


  def Zhadan(poker):
    ok1 = 1
    ok2 = 1
    for i in range(1, 4):
      if poker[i] // 10 != poker[i - 1] // 10:
        ok1 = 0
        break
    for i in range(2, 5):
      if poker[i] // 10 != poker[i - 1] // 10:
        ok2 = 0
        break
    if ok1 or ok2:
      return True
    else:
      return False


  def Hulu(poker):
    ok1 = 0
    ok2 = 0
    if (poker[0] // 10 == poker[1] // 10) and (poker[2] // 10 == poker[3] // 10 and poker[3] // 10 == poker[4] // 10):
      ok1 = 1
    if (poker[0] // 10 == poker[1] // 10 and poker[1] // 10 == poker[2] // 10) and (poker[3] // 10 == poker[4] // 10):
      ok2 = 1
    if ok1 or ok2:
      return True
    else:
      return False


  def Tonghua(poker):
    ok = 1
    for i in range(1, 5):
      if poker[i] % 10 != poker[i - 1] % 10:
        ok = 0
        break
    if ok == 1:
      return True
    else:
      return False


  def Shunzi(poker):
    ok = 1
    for i in range(1, 5):
      if poker[i] // 10 != poker[i - 1] // 10 + 1:
        ok = 0
        break
    if ok == 1:
      return True
    else:
      return False


  def Santiao(poker, n):
    ok = 1
    if n == 3:
      for i in range(1, 3):
        if poker[i] // 10 != poker[i - 1] // 10:
          ok = 0
          break
    elif n == 5:
      cnt = 0
      for i in range(1, 5):
        if poker[i] // 10 == poker[i - 1] // 10:
          cnt += 1
        else:
          cnt = 0
        if cnt >= 2:
          break
      if cnt < 2:
        ok = 0
    if ok == 1:
      return True
    else:
      return False


  def Liandui(poker):
    p1 = 0
    p2 = 0
    for i in range(1, 5):
      if poker[i] // 10 == poker[i - 1] // 10:
        if p1 == 0:
          p1 = poker[i] // 10
        else:
          p2 = poker[i] // 10
    if p1 + 1 == p2:
      return True
    else:
      return False


  def Erdui(poker):
    cnt = 0
    for i in range(1, 5):
      if poker[i] // 10 == poker[i - 1] // 10:
        cnt += 1
    if cnt >= 2:
      return True
    else:
      return False


  def Yidui(poker, n):
    ok = 0
    for i in range(1, n):
      if poker[i] // 10 == poker[i - 1] // 10:
        ok = 1
    if ok == 1:
      return True
    else:
      return False

  # 个位数为1是黑桃,2是红桃,3是梅花,4是方块
  poker = poker.split(' ')
  change1 = {'$': 1, '&': 2, '*': 3, '#': 4}
  change2 = ['', '$', '&', '*', '#']
  newpoker = []
  for x in poker:
    num = change1[x[0]]
    if x[1] == 'A':
      num += 14 * 10
    elif x[1] == 'J':
      num += 11 * 10
    elif x[1] == 'Q':
      num += 12 * 10
    elif x[1] == 'K':
      num += 13 * 10
    else:
      num += int(x[1:]) * 10
    newpoker.append(num)

  newpoker.sort()

  save = []
  MAX = 0       #记录最优且最理想情况全赢能获得多少水
  Mscore1 = 0   #记录目前最优底墩权值分数
  Mscore2 = 0   #中墩
  Mscore3 = 0   #顶墩
  SUM=0
  for TOP in combinations(newpoker, 3):
    tmp = list(newpoker[:])
    for i in range(3):
      tmp.remove(TOP[i])

    for MID in combinations(tmp, 5):
      BOT = list(tmp[:])
      for j in range(5):
        BOT.remove(MID[j])
      score1 = 0  # 底部
      val1 = 1
      score2 = 0  # 钟部
      val2 = 1
      score3 = 0  # 顶部
      val3 = 1
      if Tonghuashun(BOT):
        score1 = 512
        val1 = 5
      elif Zhadan(BOT):
        score1 = 256
        val = 4
      elif Hulu(BOT):
        score1 = 128
      elif Tonghua(BOT):
        score1 = 64
      elif Shunzi(BOT):
        score1 = 32
      elif Santiao(BOT, 5):
        score1 = 16
      elif Liandui(BOT):
        score1 = 8
      elif Erdui(BOT):
        score1 = 4
      elif Yidui(BOT, 5):
        score1 = 2
      else:
        score1 = 1

      if Tonghuashun(MID):
        score2 = 512
        val2 = 10
      elif Zhadan(MID):
        score2 = 256
        val2 = 8
      elif Hulu(MID):
        score2 = 128
        val2 = 2
      elif Tonghua(MID):
        score2 = 64
      elif Shunzi(MID):
        score2 = 32
      elif Santiao(MID, 5):
        score2 = 16
      elif Liandui(MID):
        score2 = 8
      elif Erdui(MID):
        score2 = 4
      elif Yidui(MID, 5):
        score2 = 2
      else:
        score2 = 1

      if Santiao(TOP, 3):
        score3 = 16
      elif Yidui(TOP, 3):
        score3 = 2
      else:
        score3 = 1

      if score1 >= score2 and score2 >= score3 and (val1 + val2 + val3 > MAX or (val1 + val2 + val3 == MAX and score1+score2+score3 >= SUM and score1>score2 and score2>score3) ):
        save = []
        temp = ''
        pai = ''
        for i in range(3):
          temp += change2[TOP[i] % 10]
          pai= str(TOP[i] // 10)
          if(pai=='11'):
              pai='J'
          elif(pai=='12'):
              pai='Q'
          elif(pai=='13'):
              pai='K'
          elif(pai=='14'):
              pai='A'
          temp+=pai
          if i != 2:
            temp += ' '
        save.append(temp)
        temp = ""
        for i in range(5):
          temp += change2[MID[i] % 10]
          pai   = str(MID[i] // 10)
          if(pai=='11'):
              pai='J'
          elif(pai=='12'):
              pai='Q'
          elif(pai=='13'):
              pai='K'
          elif(pai=='14'):
              pai='A'
          temp+=pai
          if i != 4:
            temp += ' '
        save.append(temp)
        temp = ""
        for i in range(5):
          temp += change2[BOT[i] % 10]
          pai   = str(BOT[i] // 10)
          if(pai=='11'):
              pai='J'
          elif(pai=='12'):
              pai='Q'
          elif(pai=='13'):
              pai='K'
          elif(pai=='14'):
              pai='A'
          temp+=pai
          if i != 4:
            temp += ' '
        save.append(temp)
        MAX = val1 + val2 + val3
        SUM=score1+score2+score3
        Mscore1 = score1
        Mscore2 = score2
        Mscore3 = score3

  header={
    'content-type':'application/json',
    'x-auth-token':str(Token)
          }
  data={
    'id':int(ID),
    'card':save
  }
  print(save)
  response=requests.post('http://api.revth.com/game/submit',json=data,headers=header)
  return response.json()


#排行榜
def Rank():
  response = requests.get('http://api.revth.com/rank')
  return response.json()

#历史战局列表
def History(Token,page,limit,id):
  header={'x-auth-token':Token}
  querystring = {"page": str(page), "limit":str(limit), "player_id": str(id)}
  response=requests.get('http://api.revth.com/history',headers=header,params=querystring)
  return response.json()

#历史战局详情,这里ID是战局ID
def HistoryDetail(Token,ID):
  header={'X-Auth-Token':str(Token)}
  url='http://api.revth.com/history/'+str(ID)
  response=requests.get(url,headers=header)
  return response.json()

