# V-SAMS: 시각 기반 표면 분석 및 매칭 시스템 (Visual-based Surface Analysis & Matching System)

## 개요 (Overview)
V-SAMS는 산업용 제품(피착제)의 사진을 분석하여 **모재의 종류**와 **표면 마감 상태**를 식별하는 지능형 시스템입니다. 분석된 표면 특성(표면 에너지, 거칠기 등)을 바탕으로 최적의 보호 필름을 자동으로 추천합니다.

**핵심 기능:**
- **시각적 분석 (Visual Analysis)**: 딥러닝을 활용하여 재질(예: 금속, 플라스틱)과 질감(예: 거울면, 거친면)을 동시에 분류합니다.
- **지능형 매칭 (Intelligent Matching)**: 시각적 특성을 물리적 속성으로 변환하여 적합한 보호 필름을 추천합니다.
- **현장 난제 해결**: 반사(Specular Reflection) 및 스케일 모호성 문제를 해결하기 위한 특화된 알고리즘을 적용합니다.

## 기술 스택 (Tech Stack)
- **AI Core**: PyTorch, timm (ResNet50), Albumentations
- **App/UI**: Streamlit (빠른 프로토타이핑)
- **Backend**: Python (FastAPI 호환 구조)
- **Data**: 전이 학습(Transfer Learning)을 위해 MINC(재질) 및 DTD(텍스처) 오픈 데이터셋 활용

## 설치 방법 (Installation)

1. **저장소 복제 (Clone)**:
   ```bash
   git clone <repository-url>
   cd V-SAMS
   ```

2. **가상 환경 설정 (권장)**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **의존성 패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

## 사용법 (Usage)

### 1. 메인 데모 앱 (Prototype Demo)
피착제 분석 및 보호필름 추천 시연을 위한 메인 애플리케이션입니다.
```bash
python -m streamlit run app.py
```
*   **사용자 모드 (User Demo)**: 사진을 업로드하고 AI 분석 및 추천 결과를 확인합니다.
*   **관리자 모드 (DB Management)**: 사이드바에서 모드를 변경하여 신규 제품을 데이터베이스에 등록할 수 있습니다. (한/영 토글 지원)

### 2. 데이터 라벨링 툴 (Labeling Tool)
AI 학습용 데이터를 쉽고 빠르게 수집/관리하기 위한 도구입니다.
```bash
python -m streamlit run labeler.py
```
*   **기능**: 이미지를 드래그 앤 드롭으로 업로드하고, 재질/마감 속성을 클릭하면 자동으로 폴더(`dataset/train/클래스명`)에 분류하여 저장합니다.
*   **가이드**: 상세한 데이터 구축 가이드는 `data_collection_guide.md`를 참고하세요.

## 프로젝트 구조 (Project Structure)
```text
V-SAMS/
├── app.py                  # 메인 데모 애플리케이션 (Streamlit)
├── labeler.py              # 데이터 라벨링 도구 (Streamlit)
├── database.json           # 제품 정보 및 추천 로직용 가상 DB
├── data_collection_guide.md # 데이터 수집 가이드라인
├── models/
│   └── classifier.py       # AI 모델 아키텍처 (ResNet50 + Multi-Head)
├── utils/
│   └── db_handler.py       # DB 로드/저장 및 검색 유틸리티
├── requirements.txt        # 의존성 목록
└── README.md               # 프로젝트 설명서
```

## 현재 진행 상황 (Current Status)
이 프로젝트는 **초기 프로토타입 (PoC)** 단계입니다.
*   **AI 모델**: `models/classifier.py`에 구조는 구현되어 있으나, 가중치는 학습되지 않았습니다(Mock Prediction 사용).
*   **데이터베이스**: `database.json` 파일을 사용하는 경량 DB 구조이며, Admin 모드에서 관리 가능합니다.
*   **데이터 수집**: `labeler.py` 툴과 `data_collection_guide.md` 가이드가 준비되어 수집 단계 진입 전입니다.

## 향후 계획 (Roadmap)
1.  **데이터 구축 Phase**:
    *   `labeler.py`를 사용하여 클래스당 100장 이상의 데이터 수집.
    *   다양한 조명 및 각도에서의 촬영 데이터 확보.
2.  **AI 학습 Phase**:
    *   수집된 데이터를 `train.py`로 학습시켜 모델 가중치(`.pth`) 생성.
    *   `app.py`의 Mock Logic을 실제 모델 추론(Inference) 코드로 교체.
3.  **고도화 Phase**:
    *   단순 매칭 로직을 점수제(Scoring) 기반의 퍼지 매칭으로 개선.
    *   JSON DB를 실제 RDBMS로 마이그레이션.

