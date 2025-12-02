import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.conf import settings
from urllib.parse import unquote # 공공데이터 인증키 디코딩용

# ---------------------------------------------------------
# 1. OCR Service (Upstage)
# ---------------------------------------------------------
class OCRService:
    @staticmethod
    def get_ocr_result(uploaded_file):
        api_key = settings.UPSTAGE_API_KEY
        if not api_key:
            raise ValueError("UPSTAGE_API_KEY가 설정되지 않았습니다.")

        url = "https://api.upstage.ai/v1/document-digitization"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        files = {"document": (uploaded_file.name, uploaded_file.file)}
        data = {"model": "document-parse"} 
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"OCR API Error: {e}")
            return None

# ---------------------------------------------------------
# 2. Parsing Service (HTML -> Data)
# ---------------------------------------------------------
class ParsingService:
    @staticmethod
    def parse_html(ocr_json):
        if not ocr_json:
            return []

        content = ocr_json.get("content", {})
        html_text = content.get("html") or content.get("text") or ""
        
        if not html_text:
            return []

        soup = BeautifulSoup(html_text, 'html.parser')
        parsed_list = []
        
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            # 유효한 행인지 검사 (컬럼 수 기준)
            if not cols or len(cols) < 4:
                continue
                
            col_texts = [col.get_text().strip() for col in cols]
            drug_name_cell = col_texts[0]

            # 9자리 약품 코드(EDI_CODE) 추출
            codes = re.findall(r'(\d{9})', drug_name_cell)
            
            if not codes:
                continue 

            try:
                # 정규식으로 숫자만 추출
                one_dose = re.sub(r'[^0-9.]', '', col_texts[1])   # 1회 투약량
                daily_freq = re.sub(r'[^0-9.]', '', col_texts[2]) # 1일 횟수
                total_days = re.sub(r'[^0-9.]', '', col_texts[3]) # 총 투약일수
                
                # 빈 값 처리 (기본값 1)
                if not daily_freq: daily_freq = "1"
                if not total_days: total_days = "1"
                
            except IndexError:
                continue

            # 추출된 코드별로 데이터 생성
            for code in codes:
                parsed_list.append({
                    "code": code, # EDI_CODE
                    "one_dose": one_dose,      
                    "daily_freq": int(float(daily_freq)), 
                    "total_days": int(float(total_days))
                })
                
        return parsed_list

# ---------------------------------------------------------
# 3. Drug Info Service (NEW: 공공데이터포털 연동)
# ---------------------------------------------------------
class DrugInfoService:
    @staticmethod
    def get_drug_detail(edi_code):
        """
        공공데이터포털 '의약품 낱알식별정보' API를 통해 약품 상세 정보 조회
        """
        # settings.py에 PUBLIC_DATA_PORTAL_KEY를 등록해야 합니다.
        service_key = settings.PUBLIC_DATA_PORTAL_KEY 
        base_url = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService03/getMdcinGrnIdntfcInfoList03"
        
        # 인증키 디코딩 (공공데이터포털 키는 보통 Encoding된 상태로 제공됨)
        # requests로 보낼 때는 Decoding된 키를 보내는 것이 안전함
        decoded_key = unquote(service_key)

        params = {
            "serviceKey": decoded_key,
            "edi_code": edi_code, # 보험코드 검색
            "type": "json",       # JSON 응답 요청
            "numOfRows": 1,
            "pageNo": 1
        }

        try:
            response = requests.get(base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # 응답 구조 파싱 (body -> items -> item)
            body = data.get("body", {})
            items = body.get("items")
            
            if items and isinstance(items, list):
                item = items[0] # 첫 번째 결과 사용
            elif items and isinstance(items, dict): # 결과가 하나면 dict로 올 수도 있음
                item = items.get("item")
                if isinstance(item, list): item = item[0]
            else:
                return None # 결과 없음

            if not item:
                return None

            # 필요한 정보만 추출하여 반환
            return {
                "name": item.get("ITEM_NAME"),
                "image_url": item.get("ITEM_IMAGE"),
                "entp_name": item.get("ENTP_NAME"), # 업체명
                "chart": item.get("CHART"),         # 성상 (모양 설명)
                "print_front": item.get("PRINT_FRONT"), # 식별문자
            }

        except Exception as e:
            print(f"Public Data API Error ({edi_code}): {e}")
            return None

# ---------------------------------------------------------
# 4. Schedule Service (DB 저장 X -> Preview 반환 O)
# ---------------------------------------------------------
class ScheduleService:
    @staticmethod
    def generate_preview(user_id, parsed_data):
        # db저장은 제외하고 임시로 
        preview_result = []
        start_date = datetime.now().date()

        drug_info_cache = {}

        for item in parsed_data:
            code = item['code']
            
            if code not in drug_info_cache:
                detail_info = DrugInfoService.get_drug_detail(code)
                if not detail_info:
                    detail_info = {
                        "name": f"약품정보 없음({code})",
                        "image_url": None,
                        "entp_name": "-",
                        "chart": "-"
                    }
                drug_info_cache[code] = detail_info
            
            drug_detail = drug_info_cache[code]

            schedule_dates = []
            freq = item['daily_freq']
            
            slots = []
            if freq >= 3: slots = ['morning', 'lunch', 'dinner']
            elif freq == 2: slots = ['morning', 'dinner']
            else: slots = ['morning']
            
            for i in range(item['total_days']):
                target_date = start_date + timedelta(days=i)
                
                daily_schedule = {
                    "date": target_date.strftime("%Y-%m-%d"),
                    "slots": slots
                }
                schedule_dates.append(daily_schedule)

            preview_result.append({
                "drug_info": {
                    "edi_code": code,
                    "name": drug_detail['name'],
                    "image_url": drug_detail['image_url'],
                    "entp_name": drug_detail['entp_name'],
                    "chart": drug_detail['chart'],
                    "one_dose": item['one_dose']
                },
                "prescription_info": {
                    "daily_freq": freq,
                    "total_days": item['total_days'],
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (start_date + timedelta(days=item['total_days']-1)).strftime("%Y-%m-%d")
                },
                "schedule_preview": schedule_dates 
            })
            
        return preview_result
