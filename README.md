# Backend


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
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)
```powershell
# PowerShell 실행 정책 설정 (최초 1회)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# uv 설치
irm https://astral.sh/uv/install.ps1 | iex
```

#### macOS (Homebrew)
```bash
brew install uv
```

#### 설치 확인
```bash
uv --version
# 예상 출력: uv 0.9.x
```

### 2. PATH 설정 (필요한 경우)

#### Windows PowerShell
```powershell
# 현재 세션에만 적용
$env:Path = "C:\Users\SSAFY\.local\bin;$env:Path"

# 영구 적용 (PowerShell 프로필에 추가)
echo '$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"' >> $PROFILE
```

#### Git Bash (Windows)
```bash
# ~/.bashrc 파일에 추가
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### macOS / Linux
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 프로젝트 클론 및 의존성 설치

```bash
# 레포 클론
git clone https://github.com/mamy-myfamilyandme/backend.git
cd backend

# 의존성 설치 (uv.lock 기반으로 정확히 같은 버전 설치)
uv sync
```

### 4. 설치 확인

```bash
# 설치된 패키지 확인
uv pip list

# Python 버전 확인
uv run python --version
```

**끝!** 이제 바로 개발 시작하시면 됩니다.

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

```bash
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
```