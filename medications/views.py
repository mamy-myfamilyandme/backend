from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import OCRService, ParsingService, ScheduleService

@csrf_exempt
@require_POST
def process_prescription_view(request):
    if 'file' not in request.FILES:
        return JsonResponse({"status": "error", "message": "파일이 없습니다."}, status=400)
    
    image_file = request.FILES['file']

    user_id = request.POST.get('user_id', 'test_user_01') 

    try:

        
        # Step 1: OCR 실행
        ocr_result = OCRService.get_ocr_result(image_file)
        if not ocr_result:
            return JsonResponse({"status": "error", "message": "OCR 서버 통신 실패"}, status=502)
        parsed_data = ParsingService.parse_html(ocr_result)
        if not parsed_data:
            return JsonResponse({
                "status": "warning", 
                "message": "처방전을 읽었으나 약품 정보를 찾을 수 없습니다.",
                "debug_raw": ocr_result  
            }, status=422)

        preview_data = ScheduleService.generate_preview(user_id, parsed_data)

        # 최종 응답
        return JsonResponse({
            "status": "success",
            "message": "약품 분석 및 스케줄 미리보기가 생성되었습니다.",
            "data": preview_data
        }, status=200)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
