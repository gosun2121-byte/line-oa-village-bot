from flask import Flask, request, abort
import requests
import json
import hashlib
import hmac
import base64
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "AS9ZGQqAWg9SK4KD7yMyLUGyTH5A8xvlHjRMdR5ohBZ903bA+Sz060KWiQ4E/3SAjnGs34WevGz+rbcp4PK+U9I0D+LsAFw1XKYQrzaYRPv70kRDHPUC7hzKJrK562wv6Pqh9NM6XHepZIT7EyeEbwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ebb901867293f260644563b260c06d08"

HEADERS = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def verify_signature(body, signature):
    hash = hmac.new(CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256).digest()
    return base64.b64encode(hash).decode("utf-8") == signature

def reply_message(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"
    data = {"replyToken": reply_token, "messages": messages}
    r = requests.post(url, headers=HEADERS, json=data)
    print(f"Reply status: {r.status_code} | {r.text}")
    return r

# =============================================
# ฟังก์ชันสร้างข้อความตอบกลับแต่ละปุ่ม
# =============================================

def get_news_message():
    return {
        "type": "flex",
        "altText": "ข่าวสารหมู่บ้าน",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{"type": "text", "text": "📰 ข่าวสารหมู่บ้าน", "weight": "bold", "size": "lg", "color": "#FFFFFF"}],
                "backgroundColor": "#EC008C",
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🔔 ข่าวที่ 1", "weight": "bold", "size": "sm", "color": "#EC008C"},
                            {"type": "text", "text": "ประชุมหมู่บ้านประจำเดือน กุมภาพันธ์ 2568", "size": "sm", "wrap": True},
                            {"type": "text", "text": "วันที่ 25 ก.พ. 68 เวลา 09.00 น. ณ ศาลาประชาคม", "size": "xs", "color": "#888888", "wrap": True}
                        ]
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box", "layout": "vertical", "margin": "md",
                        "contents": [
                            {"type": "text", "text": "🔔 ข่าวที่ 2", "weight": "bold", "size": "sm", "color": "#EC008C"},
                            {"type": "text", "text": "แจกเบี้ยยังชีพผู้สูงอายุ ประจำเดือน มีนาคม 2568", "size": "sm", "wrap": True},
                            {"type": "text", "text": "วันที่ 10 มี.ค. 68 ณ ที่ทำการผู้ใหญ่บ้าน", "size": "xs", "color": "#888888", "wrap": True}
                        ]
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box", "layout": "vertical", "margin": "md",
                        "contents": [
                            {"type": "text", "text": "🔔 ข่าวที่ 3", "weight": "bold", "size": "sm", "color": "#EC008C"},
                            {"type": "text", "text": "โครงการปลูกต้นไม้เพื่อชุมชน ปี 2568", "size": "sm", "wrap": True},
                            {"type": "text", "text": "รับสมัครอาสาสมัคร ติดต่อที่ทำการผู้ใหญ่บ้าน", "size": "xs", "color": "#888888", "wrap": True}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "ข้อมูล ณ วันที่ 22 ก.พ. 2568", "size": "xs", "color": "#AAAAAA", "align": "center"}]
            }
        }
    }

