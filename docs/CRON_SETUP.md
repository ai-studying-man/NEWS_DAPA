# 방산출근길 예약 실행 구성

## 실행 시간

목표 실행 시간은 매일 06:30 KST입니다.

- 한국 시간대 cron: `30 6 * * *`
- UTC 기준 cron: `30 21 * * *`
- 발송 기준은 06:30 KST로 고정하며, GitHub Actions에서는 UTC 기준 `30 21 * * *`를 사용합니다.

## 필수 환경변수

```text
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TZ=Asia/Seoul
```

`TELEGRAM_CHAT_ID`는 쉼표로 구분해 여러 수신 대상을 지정할 수 있습니다.

```text
TELEGRAM_CHAT_ID=6015255978,-1004402722342
```

BotFather에서 Telegram bot token을 만들고, 봇을 채널 또는 단체방에 추가한 뒤
`TELEGRAM_CHAT_ID`를 설정합니다.

## 로컬 검증

```powershell
$env:PYTHONPATH = "src"
python -m dapa_morning_brief.cli --dry-run
```

실제 Telegram 발송 전에는 반드시 `--dry-run`으로 메시지 형태를 확인합니다.

## Windows 작업 스케줄러

작업 만들기에서 다음 값을 사용합니다.

- 트리거: 매일 06:30
- 프로그램: `powershell.exe`
- 인수:

```text
-NoProfile -ExecutionPolicy Bypass -File C:\Users\dusgh\Desktop\DAPA_NEWS\scripts\run_morning_brief.ps1
```

환경변수는 사용자 환경변수 또는 작업 스케줄러의 실행 계정에 설정합니다.

## Linux cron

`crontab -e`에 아래 줄을 추가합니다.

```cron
30 6 * * * cd /path/to/DAPA_NEWS && . .venv/bin/activate && python -m dapa_morning_brief.cli >> logs/dapa_morning_brief.log 2>&1
```

`uv`를 사용하는 서버라면 다음 형태도 가능합니다.

```cron
30 6 * * * cd /path/to/DAPA_NEWS && uv run dapa-morning-brief >> logs/dapa_morning_brief.log 2>&1
```

## GitHub Actions

GitHub Actions cron은 UTC 기준입니다. 06:30 KST 실행은
`.github/workflows/dapa-morning-brief.yml`의 `30 21 * * *` 설정을 사용합니다.

Repository Secrets에 다음 값을 등록합니다.

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

## Hermes Cronjob

Hermes Cronjob에는 다음 형태로 등록합니다.

```text
이름: 방산출근길 뉴스레터
스케줄: 매일 06:30 Asia/Seoul
명령: uv run dapa-morning-brief --days 3 --fallback-days 5
전달: Telegram Bot API
환경변수: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TZ=Asia/Seoul
```

## 수집 우선순위

1. 정책브리핑 방위사업청 RSS
2. 정책브리핑 국방부 RSS
3. 정책브리핑 보도자료 RSS
4. 국방일보 방위사업 RSS
5. Google News RSS 섹션별 검색
6. 넓은 OR 검색과 단일 키워드 폴백

기사 부족 시 억지로 내용을 만들지 않고 `수집 기사 없음`을 표시합니다.
