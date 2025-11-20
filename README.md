# Backend

> **Jira-Github 연동 프로젝트**  
> 브랜치명과 커밋 메시지에 Jira 이슈 키를 포함하여 자동 연동됩니다.

## 목차
- [기술 스택](#기술-스택)
- [개발 도구](#개발-도구)
- [빠른 시작](#빠른-시작-프로젝트-클론-후)
- [Jira 협업 가이드](#jira-협업-가이드)
- [프로젝트 구조](#프로젝트-구조)
- [유용한 uv 명령어](#유용한-uv-명령어)

---

## 기술 스택

- **Python**: 3.11
- **Django**: 4.2.16 (LTS)
- **Django REST Framework**: 3.15.2
- **Database**: PostgreSQL 16.6
- **Package Manager**: uv

## 개발 도구

- **black**: 코드 포맷팅 (>=25.1.0)
- **ruff**: 린터 (>=0.13.0)
- **pytest**: 테스팅 프레임워크 (>=8.4.2)
- **pytest-django**: Django 테스팅 (>=4.11.1)
- **pre-commit**: Git 훅 관리 (>=4.3.0)

---

## 빠른 시작 (프로젝트 클론 후)

### 1. uv 설치

#### macOS / Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)
```
# PowerShell 실행 정책 설정 (최초 1회)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# uv 설치
irm https://astral.sh/uv/install.ps1 | iex
```

#### macOS (Homebrew)
```
brew install uv
```

#### 설치 확인
```
uv --version
# 예상 출력: uv 0.9.x
```

### 2. PATH 설정 (필요한 경우)

#### Windows PowerShell
```
# 현재 세션에만 적용
$env:Path = "C:\Users\SSAFY\.local\bin;$env:Path"

# 영구 적용 (PowerShell 프로필에 추가)
echo '$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"' >> $PROFILE
```

#### Git Bash (Windows)
```
# ~/.bashrc 파일에 추가
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### macOS / Linux
```
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 프로젝트 클론 및 의존성 설치

```
# 레포 클론
git clone https://github.com/mamy-myfamilyandme/backend.git
cd backend

# 의존성 설치 (uv.lock 기반으로 정확히 같은 버전 설치)
uv sync
```

### 4. 설치 확인

```
# 설치된 패키지 확인
uv pip list

# Python 버전 확인
uv run python --version
```

**끝!** 이제 바로 개발 시작하시면 됩니다.

---

## Jira 협업 가이드

### 🔗 Jira-Github 연동 원리

**핵심:** 브랜치명, 커밋 메시지, PR 제목에 **Jira 이슈 키(예: MAMY-123)**를 포함하면 자동으로 Jira와 연동됩니다.

---

### 📋 워크플로우

#### 1. Jira에서 브랜치 생성 (권장)

Jira 이슈 페이지에서 브랜치를 생성하면 **이슈 키가 자동으로 포함**됩니다.

**절차:**
1. Jira 이슈 페이지 오른쪽 **"Development"** 패널 클릭
2. **"Create branch"** 버튼 클릭
3. Repository 및 Base branch 선택
4. Branch name 확인 (자동으로 `MAMY-123-description` 형태 생성)
5. **Create** 클릭

**자동 생성 예시:**
```
MAMY-123-add-vaccination-api
MAMY-124-fix-authentication-bug
```

#### 2. 수동으로 브랜치 생성하는 경우

Jira를 거치지 않고 직접 브랜치를 생성할 때는 **반드시 이슈 키를 포함**해야 합니다.

<img width="463" height="173" alt="이슈 키" src="https://github.com/user-attachments/assets/eb7cba73-726c-4162-91fc-22515a972a93" />

**브랜치 네이밍 컨벤션:**
```
<type>/<ISSUE-KEY>-<description>
```

**Type 분류:**
- `feature/`: 새로운 기능 개발
- `bugfix/`: 버그 수정
- `hotfix/`: 긴급 수정
- `refactor/`: 코드 리팩토링
- `docs/`: 문서 작업
- `test/`: 테스트 코드

**예시:**
```
git checkout -b feature/MAMY-123-child-vaccination-api
git checkout -b bugfix/MAMY-124-fix-auth-token
git checkout -b hotfix/MAMY-125-security-patch
git checkout -b refactor/MAMY-126-optimize-query
```

#### 3. 커밋 메시지 작성

**기본 포맷:**
```
[ISSUE-KEY] <type>: <description>
```

**Type 분류:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `docs`: 문서 수정
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 변경
- `style`: 코드 포맷팅
- `perf`: 성능 개선

**예시:**
```
git commit -m "[MAMY-123] feat: 자녀 예방접종 API 엔드포인트 추가"
git commit -m "[MAMY-124] fix: JWT 토큰 만료 처리 로직 수정"
git commit -m "[MAMY-125] refactor: 데이터베이스 쿼리 최적화"
git commit -m "[MAMY-126] docs: API 문서 업데이트"
git commit -m "[MAMY-127] test: 회원가입 유닛 테스트 추가"
```

#### 4. Smart Commit으로 Jira 제어하기

커밋 메시지만으로 Jira 이슈를 업데이트할 수 있습니다.

**댓글 추가:**
```
git commit -m "[MAMY-123] feat: API 구현 완료 #comment 리뷰 요청드립니다"
```

**작업 시간 기록:**
```
git commit -m "[MAMY-124] fix: 버그 수정 #time 2h 30m"
```

**이슈 상태 변경:**
```
git commit -m "[MAMY-125] feat: 기능 완료 #done"
```

**복합 사용:**
```
git commit -m "[MAMY-126] feat: 알림 기능 구현 #time 3h #comment 푸시 알림 추가 완료 #done"
```

#### 5. Pull Request 생성

PR 제목에도 이슈 키를 포함합니다.

**PR 제목 포맷:**
```
[MAMY-123] 자녀 예방접종 API 구현
```

**PR 본문 예시:**
```
## 📝 작업 내용
- 자녀 예방접종 기록 조회 API 구현
- 접종 일정 알림 기능 추가
- PostgreSQL 인덱스 최적화

## 🔗 관련 이슈
- [MAMY-123](https://your-domain.atlassian.net/browse/MAMY-123)

## ✅ 테스트
- [x] 단위 테스트 통과
- [x] 통합 테스트 완료
- [x] API 문서 업데이트

## 📸 스크린샷
(필요 시 추가)
```

---

### ✅ 연동 확인하기

#### Jira 이슈에서 확인할 수 있는 정보:

1. **Development 패널**
   - 연결된 브랜치 목록
   - 커밋 히스토리
   - Pull Request 상태

2. **Activity 탭**
   - Smart Commit으로 추가한 댓글
   - 자동 기록된 작업 시간
   - 상태 변경 이력

#### 체크리스트:
- [ ] Github for Jira 앱 설치 완료
- [ ] Repository 연동 완료
- [ ] 브랜치명에 이슈 키 포함 (예: `feature/MAMY-123-description`)
- [ ] 커밋 메시지에 이슈 키 포함 (예: `[MAMY-123] feat: 기능 추가`)
- [ ] PR 제목에 이슈 키 포함
- [ ] Jira 이슈의 Development 패널에서 정보 확인

---

### 🚨 주의사항

1. **이슈 키 형식**: `MAMY-123` (대문자 프로젝트 코드 + 하이픈 + 숫자)
2. **브랜치명에 반드시 이슈 키 포함**: 없으면 Jira와 연동 안 됨
3. **커밋 후 push 필요**: 커밋만 하고 push 안 하면 Jira에 표시 안 됨
4. **첫 연동 시 시간 소요**: 최초 연동은 몇 분 정도 걸릴 수 있음

---

## 프로젝트 구조

```
backend/
├── .gitignore
├── pyproject.toml          # 의존성 관리
├── uv.lock                 # 의존성 잠금 파일
├── README.md
└── (Django 프로젝트는 나중에 생성)
```

---

## 유용한 uv 명령어

```
# 패키지 추가
uv add package-name

# 개발 의존성 추가
uv add --dev package-name

# 패키지 제거
uv remove package-name

# 의존성 동기화 (uv.lock 기반)
uv sync

# Python 명령 실행
uv run python script.py

# Django 명령 실행 (Django 프로젝트 생성 후)
uv run python manage.py runserver
%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-hf5jt5va)
[16](https://community.latenode.com/t/how-to-link-an-existing-git-branch-to-a-jira-issue/12090)
[17](https://support.atlassian.com/jira-cloud-administration/docs/use-the-github-for-jira-app/)
