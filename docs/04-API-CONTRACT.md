# PJ-CORE Control Dashboard v2 — API Contract

Статус: Approved for implementation
Дата: 2026-08-13
Base path: `/api/v1`

## 1. Принципы

- JSON API;
- stable resource ids/slugs;
- optimistic UI допустим только для reversible low-risk actions;
- destructive actions требуют explicit confirmation на UI;
- все write endpoints возвращают обновлённое представление сущности;
- внешние integrations не пишут напрямую в БД;
- mutation создаёт ActivityEvent там, где это значимое действие;
- pagination обязательна для activity/inbox/notifications.

## 2. Projects

### GET `/projects`

Query:
- `status`;
- `priority`;
- `activity_tier`;
- `focus`;
- `pinned`;
- `has_new_ideas`;
- `blocked`;
- `search`;
- `limit`/`cursor`.

Response project card view включает:
- identity;
- status/priority;
- current work/next action;
- progress;
- activity;
- developer;
- counters/signals;
- sync summary.

### POST `/projects`

Создание проекта.

### GET `/projects/{slug}`

Полное operational представление.

### PATCH `/projects/{slug}`

Разрешённые operational fields:
- status;
- priority;
- stage_goal;
- current_work;
- next_action;
- blocker;
- mvp_pct;
- prod_pct;
- pin/activity policy;
- developer, если policy позволяет controlled-write.

### POST `/projects/{slug}/focus`

Установить focus.

### DELETE `/projects/{slug}`

Не использовать как обычную archive operation. Реальное удаление требует повышенного confirmation; предпочтительнее lifecycle/archive state.

## 3. Ideas / Notes

### GET `/projects/{slug}/ideas`

Filters: `state`, `limit`, `cursor`.

### POST `/projects/{slug}/ideas`

```json
{
  "content": "...",
  "source": "ui"
}
```

### PATCH `/projects/{slug}/ideas/{id}`

Изменение content/state.

### POST `/projects/{slug}/ideas/{id}/transition`

```json
{"state":"seen|done|rejected|new"}
```

### POST `/projects/{slug}/ideas/{id}/convert-to-task`

Создаёт связанную Task.

## 4. Inbox

### GET `/inbox`

Filters:
- state;
- type;
- severity;
- project;
- requires_action.

### POST `/inbox`

Universal intake endpoint для UI/bot/integrations.

### POST `/inbox/{id}/attach`

```json
{"project_slug":"...","convert_to":"note|idea|task|decision|null"}
```

### POST `/inbox/{id}/resolve`
### POST `/inbox/{id}/dismiss`

## 5. Tasks

### GET `/projects/{slug}/tasks`
### POST `/projects/{slug}/tasks`
### PATCH `/projects/{slug}/tasks/{id}`
### POST `/projects/{slug}/tasks/{id}/complete`

## 6. Activity

### GET `/activity`
Global stream.

### GET `/projects/{slug}/activity`
Project timeline.

Query:
- `source`;
- `importance`;
- `event_type`;
- `cursor`;
- `limit`.

### POST `/events/ingest`

Authenticated integration endpoint.

Payload:
```json
{
  "project_slug": "meeting-room",
  "event_type": "agent.activity",
  "source": "openclaw",
  "actor_ref": "jessica",
  "title": "Обновлён Telegram transport backlog",
  "occurred_at": "2026-08-13T10:00:00Z",
  "external_id": "optional",
  "confirmed_activity": true,
  "metadata": {}
}
```

Endpoint должен быть idempotent через `external_id`/`dedupe_key`.

### GET `/events/stream`

SSE stream для live updates.

Event envelope:
```json
{
  "type": "project.updated",
  "project_slug": "...",
  "payload": {},
  "timestamp": "..."
}
```

## 7. Agents

### GET `/projects/{slug}/agents`
### POST `/projects/{slug}/agents`
### PATCH `/projects/{slug}/agents/{id}`
### DELETE `/projects/{slug}/agents/{id}`

### POST `/projects/{slug}/agents/{id}/actions`

```json
{
  "action":"review|research|implement|sync|custom",
  "instruction":"optional text"
}
```

v2 backend может сначала создавать queued action/activity без реального cross-agent transport, но API contract должен быть готов к Knowledge Protocol.

## 8. Resources / Tools

### GET `/projects/{slug}/resources`
### POST `/projects/{slug}/resources`
### PATCH `/projects/{slug}/resources/{id}`
### DELETE `/projects/{slug}/resources/{id}`

### GET `/tools`
### POST `/tools`

## 9. Sync

### GET `/projects/{slug}/sync`

Возвращает состояния Wiki/GitHub/OpenClaw/etc.

### POST `/projects/{slug}/sync/{source}`

Запускает sync pull/compare.

### GET `/projects/{slug}/sync/{source}/conflicts`

### POST `/projects/{slug}/sync/{source}/conflicts/{id}/resolve`

Resolution:
```json
{"strategy":"keep_control|accept_source|manual","value":null}
```

## 10. System

### GET `/system/health`

Components:
- api;
- db;
- wiki;
- github;
- openclaw;
- telegram;
- worker.

Каждый component:
- `state: healthy|degraded|down|disabled`;
- last success;
- latency optional;
- safe error summary.

### GET `/system/stats`

Operational strip counters.

## 11. Notifications

### GET `/notifications`
### POST `/notifications/{id}/read`
### POST `/notifications/{id}/resolve`

## 12. Command Palette

### POST `/commands/preview`

Для structured actions/natural language parsing.

Request:
```json
{"input":"добавь идею в meeting room — voice notifications"}
```

Response только preview:
```json
{
  "intent":"create_idea",
  "project_slug":"meeting-room",
  "arguments":{"content":"voice notifications"},
  "requires_confirmation":false
}
```

### POST `/commands/execute`

Выполняет только ранее валидированную команду/structured request.

Natural-language parser не является обязательным для первого cutover; searchable action palette обязательна.

## 13. Error format

```json
{
  "error": {
    "code": "SYNC_CONFLICT",
    "message": "Краткое безопасное описание",
    "details": {},
    "request_id": "..."
  }
}
```

## 14. Auth

API write endpoints защищены authenticated session/token.
Integration ingest использует отдельные scoped credentials.
Никакие GitHub/Telegram/OpenClaw secrets не возвращаются frontend.
