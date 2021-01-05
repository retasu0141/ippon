from flask import Flask, request, abort,render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,  PostbackEvent, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import random

from datetime import datetime as dt

import urllib.request, urllib.error

from apiclient.discovery import build
import urllib.parse
import re, requests
app = Flask(__name__)
def checkURL(url):
    try:
        f = urllib.request.urlopen(url)
        print ("OK:" + url )
        f.close()
        return True
    except Exception as e:
        print (str(e))
        print ("NotFound:" + url)
        return False

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def getmember(id):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    member_list = []
    for row in cur:
        if id+'/' in row[0]:
            member_list.append(row)
        else:
            pass
    print(member_list)
    return member_list

def getpoint(id):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    for row in cur:
        if id in row[0]:
            return row[4],row[3]
        else:
            pass
    return
def getippon(id):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    for row in cur:
        if id in row[0]:
            return row[1],row[2],row[5]
        else:
            pass
    return

def delta(id):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    for row in cur:
        if id in row[0]:
            sql = 'delete from db where id = ?'
            data = (row[0])
            cursor.execute(sql, data)
        else:
            pass
    return

def seve1(id,user_id):
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if id in row:
                print(row)
                dbID = row[0]
                print('ok3')
                print(dbID)
                cur.execute("UPDATE db SET id = '{id}' WHERE name='{name}';".format(id=id+"/"+user_id,name=user_id))
                conn.commit()
                print('ok3-2')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{id}','{text}','{name}','{point}','{point_n}','{test}')".format(id=id+"/"+user_id,text="text",name=user_id,point='0',point_n='0',test='0'))
        conn.commit()
        print('ok4')
        return
    except Exception as e:
        print (str(e))
        return

def seve2(id,n_):
    n = str(n_)
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if id in row:
                print(row)
                dbID = row[0]
                print('ok3')
                print(dbID)
                cur.execute("UPDATE db SET id = '{id}' WHERE point='{point}';".format(id=id,point=n))
                conn.commit()
                print('ok3-2')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{id}','{text}','{name}','{point}','{point_n}','{test}')".format(id=id,text="text",name="name",point=n,point_n='0',tset="0"))
        conn.commit()
        print('ok4')
        return
    except Exception as e:
        print (str(e))
        return

def seve3(id,text,name,point,token):
    n = str(n_)
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{id}','{text}','{name}','{point}','{point_n}','{test}')".format(id=id,text=text,name=name,point=point,point_n='0',tset=token))
        conn.commit()
        print('ok4')
        return
    except Exception as e:
        print (str(e))
        return

def seve4(id,point):
    n = str(n_)
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if id in row:
                print(row)
                dbID = row[0]
                print('ok3')
                print(dbID)
                cur.execute("UPDATE db SET id = '{id}' WHERE point_n='{point_n}';".format(id=id,point_n=point))
                conn.commit()
                print('ok3-2')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
    except Exception as e:
        print (str(e))
        return


def ippon1(msg,name,id):
    data = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": msg,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "回答者",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": name,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "投票",
          "data": "投票/"+id
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def ippon2(id):
    data = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "参加者は下のボタンを押してね",
        "weight": "bold",
        "size": "lg",
        "margin": "none"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "参加",
          "data": "join/"+id,
          "displayText": "参加したよ！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def ippon3(text,name):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://live.staticflickr.com/65535/50803657807_d507de63dd_z.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": text,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "回答者",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": name,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  }
}
    return data

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def on_postback(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    postback_msg = event.postback.data

    if "join" in postback_msg:
        id = postback_msg.replace("join/","")
        seve1(id,user_id)
        m_list = getmember(id)
        members = len(m_list)
        seve2(id,members)

    if "投票" in postback_msg:
        id = postback_msg.replace("投票/","")
        point_n_,point_ = getpoint(id)
        point_n = int(point_n_)
        point = int(point_)
        point__n = point_n + 1
        if point <= point__n:
            text,name,token = getippon(id)
            data = ippon3(text,name)
            flex = {"type": "flex","altText": "回答","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(token,messages=container_obj)
        else:
            seve4(id,str(point__n))



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    msg_id = event.message.id
    user_id = event.source.user_id

    if msg_text == 'IPPONスタート':
        if hasattr(event.source,"group_id"):
            data = ippon2(event.source.group_id)
        if hasattr(event.source,"room_id"):
            data = ippon2(event.source.room_id)
        name = line_bot_api.get_profile(user_id).display_name
        flex = {"type": "flex","altText": "スタート","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
        return

    if msg_text == 'IPPON終了':
        if hasattr(event.source,"group_id"):
            delta(event.source.group_id)
        if hasattr(event.source,"room_id"):
            delta(event.source.room_id)
        line_bot_api.reply_message(msg_from,TextSendMessage(text='また始めるときは　IPPONスタート　と言ってね！'))
        return

    if 'A.' in msg_text:
        if hasattr(event.source,"group_id"):
            m_list = getmember(event.source.group_id)
        if hasattr(event.source,"room_id"):
            m_list = getmember(event.source.room_id)
        members = len(m_list)
        members_ = str(members)
        text = msg_text.replace("A.","")
        seve2(id,members)
        name = line_bot_api.get_profile(user_id).display_name
        seve3(msg_id,text,name,members_,msg_from)
        data = ippon1(msg_text,name,msg_id)
        flex = {"type": "flex","altText": "回答","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.multicast([m_list],messages=container_obj)
        return




if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
