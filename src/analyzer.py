def calculate_relevance(notice, config):
    score = 0
    title = notice.get("title", "").lower()
    interests = [i.lower() for i in config.get("interests", [])]

    high_priority = ["学科竞赛", "挑战杯", "数学建模", "电子设计", "创新创业"]
    medium_priority = ["奖学金", "评优", "保研", "考研", "实习", "就业"]
    low_priority = ["讲座", "培训", "科技创新", "科研", "论文", "英语", "计算机", "编程"]

    for keyword in high_priority:
        if keyword.lower() in title:
            score += 30

    for keyword in medium_priority:
        if keyword.lower() in title:
            score += 20

    for keyword in low_priority:
        if keyword.lower() in title:
            score += 10

    major_keywords = ["机械", "机电", "电子", "工程", "自动化", "制造"]
    for kw in major_keywords:
        if kw in title:
            score += 15

    class_keywords = ["班长", "班委", "124120402", "学生会"]
    for kw in class_keywords:
        if kw in title:
            score += 25

    for interest in interests:
        if interest in title:
            score += 5

    score = min(score, 100)
    return score

def analyze_notices(notices, config):
    min_score = config.get("min_relevance_score", 30)
    analyzed = []

    for notice in notices:
        score = calculate_relevance(notice, config)
        if score >= min_score:
            notice["relevance_score"] = score
            notice["relevance_level"] = get_relevance_level(score)
            analyzed.append(notice)

    analyzed.sort(key=lambda x: x["relevance_score"], reverse=True)
    return analyzed

def get_relevance_level(score):
    if score >= 80:
        return "极高相关"
    elif score >= 60:
        return "高相关"
    elif score >= 40:
        return "中等相关"
    else:
        return "一般相关"
