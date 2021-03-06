from flask import Flask, request, abort,render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, TextMessage, TextSendMessage, FlexSendMessage,  PostbackEvent, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
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
            member_list.append(row[2])
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
    sql = "delete from db where id = '{id}'".format(id=id)
    #data = (data_id,)
    cur.execute(sql)
    conn.commit()
    '''for row in cur:
        if id in row[0]:
            print(row[0])
            data_id = row[0]
            #
            sql = "delete from db where '{id}' in id".format(id=data_id)
            #data = (data_id,)
            cur.execute(sql)
            conn.commit()
        else:
            pass'''
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

def seve2(id,nint):
    n = str(nint)
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
                cur.execute("UPDATE db SET point='{point}' WHERE id = '{id}';".format(id=id,point=n))
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
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{id}','{text}','{name}','{point}','{point_n}','{test}')".format(id=id,text=text,name=name,point=point,point_n='0',test=token))
        conn.commit()
        print('ok4')
        return
    except Exception as e:
        print (str(e))
        return

def seve4(id):
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
                point_n_int = int(row[4]) + 1
                point_n = str(point_n_int)
                print('ok3')
                print(point_n)
                r = cur.execute("UPDATE db SET pointdate='{point_n}' WHERE id = '{id}'".format(id=row[0],point_n=point_n))
                print(r)
                cur.execute('select * from db')
                result = cur.fetchall()
                print(result)
                conn.commit()
                cur.close()
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
          "data": "投票/"+id,
          "displayText": name+"の「"+msg+"」に投票したよ！"
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

def ippon4():
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
        "text": "使い方",
        "weight": "bold",
        "size": "3xl",
        "align": "center"
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
                "text": "注意",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "参加者は事前にこのアカウントを友達追加しておいてください。また、20秒以内に投票数が集まらないと無効になります。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "最初に",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "IPPONスタートと送信し参加者を決める",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "お題",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "任意のお題を決める",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "回答",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "A. の後に回答文をつけて送信する",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "回答例",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "A.○○だから",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "投票",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "個人チャットに投票用メッセージが届くので、良いと思ったら[投票]ボタンを押す",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "IPPON",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "指定の数以上の投票数が確認されるとグループにIPPONが出る",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "終了",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "人数リセット、又は終了するときはIPPON終了と送信する",
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
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "IPPONスタート",
          "text": "IPPONスタート"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "IPPON終了",
          "text": "IPPON終了"
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
@handler.add(JoinEvent)
def join(event):
    reply_token = event.reply_token
    data = ippon4()
    flex = {"type": "flex","altText": "説明","contents":data}
    container_obj = FlexSendMessage.new_from_json_dict(flex)
    line_bot_api.reply_message(reply_token,messages=container_obj)


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
        if point >= 11:
            point_data = 10
        elif point >= 10:
            point_data = 8
        elif point >= 9 and point <= 5:
            point_data = point - 1
        elif point <= 4:
            point_data = point
        print(point_data)
        print(point__n)
        if point_data <= point__n:
            text,name,token = getippon(id)
            data = ippon3(text,name)
            flex = {"type": "flex","altText": "回答","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(token,messages=container_obj)
            #line_bot_api.reply_message(reply_token,messages=container_obj)
        else:
            seve4(id)



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
            m_list = getmember(event.source.group_id)
            id = event.source.group_id 
        if hasattr(event.source,"room_id"):
            delta(event.source.room_id)
            m_list = getmember(event.source.room_id)
            id = event.source.room_id
        for member in m_list:
            delta('{id}/{member}'.format(id=id,member=member))
        line_bot_api.reply_message(msg_from,TextSendMessage(text='また始めるときは　IPPONスタート　と言ってね！'))
        return

    if 'A.' in msg_text:
        if hasattr(event.source,"group_id"):
            m_list = getmember(event.source.group_id)
            id = event.source.group_id 
        if hasattr(event.source,"room_id"):
            m_list = getmember(event.source.room_id)
            id = event.source.room_id
        print(m_list)
        members = len(m_list)
        members_ = str(members)
        text = msg_text.replace("A.","")
        seve2(id,members)
        name = line_bot_api.get_profile(user_id).display_name
        seve3(msg_id,text,name,members_,msg_from)
        data = ippon1(msg_text,name,msg_id)
        flex = {"type": "flex","altText": "回答","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.multicast(m_list,messages=container_obj)
        #line_bot_api.reply_message(msg_from,messages=container_obj)
        return

    if msg_text == 'IPPON使い方':
        data = ippon4()
        flex = {"type": "flex","altText": "説明","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
        return


if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
