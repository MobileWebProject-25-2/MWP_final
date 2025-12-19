"""
분리수거 객체 검출 및 Django 서버 전송 모듈
YOLOv5로 검출된 객체를 분석하여 분리수거 가이드 제공

추가 기능:
- 1-5. 검출 신뢰도 필터링: 설정한 신뢰도 이상만 처리 (오검출 방지)
"""

import os
import cv2
import pathlib
import requests
from datetime import datetime


class RecyclingDetection:
    """분리수거 객체 검출 및 서버 전송 클래스"""
    
    result_prev = []
    
    # ============== 서버 설정 ==============
    HOST = 'http://127.0.0.1:8000'
    username = 'ksw'
    password = '1234'
    token = ''
    title = ''
    text = ''
    
    # ============== 1-5. 신뢰도 필터링 설정 ==============
    # 0.0 ~ 1.0 사이 값 (기본값 0.5 = 50%)
    # 이 값 이상의 신뢰도를 가진 객체만 분리수거 가이드 표시
    CONFIDENCE_THRESHOLD = 0.5
    
    # ============== 분리수거 카테고리 매핑 ==============
    RECYCLING_MAP = {
        # 유리류
        'bottle': {'category': '유리', 'guide': '내용물을 비우고 라벨을 제거한 후 유리류 수거함에 버리세요.'},
        'wine glass': {'category': '유리', 'guide': '깨지지 않게 신문지로 감싸서 유리류 수거함에 버리세요.'},
        
        # 플라스틱/일반
        'cup': {'category': '플라스틱/일반쓰레기', 'guide': '재질 확인 필요. 종이컵은 일반쓰레기, 플라스틱컵은 플라스틱류로 분리하세요.'},
        
        # 고철류
        'fork': {'category': '고철', 'guide': '금속류 수거함에 버리세요.'},
        'knife': {'category': '고철', 'guide': '안전하게 포장 후 금속류 수거함에 버리세요.'},
        'spoon': {'category': '고철', 'guide': '금속류 수거함에 버리세요.'},
        'scissors': {'category': '고철', 'guide': '금속류 수거함에 버리세요. 날카로운 부분은 테이프로 감싸세요.'},
        
        # 일반쓰레기
        'bowl': {'category': '일반쓰레기', 'guide': '도자기/사기 재질은 일반쓰레기로 버리세요.'},
        'potted plant': {'category': '일반쓰레기', 'guide': '화분은 일반쓰레기, 흙은 소량만 일반쓰레기로 가능합니다.'},
        'vase': {'category': '일반쓰레기', 'guide': '도자기/유리 재질에 따라 분류. 깨진 경우 신문지로 감싸세요.'},
        'teddy bear': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'toothbrush': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'backpack': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'umbrella': {'category': '일반쓰레기', 'guide': '천과 금속 분리가 어려우면 일반쓰레기로 버리세요.'},
        'handbag': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        
        # 음식물쓰레기
        'banana': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요. 바나나 껍질도 가능합니다.'},
        'apple': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요.'},
        'sandwich': {'category': '음식물쓰레기', 'guide': '포장재는 분리하고 음식물만 음식물쓰레기로 버리세요.'},
        'orange': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요.'},
        'broccoli': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요.'},
        'carrot': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요.'},
        'hot dog': {'category': '음식물쓰레기', 'guide': '포장재는 분리하고 음식물만 음식물쓰레기로 버리세요.'},
        'pizza': {'category': '음식물쓰레기', 'guide': '피자박스는 기름이 묻으면 일반쓰레기, 깨끗하면 종이류로 분리하세요.'},
        'donut': {'category': '음식물쓰레기', 'guide': '음식물쓰레기 수거함에 버리세요.'},
        'cake': {'category': '음식물쓰레기', 'guide': '케이크 상자는 종이류, 내용물은 음식물쓰레기로 분리하세요.'},
        
        # 대형폐기물
        'chair': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'couch': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'bed': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'dining table': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'toilet': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'sink': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요. (구청/주민센터 문의)'},
        'suitcase': {'category': '대형폐기물', 'guide': '크기에 따라 대형폐기물 또는 일반쓰레기로 분류하세요.'},
        
        # 폐가전
        'tv': {'category': '폐가전', 'guide': '폐가전 무상수거 서비스(1599-0903)를 이용하세요.'},
        'laptop': {'category': '폐가전', 'guide': '폐가전 무상수거 서비스를 이용하거나 소형가전 수거함에 버리세요.'},
        'mouse': {'category': '폐가전', 'guide': '소형가전 수거함에 버리세요.'},
        'remote': {'category': '폐가전', 'guide': '건전지를 분리 후 소형가전 수거함에 버리세요.'},
        'keyboard': {'category': '폐가전', 'guide': '소형가전 수거함에 버리세요.'},
        'cell phone': {'category': '폐가전', 'guide': '소형가전 수거함에 버리거나 대리점에서 수거합니다.'},
        'microwave': {'category': '폐가전', 'guide': '폐가전 무상수거 서비스(1599-0903)를 이용하세요.'},
        'oven': {'category': '폐가전', 'guide': '폐가전 무상수거 서비스를 이용하세요.'},
        'toaster': {'category': '폐가전', 'guide': '소형가전 수거함에 버리세요.'},
        'refrigerator': {'category': '폐가전', 'guide': '폐가전 무상수거 서비스(1599-0903)를 이용하세요.'},
        'hair drier': {'category': '폐가전', 'guide': '소형가전 수거함에 버리세요.'},
        'clock': {'category': '폐가전/일반쓰레기', 'guide': '전자시계는 소형가전, 일반시계는 일반쓰레기로 분류하세요.'},
        
        # 종이류
        'book': {'category': '종이류', 'guide': '비닐 코팅된 표지는 제거 후 종이류 수거함에 버리세요.'},
        
        # 의류
        'tie': {'category': '의류', 'guide': '의류수거함에 버리거나 일반쓰레기로 버리세요.'},
        
        # 기타
        'person': {'category': '감지됨', 'guide': '사람이 감지되었습니다.'},
        'bicycle': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'car': {'category': '폐차', 'guide': '폐차장에 문의하세요.'},
        'motorcycle': {'category': '폐차', 'guide': '이륜차 폐차장에 문의하세요.'},
        'airplane': {'category': '확인필요', 'guide': '장난감인 경우 플라스틱/일반쓰레기로 분류하세요.'},
        'bus': {'category': '폐차', 'guide': '폐차장에 문의하세요.'},
        'train': {'category': '확인필요', 'guide': '장난감인 경우 재질에 따라 분류하세요.'},
        'truck': {'category': '폐차', 'guide': '폐차장에 문의하세요.'},
        'boat': {'category': '확인필요', 'guide': '재질에 따라 분류하세요.'},
        'traffic light': {'category': '폐가전', 'guide': '전자제품 수거함에 버리세요.'},
        'fire hydrant': {'category': '고철', 'guide': '금속류로 분류하세요.'},
        'stop sign': {'category': '고철', 'guide': '금속류로 분류하세요.'},
        'parking meter': {'category': '폐가전', 'guide': '전자제품 수거함에 버리세요.'},
        'bench': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'bird': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'cat': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'dog': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'horse': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'sheep': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'cow': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'elephant': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'bear': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'zebra': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'giraffe': {'category': '확인필요', 'guide': '동물은 분리수거 대상이 아닙니다.'},
        'frisbee': {'category': '플라스틱', 'guide': '플라스틱류 수거함에 버리세요.'},
        'skis': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'snowboard': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'sports ball': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'kite': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'baseball bat': {'category': '일반쓰레기', 'guide': '재질에 따라 분류. 금속은 고철, 나무/플라스틱은 일반쓰레기.'},
        'baseball glove': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
        'skateboard': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'surfboard': {'category': '대형폐기물', 'guide': '대형폐기물로 신고 후 배출하세요.'},
        'tennis racket': {'category': '일반쓰레기', 'guide': '일반쓰레기 종량제 봉투에 버리세요.'},
    }
    
    def __init__(self, names):
        """초기화"""
        self.names = names
        self.result_prev = [0 for i in range(len(names))]
        self.confidence_values = {}  # 1-5. 신뢰도 저장용
        self._authenticate()
        print(f"🎯 신뢰도 필터링 활성화: {self.CONFIDENCE_THRESHOLD * 100}% 이상만 처리")
    
    def _authenticate(self):
        """Django 서버에 로그인하여 JWT 토큰 획득"""
        try:
            res = requests.post(self.HOST + '/api-token-auth/', {
                'username': self.username,
                'password': self.password,
            }, timeout=10)
            res.raise_for_status()
            self.token = res.json()['access']
            print(f"✅ 서버 인증 성공! Token: {self.token[:20]}...")
        except requests.exceptions.ConnectionError:
            print(f"❌ 서버 연결 실패: {self.HOST} 에 연결할 수 없습니다.")
            print("   Django 서버가 실행 중인지 확인하세요.")
            self.token = ''
        except requests.exceptions.RequestException as e:
            print(f"❌ 인증 실패: {e}")
            self.token = ''
    
    def get_recycling_info(self, class_name):
        """객체 이름으로 분리수거 정보 조회"""
        if class_name in self.RECYCLING_MAP:
            return self.RECYCLING_MAP[class_name]
        return {'category': '확인필요', 'guide': '해당 물품의 재질을 확인하여 분리수거해주세요.'}
    
    def add(self, names, detected_current, save_dir, image):
        """객체 출현 변화 감지 및 처리"""
        self.title = ''
        self.text = ''
        detected_items = []
        change_flag = 0
        
        for i in range(len(self.result_prev)):
            # 새로 출현한 객체 감지 (0 -> 1)
            if self.result_prev[i] == 0 and detected_current[i] == 1:
                item_name = names[i]
                
                # ============== 1-5. 신뢰도 필터링 ==============
                # 신뢰도가 저장되어 있고, 임계값 이상인 경우만 처리
                if item_name in self.confidence_values:
                    confidence = self.confidence_values[item_name]
                    if confidence < self.CONFIDENCE_THRESHOLD:
                        print(f"⚠️ {item_name} 신뢰도 {confidence*100:.1f}% - 임계값({self.CONFIDENCE_THRESHOLD*100}%) 미만으로 건너뜀")
                        continue
                    print(f"✓ {item_name} 신뢰도 {confidence*100:.1f}% - 처리 진행")
                # ================================================
                
                change_flag = 1
                recycling_info = self.get_recycling_info(item_name)
                detected_items.append({
                    'name': item_name,
                    'category': recycling_info['category'],
                    'guide': recycling_info['guide'],
                    'confidence': self.confidence_values.get(item_name, 0)
                })
        
        # 상태 저장
        self.result_prev = detected_current[:]
        
        if change_flag == 1 and detected_items:
            # 첫 번째 감지된 아이템을 title로
            self.title = f"[{detected_items[0]['category']}] {detected_items[0]['name']}"
            
            # 모든 감지된 아이템의 가이드를 text로
            guides = []
            for item in detected_items:
                guides.append(f"🔹 {item['name']} ({item['confidence']*100:.1f}%): {item['guide']}")
            self.text = '\n'.join(guides)
            
            self.send(save_dir, image)
            
            # 콘솔에도 출력
            print("\n" + "="*50)
            print("🔍 분리수거 가이드")
            print("="*50)
            for item in detected_items:
                print(f"📦 품목: {item['name']}")
                print(f"📊 신뢰도: {item['confidence']*100:.1f}%")
                print(f"📂 분류: {item['category']}")
                print(f"💡 방법: {item['guide']}")
                print("-"*50)
    
    def update_confidence(self, class_name, confidence):
        """
        1-5. 검출 신뢰도 업데이트
        detect.py에서 호출하여 각 클래스의 신뢰도를 저장
        """
        self.confidence_values[class_name] = confidence
    
    def send(self, save_dir, image):
        """검출 결과를 서버로 전송"""
        if not self.token:
            print("❌ 토큰이 없어 전송을 건너뜁니다.")
            return
            
        now = datetime.now()
        today = datetime.now()
        
        # 이미지 저장 경로 생성
        save_path = pathlib.Path(os.getcwd()) / save_dir / 'detected' / str(today.year) / str(today.month) / str(today.day)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        
        full_path = save_path / f'{today.hour}-{today.minute}-{today.second}-{today.microsecond}.jpg'
        
        # 이미지 리사이즈 및 저장
        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(full_path), dst)
        
        # API 요청 헤더
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json'
        }
        
        # POST 데이터
        data = {
            'title': self.title,
            'text': self.text,
            'created_date': now.isoformat(),
            'published_date': now.isoformat()
        }
        
        try:
            with open(full_path, 'rb') as f:
                files = {'image': f}
                res = requests.post(
                    self.HOST + '/api_root/Post/',
                    data=data,
                    files=files,
                    headers=headers,
                    timeout=30
                )
            print(f"📤 서버 전송 결과: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 전송 실패: {e}")