def get_document_message():
    return {
        "type": "flex",
        "altText": "ขอเอกสาร/ใบรับรอง",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "📄 ขอเอกสาร/ใบรับรอง", "weight": "bold", "size": "lg", "color": "#FFFFFF"}],
                "backgroundColor": "#003087", "paddingAll": "15px"
            },
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "เอกสารที่ต้องเตรียม:", "weight": "bold", "size": "md", "color": "#003087"},
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box", "layout": "vertical", "margin": "md", "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "✅ สำเนาบัตรประชาชน 1 ฉบับ", "size": "sm"},
                            {"type": "text", "text": "✅ สำเนาทะเบียนบ้าน 1 ฉบับ", "size": "sm"},
                            {"type": "text", "text": "✅ รูปถ่าย 1 นิ้ว 1 รูป (ถ้าจำเป็น)", "size": "sm"},
                            {"type": "text", "text": "✅ เอกสารประกอบอื่นๆ (ตามประเภท)", "size": "sm"}
                        ]
                    },
                    {"type": "separator", "margin": "md"},
                    {"type": "text", "text": "ประเภทเอกสารที่ให้บริการ:", "weight": "bold", "size": "sm", "color": "#EC008C", "margin": "md"},
                    {
                        "type": "box", "layout": "vertical", "margin": "sm", "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "• หนังสือรับรองการมีชีวิต", "size": "sm"},
                            {"type": "text", "text": "• หนังสือรับรองความประพฤติ", "size": "sm"},
                            {"type": "text", "text": "• หนังสือรับรองรายได้", "size": "sm"},
                            {"type": "text", "text": "• หนังสือรับรองที่อยู่อาศัย", "size": "sm"},
                            {"type": "text", "text": "• เอกสารอื่นๆ ตามความต้องการ", "size": "sm"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical", "spacing": "sm",
                "contents": [
                    {
                        "type": "button", "style": "primary", "color": "#EC008C",
                        "action": {"type": "message", "label": "📞 ติดต่อขอเอกสาร", "text": "ต้องการขอเอกสาร กรุณาแจ้งชื่อและประเภทเอกสาร"}
                    }
                ]
            }
        }
    }

def get_emergency_message():
    return {
        "type": "flex",
        "altText": "เบอร์โทรฉุกเฉิน",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "🚨 เบอร์โทรฉุกเฉิน", "weight": "bold", "size": "lg", "color": "#FFFFFF"}],
                "backgroundColor": "#CC0000", "paddingAll": "15px"
            },
            "body": {
                "type": "box", "layout": "vertical", "spacing": "sm",
                "contents": [
                    {"type": "text", "text": "กดปุ่มเพื่อโทรออกได้ทันที", "size": "sm", "color": "#888888", "align": "center"},
                    {"type": "separator", "margin": "md"},
                    {"type": "button", "style": "primary", "color": "#CC0000", "margin": "md",
                     "action": {"type": "uri", "label": "🚑 กู้ชีพ / EMS: 1669", "uri": "tel:1669"}},
                    {"type": "button", "style": "primary", "color": "#FF6600",
                     "action": {"type": "uri", "label": "🚒 ดับเพลิง: 199", "uri": "tel:199"}},
                    {"type": "button", "style": "primary", "color": "#003087",
                     "action": {"type": "uri", "label": "👮 ตำรวจ: 191", "uri": "tel:191"}},
                    {"type": "button", "style": "secondary", "margin": "md",
                     "action": {"type": "message", "label": "📞 ติดต่อผู้ใหญ่บ้าน", "text": "ต้องการติดต่อผู้ใหญ่บ้านโดยตรง"}}
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "ในกรณีฉุกเฉิน กรุณาโทร 191 หรือ 1669", "size": "xs", "color": "#CC0000", "align": "center", "wrap": True}]
            }
        }
    }

def get_lawyer_ai_message():
    return {
        "type": "flex",
        "altText": "ปรึกษาทนาย AI",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "⚖️ ปรึกษาทนาย AI", "weight": "bold", "size": "lg", "color": "#FFFFFF"}],
                "backgroundColor": "#003087", "paddingAll": "15px"
            },
            "body": {
                "type": "box", "layout": "vertical", "spacing": "md",
                "contents": [
                    {"type": "text", "text": "คุณสามารถปรึกษาข้อกฎหมายเบื้องต้นได้ฟรี!", "weight": "bold", "size": "sm", "wrap": True},
                    {"type": "text", "text": "ระบบทนาย AI พร้อมให้คำแนะนำในเรื่อง:\n• กฎหมายที่ดินและมรดก\n• สัญญาจ้างและหนี้สิน\n• กฎหมายครอบครัว\n• และข้อกฎหมายอื่นๆ ในชีวิตประจำวัน", "size": "xs", "color": "#555555", "wrap": True},
                    {"type": "separator", "margin": "md"},
                    {"type": "text", "text": "คลิกปุ่มด้านล่างเพื่อเริ่มปรึกษาได้ทันทีครับ 👇", "size": "xs", "color": "#888888", "align": "center"}
                ]
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {
                        "type": "button", "style": "primary", "color": "#EC008C",
                        "action": {"type": "uri", "label": "⚖️ เริ่มปรึกษาทนาย AI", "uri": "https://sunlawai-3rquvesc.manus.space/"}
                    }
                ]
            }
        }
    }

