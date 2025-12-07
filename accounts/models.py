from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 기본: username, password, email
    
    # 추가 정보 필드
    real_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    # 신체 정보
    height = models.FloatField(blank=True, null=True)  # 키 (cm)
    weight = models.FloatField(blank=True, null=True)  # 체중 (kg)
    
    # 혈액형 (선택형)
    BLOOD_TYPE_CHOICES = [
        ('A', 'A형'),
        ('B', 'B형'),
        ('O', 'O형'),
        ('AB', 'AB형'),
    ]
    RH_FACTOR_CHOICES = [
        ('+', 'Rh+'),
        ('-', 'Rh-'),
    ]
    blood_type = models.CharField(max_length=2, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)  # 혈액형 (ABO)
    rh_factor = models.CharField(max_length=1, choices=RH_FACTOR_CHOICES, blank=True, null=True)  # Rh 인자

    # 건강 상세 정보
    allergies = models.TextField(blank=True, null=True)  # 약물/음식 알레르기
    chronic_diseases = models.TextField(blank=True, null=True)  # 만성질환 (고혈압, 당뇨 등)
    surgery_history = models.TextField(blank=True, null=True)  # 과거 수술기록
    family_history = models.TextField(blank=True, null=True)  # 가족력
    current_medications = models.TextField(blank=True, null=True)  # 현재 복용중인 약물

    # 의료 기록 (텍스트로 상세 기입)
    vaccination_history = models.TextField(blank=True, null=True)  # 예방접종 기록
    medical_checkup_history = models.TextField(blank=True, null=True)  # 정기검진 및 진료 기록

    # 생활 습관 - 흡연
    SMOKING_STATUS_CHOICES = [
        ('NONE', '비흡연'),
        ('PAST', '과거 흡연'),
        ('CURRENT', '현재 흡연'),
    ]
    smoking_status = models.CharField(max_length=10, choices=SMOKING_STATUS_CHOICES, blank=True, null=True)
    smoking_daily_amount = models.CharField(max_length=50, blank=True, null=True)  # 하루 흡연량 (예: 반 갑, 10개비)

    # 생활 습관 - 음주
    DRINKING_STATUS_CHOICES = [
        ('NONE', '비음주'),
        ('DRINKER', '음주'),
    ]
    drinking_status = models.CharField(max_length=10, choices=DRINKING_STATUS_CHOICES, blank=True, null=True)
    drinking_average_amount = models.CharField(max_length=50, blank=True, null=True)  # 1회 평균 음주량 (예: 소주 1병)
    drinking_frequency = models.CharField(max_length=50, blank=True, null=True)  # 음주 주기 (예: 주 1회, 월 2회 등)
    last_drinking_date = models.DateField(blank=True, null=True)  # 마지막 음주 날짜

    # 생활 습관 - 운동
    EXERCISE_STATUS_CHOICES = [
        ('NONE', '운동 안 함'),
        ('YES', '운동 함'),
    ]
    exercise_status = models.CharField(max_length=10, choices=EXERCISE_STATUS_CHOICES, blank=True, null=True)
    exercise_frequency = models.CharField(max_length=50, blank=True, null=True)  # 운동 주기 (예: 주 3회)
    exercise_duration = models.CharField(max_length=50, blank=True, null=True)  # 1회 운동 시간 (예: 1시간, 30분)
    exercise_type = models.CharField(max_length=100, blank=True, null=True)  # 주된 운동 종류 (예: 헬스, 요가, 러닝)
    
    def __str__(self):
        return self.email