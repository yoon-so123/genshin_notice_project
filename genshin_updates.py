# import requests
# from bs4 import BeautifulSoup
# import csv

# url = "https://namu.wiki/w/원신/업데이트"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.text, "html.parser")

# # CSV 파일 세팅
# with open("genshin_updates.csv", "w", newline="", encoding="utf-8-sig") as f:
#     writer = csv.writer(f)
#     writer.writerow(["버전", "이름"])  # 컬럼 헤더

#     # '3. 적용된 업데이트' 헤딩 찾기
#     heading = soup.find("span", {"id": "3._적용된_업데이트"})
#     if heading:
#         section = heading.find_parent(["h2", "h3"])
#         # 다음 sibling들 중 li 항목들만 추출
#         for sibling in section.find_next_siblings():
#             # 같은 레벨 헤딩 나오면 종료
#             if sibling.name and sibling.name.startswith("h"):
#                 break
#             # li 요소 찾기
#             for li in sibling.select("li"):
#                 text = li.get_text(strip=True)
#                 # "5.x버전 - 이름" 형태로 분리
#                 if "버전" in text and " - " in text:
#                     version, name = text.split(" - ", 1)
#                     writer.writerow([version, name])
# print("genshin_updates.csv 생성 완료!")

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import re

# # 나무위키 URL
# url = "https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8"
# headers = {"User-Agent": "Mozilla/5.0"}
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")

# # 결과 담을 리스트
# results = []

# # 모든 heading 태그 중 h3로 된 '5.x 버전' 찾기
# headings = soup.find_all(['h2', 'h3', 'h4'])
# version_pattern = re.compile(r'^5\.[0-6] 버전')

# for heading in headings:
#     title = heading.get_text(strip=True)
#     if version_pattern.match(title):
#         version_name = title
#         content = []
#         sibling = heading.find_next_sibling()
#         while sibling and sibling.name not in ['h2', 'h3', 'h4']:
#             content.append(sibling.get_text(separator="\n").strip())
#             sibling = sibling.find_next_sibling()
#         full_text = "\n".join(content)
#         results.append({
#             "버전명": version_name,
#             "내용": full_text
#         })

# # DataFrame으로 저장
# print(results)
# df = pd.DataFrame(results)
# df.to_csv("genshin_5x_updates.csv", index=False, encoding="utf-8-sig")  # 한글 깨짐 방지용
# print("CSV 파일이 저장되었습니다.")

# results = []
# print(results)

import requests
from bs4 import BeautifulSoup
import csv

# 1. 크롤링할 URL
url = "https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# 2. 요청 보내기
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"페이지 요청 실패: {response.status_code}")
    exit()

# 3. 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 4. 특정 div 찾기
target_div = soup.find('div', class_='_6d28490a759486f05dae6f09c0c40434')

if not target_div:
    print("해당 div를 찾을 수 없습니다.")
    exit()

# 5. div 내용 줄 단위로 분리 (줄바꿈 기준 등)
# 줄바꿈이 없으면 <p>나 <li> 태그별로 추출하는 게 좋음
# 여기서는 간단히 줄바꿈 기준 텍스트 분리 시도

# 예시로, div 내 텍스트를 줄 단위로 분리 (또는 적절한 태그로 분리)
lines = target_div.get_text(separator='\n').split('\n')

# 6. CSV 저장
csv_filename = 'namuwiki_update_content.csv'
with open(csv_filename, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Content'])  # 헤더 작성
    for line in lines:
        clean_line = line.strip()
        if clean_line:  # 빈 줄 제외
            writer.writerow([clean_line])

print(f"크롤링 완료, {csv_filename} 파일에 저장했습니다.")

# import requests
# from bs4 import BeautifulSoup

# url = "https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# }

# response = requests.get(url, headers=headers)
# response.encoding = 'utf-8'  # 인코딩 지정

# soup = BeautifulSoup(response.text, 'html.parser')

# target_div = soup.find("div", class_="6d28490a759486f05dae6f09c0c40434")

# if target_div:
#     print("Found the target div!")
#     print(target_div.text[:500])  # 앞 500자만 출력 (너무 길면 안 보임)
# else:
#     print("Could not find the target div.")
