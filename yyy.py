import pandas as pd
import numpy as np

# CSV 파일 경로
file_path = "원신_이벤트_리스트.csv"

# CSV 파일 불러오기
df = pd.read_csv(file_path)

# 텍스트 정리 함수 정의
def clean_text(text):
    if pd.isna(text):
        return np.nan
    return " ".join(str(text).split())

# 전체 데이터에 적용
df_cleaned = df.applymap(clean_text)

# 결과 저장
output_path = "원신_이벤트_리스트_정리본.csv"
df_cleaned.to_csv(output_path, index=False)

print("CSV 정리 완료! 저장 위치:", output_path)
