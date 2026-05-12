# TODO After Stage 1

## Current Scope Constraint

- 감시 대상은 Chrome과 Steam으로 제한한다.
- Chrome: `chrome.exe`만 감시한다.
- Steam: `steam.exe`, `steamwebhelper.exe`만 감시한다.
- 모든 게임은 Steam에 등록해서 실행한다고 가정한다.
- 다른 브라우저, 다른 게임 런처, 개별 게임 exe 목록은 Stage 2 기본 범위에서 제외한다.

## Stage 2

완료:
- Chrome/Steam 전용 foreground window watcher 구현
- Chrome 제목/도메인 힌트 기반 활동 분류 골격
- Steam 실행/활성 창/Steam 하위 프로세스 기반 게임 게이트웨이 분류
- 기본 policy engine 구현
- pending intervention event 생성
- decision logging 기본 CLI 유지

남음:
- Codex intervention prompt 실행
- intervention dispatcher가 pending event를 Codex 창으로 전달
- 반복 개입 UX 다듬기

## Stage 3

- recovery mode 실제 계획 축소
- exception workflow
- daily summary
- weekly pattern analysis using `codex exec`

## Stage 4

- Chrome extension
- Native Messaging host
- Chrome domain-only reporting
- redirect/friction page
- ICS export 또는 calendar API sync

## Stage 5

- lifeops-mcp 서버
- Codex tool interface
- rule proposal approval workflow 고도화