@app.route("/", methods=["GET"])
def index():
    return "LINE Webhook Server is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data()
    
    if not verify_signature(body, signature):
        abort(400)
        
    events = request.json.get("events", [])
    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            reply_token = event["replyToken"]
            text = event["message"]["text"]
            
            if text == 'ข่าวสารหมู่บ้าน':
                reply_message(reply_token, [get_news_message()])
            elif text == 'ขอเอกสาร/ใบรับรอง':
                reply_message(reply_token, [get_document_message()])
            elif text == 'เบอร์โทรฉุกเฉิน':
                reply_message(reply_token, [get_emergency_message()])
            elif text == 'คำถามที่พบบ่อย':
                reply_text = "❓ คำถามยอดฮิตสำหรับลูกบ้าน:\n1. การทำบัตรประชาชนใหม่\n2. การแจ้งย้ายที่อยู่\n3. การรับเงินอุดหนุนเด็ก\n4. การขอใบรับรองความประพฤติ\n5. การแจ้งเหตุเหตุด่วนเหตุร้าย\n6. ปรึกษาข้อกฎหมาย (ทนาย AI)\n\nต้องการทราบรายละเอียดข้อไหน พิมพ์หมายเลขได้เลยครับ"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == 'ติดต่อผู้ใหญ่บ้าน':
                reply_text = "📞 ช่องทางการติดต่อผู้ใหญ่บ้าน:\n- โทร: [เบอร์โทรของคุณ]\n- ที่ทำการ: [ที่อยู่ของคุณ]\n\nหรือพิมพ์ข้อความทิ้งไว้ที่นี่ได้เลยครับ ผมจะรีบมาตอบกลับ"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == 'ทนาย AI' or 'ทนาย' in text:
                reply_message(reply_token, [get_lawyer_ai_message()])
            elif text == '1':
                reply_text = "🪪 การทำบัตรประชาชนใหม่:\n1. เตรียมบัตรเดิม (ถ้ามี)\n2. ไปที่อำเภอ/เทศบาล\n3. ค่าธรรมเนียม 100 บาท (กรณีหาย/ชำรุด)\n\nไม่ต้องใช้สำเนาทะเบียนบ้านแล้วครับ"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == '2':
                reply_text = "🏠 การแจ้งย้ายที่อยู่:\n1. เจ้าบ้านนำทะเบียนบ้านไปแจ้งที่อำเภอ\n2. แจ้งย้ายเข้าภายใน 15 วัน\n3. เตรียมบัตรประชาชนเจ้าบ้านและผู้ย้าย"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == '3':
                reply_text = "👶 การรับเงินอุดหนุนเด็ก:\n1. เด็กอายุ 0-6 ปี\n2. รายได้ครอบครัวเฉลี่ยไม่เกิน 100,000 บาท/คน/ปี\n3. ลงทะเบียนได้ที่ อบต./เทศบาล"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == '4':
                reply_text = "📄 การขอใบรับรองความประพฤติ:\n1. เตรียมบัตรประชาชน\n2. มาพบผู้ใหญ่บ้านที่ที่ทำการ\n3. แจ้งวัตถุประสงค์การนำไปใช้"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == '5':
                reply_text = "🚨 การแจ้งเหตุเหตุด่วนเหตุร้าย:\n1. โทร 191 ทันที\n2. แจ้งพิกัดและลักษณะเหตุการณ์\n3. แจ้งชื่อและเบอร์โทรผู้แจ้ง\n\nหรือกดปุ่ม 'เบอร์โทรฉุกเฉิน' เพื่อดูเบอร์อื่นๆ ครับ"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
            elif text == '6':
                reply_message(reply_token, [get_lawyer_ai_message()])
            else:
                # ข้อความทั่วไป
                reply_text = f"สวัสดีครับ ผมเป็นผู้ช่วยอัตโนมัติของคุณ\nคุณพิมพ์ว่า: {text}\n\nหากต้องการความช่วยเหลือ กรุณากดเมนูที่ด้านล่างได้เลยครับ 🙏"
                reply_message(reply_token, [{"type": "text", "text": reply_text}])
                
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
