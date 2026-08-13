# PJ-CORE Control Dashboard v2 — Sync & Activity Engine

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Назначение

Activity Engine превращает PJ-CORE Control из статичного каталога в живую операционную панель. Он собирает подтверждённые события из внутренних и внешних источников, нормализует их, связывает с проектами, обновляет activity state и формирует timeline/сигналы интерфейса.

Sync Engine отвечает за безопасное чтение canonical/engineering metadata из Wiki/GitHub и обнаружение расхождений без слепого перезаписывания данных.

## 2. Источники активности

Поддерживаемые source keys:
- `control`;
- `founder`;
- `chatgpt`;
- `openclaw`;
- `jessica`;
- `agent`;
- `github`;
- `wiki`;
- `deploy`;
- `telegram`;
- `system`.

## 3. Что считается confirmed activity

Да:
- meaningful discussion/decision;
- code commit/PR/issue change;
- documentation change;
- project status/current-work/next-action update;
- idea/task action;
- deployment/test/release;
- agent starts/completes meaningful project work;
- Founder manually confirms activity.

Нет:
- простое открытие Dashboard;
- background health polling;
- automatic read with no change;
- cache refresh;
- duplicate webhook/event;
- cosmetic UI preference change.

## 4. Ingestion pipeline

```text
raw event
   ↓
auth/source validation
   ↓
project resolution
   ↓
normalization
   ↓
deduplication
   ↓
importance classification
   ↓
persist ActivityEvent
   ↓
recompute project activity
   ↓
update counters/notifications
   ↓
publish SSE event
```

## 5. Project resolution

Порядок:
1. explicit `project_slug`;
2. repository mapping;
3. wiki path mapping;
4. project key/alias mapping;
5. integration-specific mapping table.

Нельзя silently attach ambiguous event. Ambiguous event отправляется в unassigned/system inbox для triage.

## 6. Deduplication

Preferred key:
`source + external_id`.

Fallback normalized hash:
`source + project + event_type + occurred_at_bucket + normalized title/ref`.

Повторная ingestion должна быть idempotent.

## 7. Importance

- `low` — техническое второстепенное событие;
- `normal` — обычная активность;
- `high` — важное изменение статуса/релиз/blocker;
- `critical` — production failure, security issue, explicit Founder decision required.

Importance не равна activity confirmation: low event может быть confirmed activity.

## 8. Activity tier algorithm

Input:
- `last_activity_at`;
- `is_focus`;
- `is_pinned`;
- `activity_policy`;
- manual override if policy=manual.

Default adaptive thresholds:
- focus: 0–3 days;
- active: 4–14;
- cooling: 15–30;
- dormant: 31–90;
- archive_by_activity: >90.

Rules:
- explicit focus always maps to focus visual state;
- persistent project cannot shrink below configured minimum tier;
- pinned affects sort/display but не обязан менять true inactivity metric;
- project closure/archive lifecycle не определяется activity age.

## 9. Recalculation

Выполняется:
- сразу после confirmed event;
- при загрузке board как safety calculation;
- periodic job минимум 2 раза в сутки;
- после timezone/day boundary при необходимости.

## 10. Sync ownership model

### Wiki → Control automatic read

Разрешено читать:
- summary/description;
- maturity/integration;
- confirmed developer/owner;
- lifecycle metadata;
- repo/wiki links;
- canonical references.

Изменения применяются только к Wiki-owned fields.

### Control → Wiki

Только explicit controlled write или отдельный trusted sync workflow.

Control не должен коммитить каждое оперативное изменение в Wiki.

### GitHub → Control

Automatic read/activity ingest:
- repo metadata;
- commits;
- PRs;
- issues;
- releases;
- recent activity.

GitHub activity меняет activity state, но не должна автоматически менять product status без правила.

## 11. Conflict detection

Конфликт возникает, когда:
- field относится к shared/controlled ownership;
- local value changed after last sync;
- source value changed after last sync;
- values differ.

UI показывает:
- field;
- Control value;
- source value;
- source timestamp;
- local timestamp;
- recommended owner.

Resolution must be audited.

## 12. Sync states

- `ok` — синхронизировано;
- `pending` — sync выполняется/ожидает;
- `stale` — давно не обновлялось;
- `conflict` — обнаружено расхождение;
- `error` — техническая ошибка;
- `disabled` — integration выключен.

## 13. Failure behavior

GitHub/Wiki/OpenClaw outage:
- Control продолжает работать на локальной DB;
- карточки показывают last known state;
- sync indicator становится degraded/stale;
- ошибка не превращается автоматически в project blocker;
- critical integration outage может породить global notification.

## 14. Polling/webhooks

Предпочтение:
- webhooks/events там, где удобно и безопасно;
- polling fallback;
- GitHub polling допускается на MVP;
- Wiki sync polling/cron допускается;
- Agent/Knowledge Protocol в будущем — event push.

## 15. UI live delivery

SSE events:
- `project.updated`;
- `activity.created`;
- `project.tier_changed`;
- `inbox.created`;
- `notification.created`;
- `sync.updated`;
- `system.health_changed`.

Frontend при reconnect делает REST refresh/checkpoint, чтобы не зависеть от пропущенных transient events.

## 16. Observability

Metrics/logging:
- ingest count by source;
- duplicate count;
- unresolved project mapping;
- sync latency;
- sync failures;
- conflicts;
- last successful sync per source;
- SSE connected clients;
- activity tier recalculation count.
