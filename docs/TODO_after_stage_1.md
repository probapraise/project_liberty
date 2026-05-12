# TODO After Stage 1

## Current Scope Constraint

- 감시 대상은 Chrome과 Steam으로 제한한다.
- Chrome: `chrome.exe`만 감시한다.
- Steam: `steam.exe`, `steamwebhelper.exe`만 감시한다.
- 모든 게임은 Steam에 등록해서 실행한다고 가정한다.
- 다른 브라우저, 다른 게임 런처, 개별 게임 exe 목록은 Stage 2 기본 범위에서 제외한다.

## Stage 2

- Chrome/Steam 전용 foreground window watcher 구현
- Chrome 도메인/title 기반 활동 분류
- Steam 실행/활성 창 기반 게임 게이트웨이 분류
- policy engine 구현
- pending intervention event 생성
- Codex intervention prompt 실행
- decision logging 확장

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
