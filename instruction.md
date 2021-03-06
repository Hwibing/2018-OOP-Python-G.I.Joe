# 0. 소개
저희 Millstone은 한 마디로,
미래를 예측하여 자본을 불리는 게임입니다!
게임을 시작하기 위해서는 GUI.py 파일을 실행해주세요.
단축키 목록은 다음과 같습니다.
Esc - 창 닫기(메인 윈도우 제외)
Ctrl+S - 잠자기
q, w, e, r: 물건 품목별로 접기/펴기

# 1. 게임 진행 
처음엔 500000τ(가상의 화폐 단위)로 시작합니다.
게임을 시작하면 은행, 창고, 목록, 체크박스 등이 보입니다.
이 게임에서는 물건을 사고 팔며 자본을 불리는 것이 제일 중요합니다.
'잠자기' 버튼을 눌러 다음 주로 넘어갈 수 있습니다.
물건의 가격은 주 단위로 바뀝니다.
가진 모든 수단을 활용하여 자본을 축적하세요!

# 2. 뉴스 & 예측
뉴스는 매일 새로 나타납니다.
뉴스에 따라 상품의 가격이 변하게 됩니다. 
하단의 '예측하기' 버튼을 누르면 아직 나타나지 않은 뉴스를 25000τ를 지불하고 미리 볼 수 있습니다.

# 3. 물건 구매/판매
물건 리스트에서 어떤 것을 선택하면 그 상품을 판매/구매할 수 있습니다.
(각 상품은 주 단위로 가격이 변동합니다: 문단 2 참고)
개수를 입력한 뒤, 구매/판매를 누르면 그만큼의 돈을 잃고 해당 물건이 창고로 들어옵니다.
'최댓값'을 누르면 현재 돈으로 살 수 있는 값을 자동으로 넣어줍니다.
'보유량'을 누르면 창고에 있는 수량을 입력해줍니다.

## 3.1. 유통기한
농산물, 축/수산물은 유통기한이 존재합니다.
구매한 뒤 유통기간 동안 팔지 않으면, 자동으로 창고에서 사라집니다.

# 4. 적금 & 대출
'은행' 버튼을 누르면 은행 창이 열립니다.
액수를 입력하고 적금, 대출, 상환 버튼을 눌러 해당 기능을 사용할 수 있습니다.

## 4-1. 적금
'적금' 버튼은 가지고 있는 돈에서 일정 돈을 적금에 넣는 버튼입니다.
한 번 적금에 넣은 돈은 다시 뺄 수 없습니다.
단, 자고 일어났을 때, 적금에 넣었던 돈의 3%만큼 돈을 추가로 획득할 수 있습니다.

## 4-2. 대출 & 상환
긴급하게 돈이 많이 필요하다면, '대출' 단추를 눌러 돈을 빌리십시오!
그 즉시, 묻지도 따지지도 않고 수중에 돈을 추가해줍니다.
이자율은 10%로, 자고 일어났을 때 해당 액수만큼 차감됩니다.
상환하여 돈을 갚을 수 있습니다.

# 5. 창고
창고 용량은 기본 100이나, 매회 3000000τ를 지불하여 업그레이드 할 수 있습니다.
창고 용량은 80씩 늘어납니다.
더불어, 맨 처음엔 창고를 구매하지 않은 것으로 간주하여, 
매주 15000τ씩 대여료를 지불합니다.

# 6. 뉴스
이번 주의 뉴스를 봅니다. 첫 주엔 뉴스가 없습니다. 

# 7. 예측
내일의 뉴스를 예측합니다. 창을 닫으면 사라지니, 주의하세요!

# 8. 잠자기
다음 주로 넘어갑니다. 만일 다음 주에 돈이 음수로 내려간다면,
'파산하였습니다!'라는 문구와 함께 처음으로 돌아갑니다.

# 9. 종료
게임을 종료합니다.