# PJ-CORE Control Dashboard v2 — System Architecture

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Архитектурная цель

Объединить premium frontend нового PJ-CORE Control с проверенной предметной и серверной логикой legacy `pj-core`, не сохраняя две конкурирующие системы данных.

Новый `pj-core-control` становится единственным runtime-продуктом. Legacy `pj-core` используется как источник кода и данных для миграции, после cutover переводится в read-only/archive.

## 2. High-level architecture

```text
                    PJ-CORE Wiki
                         │
                 Wiki Sync Adapter
                         │
GitHub ── GitHub Adapter │     OpenClaw/Jessica/Agents
   │                     │                │
   └──────────────┐      │       Agent/Event Adapter
                  ▼      ▼                ▼
              ┌──────────────────────────────┐
              │      Control Backend         │
              │ FastAPI + service layer      │
              ├──────────────────────────────┤
              │ Projects / Ideas / Inbox     │
              │ Activity / Agents / Sync     │
              │ Commands / Resources         │
              └──────────────┬───────────────┘
                             │
                    SQLAlchemy + Alembic
                             │
                        Control DB
                             │
               ┌─────────────┴─────────────┐
               │                           │
         REST/JSON API               Event stream
               │                           │
               └─────────────┬─────────────┘
                             ▼
                   Premium Frontend
                             ▲
                             │
                      Telegram Bot
                       via API only
```

## 3. Технологический baseline

### Backend

- Python 3.12+;
- FastAPI;
- SQLAlchemy 2.x;
- Alembic;
- Pydantic v2;
- HTTPX для внешних adapters;
- structured logging;
- background jobs через встроенный scheduler/worker abstraction на первой фазе.

### Database

MVP допускает SQLite для простого одиночного deployment, но схема и миграции должны быть PostgreSQL-compatible.

Production preference:
- PostgreSQL, если появляется несколько writer-процессов/инстансов;
- SQLite WAL допустим для single-node private deployment.

DB backend выбирается через `DATABASE_URL` без изменения бизнес-логики.

### Frontend

Рекомендуемый вариант: TypeScript + Vite + React или Preact, если реализация complex shared transitions, command palette, drawer state и realtime становится слишком тяжёлой для vanilla JS.

Критерий выбора framework: maintainability и motion/state complexity, а не мода.

Если команда оставляет vanilla/HTMX, обязателен component/module split. Монолитный `index.html` больше не является допустимой архитектурой.

### Motion

- CSS View Transitions API там, где поддерживается;
- Motion/Framer Motion только если выбран React и библиотека реально упрощает shared layout transitions;
- fallback transitions без потери функциональности.

## 4. Backend modules

```text
backend/
  app/
    main.py
    config.py
    db/
      base.py
      session.py
      migrations/
    domain/
      projects/
      ideas/
      inbox/
      tasks/
      agents/
      activity/
      resources/
      sync/
      notifications/
    api/
      v1/
    services/
    integrations/
      wiki/
      github/
      openclaw/
      telegram/
    workers/
    security/
    observability/
```

Правило: API routes не содержат сложную бизнес-логику. Они валидируют запрос, вызывают service/use-case и формируют response.

## 5. Frontend modules

```text
frontend/
  src/
    app/
    api/
    components/
      shell/
      cards/
      drawers/
      command-palette/
      timeline/
      signals/
    features/
      projects/
      inbox/
      ideas/
      agents/
      activity/
      system/
    pages/
      control-board/
      project-workspace/
    motion/
    styles/
      tokens/
      base/
      components/
    state/
    utils/
```

## 6. Domain/service boundaries

### ProjectService

Отвечает за:
- CRUD project operational state;
- focus uniqueness;
- priority;
- pin/activity policy;
- progress;
- current/next/blocker;
- computed project summary.

### IdeaService

- add;
- state transitions;
- count new;
- convert to task;
- audit event.

### InboxService

- ingest;
- assign;
- convert;
- resolve/dismiss;
- unread counters.

### ActivityService

- normalize incoming external/internal events;
- deduplicate;
- persist;
- recompute last confirmed activity;
- activity tier calculation;
- importance scoring.

### SyncService

- source ownership rules;
- pull/compare/apply;
- conflict detection;
- sync health;
- provenance.

### AgentService

- agent bindings;
- developer marker;
- last activity;
- action requests;
- future Knowledge Protocol integration.

## 7. Read/write ownership rules

Нельзя строить unrestricted two-way sync.

### Wiki-owned fields

По умолчанию:
- canonical description;
- product goal;
- architecture references;
- maturity/integration levels;
- confirmed developer/owner;
- canonical repo/wiki links;
- roadmap references.

### Control-owned fields

- focus;
- UI pin;
- current work;
- next action;
- operational blockers;
- progress indicators;
- idea states;
- inbox state;
- unread state;
- activity tier;
- runtime health.

### Shared/controlled-write fields

Для некоторых полей допускается изменение в Control с последующей подтверждённой записью в Wiki через explicit sync action/service, например developer или lifecycle status. Нельзя молча перезаписывать canonical wiki при каждом UI edit.

## 8. Event architecture

Каждое значимое действие создаёт `ActivityEvent`.

Пример internal event types:
- `project.created`;
- `project.updated`;
- `project.focused`;
- `idea.created`;
- `idea.state_changed`;
- `inbox.received`;
- `inbox.attached`;
- `agent.activity`;
- `github.commit`;
- `github.pull_request`;
- `wiki.changed`;
- `deploy.succeeded`;
- `deploy.failed`;
- `sync.conflict`;
- `founder.decision_required`.

UI читает события через REST pagination и в перспективе через SSE/WebSocket stream.

Для v2 рекомендуется SSE для server-to-client обновлений: проще, чем full WebSocket, и достаточно для live Dashboard. WebSocket вводить только если потребуется двусторонняя realtime-сессия.

## 9. Cache/snapshot

`data/projects.json` больше не primary storage.

Можно сохранить export endpoint/job:
- `/api/v1/export/projects.json`;
- аварийный static snapshot;
- backup/debug artifact.

Frontend не должен редактировать JSON-файл напрямую.

## 10. Integration adapters

Каждый внешний источник реализуется через adapter interface:

```text
IntegrationAdapter
  health()
  pull_events(since)
  fetch_project_metadata(project)
  normalize_event(raw)
```

Ошибки одного adapter не должны ломать основной Control.

## 11. Deployment topology

Минимум:

```text
reverse proxy
   │
   ├── /          frontend static
   └── /api       FastAPI
                  │
              Control DB
```

Telegram bot и background sync могут работать отдельными процессами в том же Docker Compose.

```text
services:
  web
  api
  worker
  telegram-bot
  db(optional postgres)
```

Для single-node SQLite возможно объединить api+worker при сохранении логических границ.

## 12. Non-functional requirements

- первый meaningful paint desktop: target < 2.5s в локальной/private network;
- API list projects p95 target < 300ms на 100 проектов;
- UI должен выдерживать 100 проектов и тысячи activity events с pagination/virtualization;
- никакой external CDN dependency для критических runtime-assets;
- graceful degradation при недоступном GitHub/Wiki/OpenClaw;
- backups before migration;
- idempotent sync;
- auditability всех автоматических изменений.
