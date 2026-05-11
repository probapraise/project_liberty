# LifeOps Codex Operator

LifeOps Codex Operator는 Codex CLI/Codex app을 생활 운영 보조자로 사용하는 로컬 시스템이다. 별도 챗봇 GUI나 OpenAI API 직접 호출 없이, 로컬 DB와 스크립트가 Codex에게 필요한 상태만 전달한다.

## Stage 1 범위

- 저장소 기본 구조
- Codex Operator용 `AGENTS.md`
- 기본 생활 규칙/스케줄/개입/프라이버시 설정
- SQLite DB 스키마 초기화
- 부팅 브리핑 컨텍스트 생성
- Windows 로그온 자동 시작 작업 설치/삭제 스크립트
- Codex CLI 실행 스크립트
- Stage 2용 watcher/dispatcher 자리표시자

브라우저 확장, 실제 브라우저 도메인 감지, 캘린더 API 연동은 Stage 1 이후 TODO로 남겨져 있다.

## 수동 1회 시작

PowerShell에서 저장소 루트로 이동한 뒤 실행한다.

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\Start-LifeOps.ps1
```

## 자동 시작 설치

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\Install-StartupTask.ps1
```

설치 후 Windows 로그인 시 `scripts/Start-LifeOps.ps1`이 실행된다.

## 자동 시작 제거

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\Remove-StartupTask.ps1
```

## 주요 CLI

```powershell
$env:PYTHONPATH = ".\src"
python -m lifeops.cli init-db
python -m lifeops.cli export-boot-briefing-context
python -m lifeops.cli write-boot-prompt
python -m lifeops.cli get-today-plan
python -m lifeops.cli get-current-block
```

## Python 경로

Stage 1 런처는 `.venv`가 없으면 Python 3.12+로 가상환경을 만든다. `python`, `python3`, `py` 순서로 찾고, 특수한 설치 경로를 쓰는 경우 아래처럼 지정할 수 있다.

```powershell
$env:LIFEOPS_PYTHON = "C:\Path\To\python.exe"
pwsh -ExecutionPolicy Bypass -File .\scripts\Start-LifeOps.ps1
```
