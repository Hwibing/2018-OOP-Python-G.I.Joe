# 2018-2 객체지향 프로그래밍 프로젝트 - **Millstone**
구성원: 2-1 박해준 | 2-4 정영근 | 2-5 권정준

## 1. 주제
**뉴스를 보고 시세를 예측**하여 자본을 늘리는 게임

## 2. 동기
정치경제 과목을 수강하는 도중, 주식 투자에 앞서 뉴스기사 등을 통해 현재 시장 상황을 읽는 능력이 제일 중요하다는 것을 깨달았다. 시장경제에 무지하지만 주식시장에 진입하고 싶은 신규 투자자들에게 뉴스에 따라 시장경제를 연습할 수 있는 기회를 주는 프로그램을 설계하기로 하였다.

## 3. 프로그램 사용 대상
시장 경제를 예측하는 훈련을 하고 싶은 사람. (옆에 정치경제 선생님을 두고 즐기면 재미가 2배!)

## 4. 목적
본 프로젝트의 의의는 사용자로 하여금 뉴스를 통해 미래의 시장 경제를 예측할 기회를 제공하고, 그를 기반으로 투자하도록 해 자본을 축적하도록 유도하는 것이다. 이 외에도 현실적인 거래 시스템을 제공하여 사용자가 더욱 몰입할 수 있게 한다.

## 5. 주요 기능
### 1) 날짜에 따른 무작위 이벤트
 * 날짜에 따라 무작위로 바뀌는 시장 상황, 그를 사용자에게 뉴스로 제공  
 * 예: 기상청 曰 “태풍이 한반도를 강타할 것으로 예상됩니다.”

### 2) 이벤트에 따른 물가 변동
 * 랜덤으로 제시된 시장 상황에 따른 물건 가격의 변동  
 * 예: 기상청 曰 “태풍이 한반도를 강타할 것으로 예상됩니다.” → 농산물 가격 상승

### 3) 다양한 거래 시스템
 * 저축, 적금, 대출(이자 존재)
 * 창고 임대료(보관 기간 차별화)
 * 선물거래

### 4) 물품 별 특징 구현
 * 예 1: 농산물은 유통기한이 존재 → 보관 중 가치 하락
 * 예 2: 금(Gold)은 안정적 → 가치 변동 적음

### 5) 게임의 재미를 위한 요소 추가
 * 도둑 이벤트 (보안업체 등 추가 가능)
 * 랜덤박스

### 6) 정보료를 내고 조금 더 많은 뉴스(정보)를 받아볼 수 있다. 

## 6. 프로젝트 핵심
주요 기능 구현의 핵심은 두 가지이다. 첫째는 ‘다양한 현실적인 시장 상황 제공’이다. 이는 게임 내에 구현될 날짜 시스템을 이용하면 된다. 시장 상황은 게임 내 날짜에 의해 결정된다. 예를 들어, 김장철에 배추 가격이 올라가는 방식(수요 증가)이다. 둘째는 ‘시장 상황에 따른 물가의 변동 적용’이다. 뉴스와 물품들을 클래스로 표현하고, 뉴스가 물품 가격에 미치는 영향을 메소드로 대응시키고자 한다. 

## 7. 구현에 필요한 라이브러리나 기술
 * PyQt: 유저 인터페이스를 구현하기 위해 사용한다.  
 * matplotlib: 물가 그래프를 그릴 때 유용하게 쓸 수 있다. 

## 8. 분업 계획
### 정영근
 * 클래스 설계
 * 시스템 로직 코딩

### 박해준
 * GUI 구현
 * 일러스트 제작

### 권정준
 * 게임 스토리 설계
 * 시스템 디자인, 코딩

## 9. 기타

<hr>

#### readme 작성관련 참고하기 [바로가기](https://heropy.blog/2017/09/30/markdown/)

#### 예시 계획서 [[예시 1]](https://docs.google.com/document/d/1hcuGhTtmiTUxuBtr3O6ffrSMahKNhEj33woE02V-84U/edit?usp=sharing) | [[예시 2]](https://docs.google.com/document/d/1FmxTZvmrroOW4uZ34Xfyyk9ejrQNx6gtsB6k7zOvHYE/edit?usp=sharing)
