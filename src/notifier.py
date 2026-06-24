import requests
import json

def send_pushplus(token, title, content):
    url = "http://www.pushplus.plus/send"
    headers = {"Content-Type": "application/json"}
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "html",
    }

    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        result = resp.json()
        if result.get("code") == 200:
            print(f"[PushPlus] Sent: {title}")
            return True
        else:
            print(f"[PushPlus] Error: {result.get('msg', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"[PushPlus] Exception: {e}")
        return False

def format_notice_html(notice):
    score = notice.get("relevance_score", 0)
    level = notice.get("relevance_level", "未知")
    title = notice.get("title", "")
    url = notice.get("url", "")
    source = notice.get("source", "")
    date = notice.get("date", "")

    if score >= 80:
        color = "#e74c3c"
    elif score >= 60:
        color = "#e67e22"
    elif score >= 40:
        color = "#3498db"
    else:
        color = "#95a5a6"

    html = f"""
    <div style="margin-bottom:15px;padding:12px;border-left:4px solid {color};background:#f9f9f9;">
        <div style="font-size:16px;font-weight:bold;color:#333;margin-bottom:5px;">
            <a href="{url}" style="color:#333;text-decoration:none;">{title}</a>
        </div>
        <div style="font-size:13px;color:#666;margin-bottom:5px;">
            <span style="background:{color};color:white;padding:2px 8px;border-radius:3px;margin-right:8px;">{score}分 {level}</span>
            <span>来源: {source}</span>
            <span style="margin-left:8px;">{date}</span>
        </div>
        <div style="font-size:12px;color:#999;">
            <a href="{url}" style="color:#3498db;">查看原文</a>
        </div>
    </div>
    """
    return html

def send_notification(token, notices, config):
    if not notices:
        print("No new notices to notify.")
        return

    user = config.get("user", {})
    greeting = f"Hi {user.get('name', '同学')}，有新的通知公告！"

    html_content = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
        <h2 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px;">📚 重庆理工大学通知监控</h2>
        <p style="color:#555;font-size:14px;">{greeting}</p>
        <p style="color:#777;font-size:13px;">以下是与你相关的通知（共 {len(notices)} 条）：</p>
        <div style="margin-top:15px;">
    """

    for notice in notices[:10]:
        html_content += format_notice_html(notice)

    html_content += """
        </div>
        <div style="margin-top:20px;padding:10px;background:#ecf0f1;border-radius:5px;font-size:12px;color:#7f8c8d;">
            <p>💡 评分说明：满分100分，基于通知内容与你的专业、兴趣、班级的相关程度自动评估。</p>
            <p>🔗 本消息由 CQUT-Monitor 自动推送 | <a href="https://github.com">GitHub Actions</a></p>
        </div>
    </div>
    """

    title = f"📚 CQUT通知 | {len(notices)}条新消息"
    send_pushplus(token, title, html_content)
