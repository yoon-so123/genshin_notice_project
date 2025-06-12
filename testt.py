import requests
from bs4 import BeautifulSoup
import csv

url = 'https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    target_sections = ['신규 캐릭터', '복각 캐릭터', '신규 무기', '이벤트']

    data = []  # 저장할 데이터 리스트 (각 항목은 [섹션명, 내용])

    for header in soup.find_all(['h2', 'h3']):
        header_text = header.get_text(strip=True)

        for section in target_sections:
            if section.replace(" ", "") in header_text.replace(" ", ""):
                # 다음 노드들을 탐색하며 내용 수집
                next_node = header.find_next_sibling()
                while next_node:
                    if next_node.name in ['h2', 'h3']:
                        break

                    if next_node.name in ['ul', 'ol', 'div']:
                        items = next_node.find_all('li')
                        if items:
                            for li in items:
                                text = li.get_text(strip=True)
                                data.append([section, text])
                        else:
                            # li가 없으면 div 안 텍스트 통째로 저장
                            text = next_node.get_text(strip=True)
                            if text:
                                data.append([section, text])
                    next_node = next_node.find_next_sibling()

    # CSV 저장
    with open('output.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Section', 'Content'])  # 헤더
        writer.writerows(data)

    print("CSV 파일로 저장 완료: output.csv")

else:
    print(f"요청 실패: 상태 코드 {response.status_code}")
