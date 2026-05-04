
# 1. 라이브러리 로드 (필요한 도구 꺼내기)
    # train_test_split : train / test 용으로 data split
    # accuracy_score : 모델 정확도 계산
    # classification_report : 정답 별로 얼마나 맞췄고, 어디서 잘못됬는지 보여주는 도구
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# 2. 데이터 불러오기
df = pd.read_csv('your_data.csv') 
X = df.drop('target_column', axis=1) # 특성 데이터 (matrix)
y = df['target_column']              # 정답 데이터 (vector)

# 3. 데이터 분할 (학습용/시험용)
    # X_train, y_train : 학습용 (학습용 X를 기준으로 학습용 y가 나오는 규칙을 학습)
    # X_test, y_test : 시험용 (TEST용 X를 기준으로 test용 y가 나오는지 확인)    
    # test_size = 0.2 : 전체 중 20%가 test용 
    # stratify = y : 정답(y)의 비율을 test, train에 골고루 섞어달라는 것 
    # random_state=42 : 섞는 방식 고정
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4. 모델 초기화 및 학습 (여기를 원하는 모델로 교체)
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(max_depth=5) #모델에 따라 바뀜

#모델 상관없이 안 바뀐다.
model.fit(X_train, y_train) 

# 5. 예측 및 평가 (모델 상관없이 안 바뀜)
y_pred = model.predict(X_test)
print(f"정확도: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# 6. 결과 시각화 (선택 사항)
# plot_tree(model) 등