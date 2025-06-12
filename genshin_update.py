from bs4 import BeautifulSoup
import pandas as pd
import re

# HTML 파일 경로
html_path = "genshin_update.html"

# HTML 파일 열기
with open(html_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

results = []

# 모든 버전 헤더 찾기 (h2, h3, h4 중 '버전'이라는 단어가 들어간 경우)
version_headers = soup.find_all(['h2', 'h3', 'h4'])

target_versions = []
for tag in version_headers:
    text = tag.get_text(separator="\n").strip()
    if "버전" in text or re.match(r"\d+\.\d+", text):  # 예: '5.0 버전', '4.7', '업데이트 3.8'
        target_versions.append((text, tag))

for version, header in target_versions:
    info = {
        "버전": version,
        "신규 캐릭터": "",
        "복각 캐릭터": "",
        "신규 무기": "",
        "이벤트": "",
        "신규 명함": "",
        "신규 전설 임무": ""
    }

    # 다음 버전 전까지의 텍스트 수집
    content = ""
    next_tag = header.find_next_sibling()
    while next_tag and next_tag.name not in ['h2', 'h3', 'h4']:
        content += next_tag.get_text(separator="\n")
        next_tag = next_tag.find_next_sibling()

    # 각 항목 추출
    patterns = {
        "신규 캐릭터": r"신규\s*캐릭터\s*[:：]?\s*(.+)",
        "복각 캐릭터": r"복각\s*캐릭터\s*[:：]?\s*(.+)",
        "신규 무기": r"신규\s*무기\s*[:：]?\s*(.+)",
        "이벤트": r"이벤트\s*[:：]?\s*(.+)",
        "신규 명함": r"신규\s*명함\s*[:：]?\s*(.+)",
        "신규 전설 임무": r"신규\s*전설\s*임무\s*[:：]?\s*(.+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            info[key] = match.group(1).strip()

    results.append(info)

# DataFrame으로 저장
df = pd.DataFrame(results)
df.to_csv("원신_전체_업데이트.csv", index=False, encoding='utf-8-sig')
