#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import flask
from flask_cors import CORS
from flask import jsonify
from itertools import combinations,permutations

def Play(poker):

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

  # ��λ��Ϊ1�Ǻ���,2�Ǻ���,3��÷��,4�Ƿ���
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
  MAX = 0       #��¼���������������ȫӮ�ܻ�ö���ˮ
  Mscore1 = 0   #��¼Ŀǰ���ŵ׶�Ȩֵ����
  Mscore2 = 0   #�ж�
  Mscore3 = 0   #����
  SUM=0
  for TOP in combinations(newpoker, 3):
    tmp = list(newpoker[:])
    for i in range(3):
      tmp.remove(TOP[i])

    for MID in combinations(tmp, 5):
      BOT = list(tmp[:])
      for j in range(5):
        BOT.remove(MID[j])
      score1 = 0  # �ײ�
      val1 = 1
      score2 = 0  # �Ӳ�
      val2 = 1
      score3 = 0  # ����
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

      bigger = 0
      if score1 > Mscore1:
        bigger += 1
      if score2 > Mscore2:
        bigger += 1
      if score3 > Mscore3:
        bigger += 1

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

  return save


server = flask.Flask(__name__)  # __name__����ǰ��python�ļ����ѵ�ǰ��python�ļ�����һ����������

CORS(server, resources=r'/*')


@server.route('/getcards', methods=['post'])  # ��һ����������·��,�ڶ�������֧�ֵ�����ʽ����д�Ļ�Ĭ����get
def getcards():
    card = flask.request.values.get('card')
    # ��Ķ��ѵ�����Ľӿڵ�ʱ��ᷢ����13���ƣ���һ�д�����Ի�ȡ��13���ƣ�
    # �����ַ�������ʽ�洢��card�У�����card="*2 *3 *4 *5 *6 *7 *8 *9 *10 *J *Q *K *A"

    # Ȼ����������Ҫ������㷨������ַ������д����ֳ����գ�Ȼ��洢��res�У�����res=["*2 *3 *4","*5 *6 *7 *8 *9","*10 *J *Q *K *A"]
    # ʣ�µľͲ��ø���
    # ���ĵĽӿڵ�url��http://���ip:7777/getcards
    # ǰ����ô��������ӿ��������ԣ��
    res=Play(card)
    ans={'card':res}
    response = flask.make_response(jsonify(ans))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response


server.run(port=7777, debug=True, host='0.0.0.0')
