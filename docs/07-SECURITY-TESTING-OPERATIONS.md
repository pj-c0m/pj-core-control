# PJ-CORE Control Dashboard v2 — Security, Testing & Operations

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Security goals

Control управляет проектами, агентами, интеграциями и operational metadata. Ошибка прав или secret handling может дать непропорционально высокий ущерб, поэтому security должна быть частью архитектуры, а не post-MVP дополнением.

## 2. Authentication

Для private deployment допускается один Founder account на первой фазе, но auth boundary должен быть реальным.

Рекомендуемые варианты:
- reverse-proxy SSO/OIDC;
- secure session auth;
- отдельные scoped integration tokens.

Нельзя полагаться на pattern-lock как на единственный security boundary. Pattern/Aurora lock может остаться декоративным/локальным UX-слоем поверх реальной authentication.

## 3. Authorization

Минимальные roles/capabilities:
- Founder: полный доступ;
- trusted service/integration: только scoped API;
- read-only viewer: optional future;
- agent: только разрешённые project/action scopes.

Sensitive actions:
- delete project;
- change canonical/shared fields;
- resolve sync conflicts;
- manage integrations;
- trigger agent action;
- change deployment/resource settings.

## 4. Secrets

Запрещено хранить в репозитории/DB plaintext secrets:
- Telegram bot token;
- GitHub token;
- OpenClaw credentials;
- API keys;
- passwords.

DB хранит только `secret_ref`/`token_ref`.

Runtime получает secrets из environment/secret manager.

Logs должны redaction sensitive headers/query/body fields.

## 5. Input security

- strict Pydantic validation;
- URL allow/validation where relevant;
- sanitize/escape user-generated content;
- Markdown render через safe mode;
- CSRF protection для cookie-auth write requests;
- rate limit integration ingest/auth endpoints;
- request size limits;
- no shell interpolation from project fields.

## 6. Integration security

Каждый integration credential имеет:
- source identity;
- scopes;
- rotation path;
- revoke path;
- last-used/health metadata where possible.

Webhook/event ingest проверяет signature/token.

## 7. Audit

Audit/activity trail обязателен для:
- project status;
- focus;
- priority;
- developer/owner controlled changes;
- progress;
- blockers;
- idea transitions;
- agent actions;
- sync conflict resolution;
- integration config changes;
- destructive actions.

## 8. Backup policy

Перед migration/cutover:
- full DB backup;
- integrity verification;
- `.env`/secret references backup в безопасном месте;
- current commit hashes;
- restore drill.

После launch:
- automated daily DB backup;
- configurable retention;
- off-host copy recommended;
- documented restore command;
- backup health surfaced in System Status later.

## 9. Testing pyramid

### Unit

Обязательно:
- activity tier calculation;
- focus/pin policy;
- idea transitions;
- project mapping;
- dedupe;
- sync conflict detection;
- field ownership rules;
- migration mapping;
- command validation.

### Integration

- API + DB;
- migration upgrade/downgrade where supported;
- Wiki adapter fixtures;
- GitHub adapter fixtures;
- Telegram bot → API;
- SSE reconnect;
- auth/scopes.

### UI component

- project card states;
- signal badges;
- Founder Inbox;
- command palette;
- tab/workspace rendering;
- error/degraded states.

### End-to-end

Критические flows:
1. login → board;
2. search project;
3. expand card;
4. edit next action;
5. add idea;
6. mark idea seen/done;
7. receive Telegram idea;
8. attach inbox item;
9. GitHub event changes activity;
10. tier transition updates UI;
11. open workspace;
12. sync conflict displayed/resolved;
13. degraded GitHub does not break board;
14. mobile core flows.

## 10. Visual regression

Для premium UI обязательны screenshot/visual regression tests минимум для:
- desktop 1440;
- wide 1920;
- tablet;
- mobile;
- compact/normal/focus/expanded cards;
- dark surfaces;
- hover/focus states where testable.

## 11. Motion QA

Проверить:
- no layout jumps;
- shared element identity preserved;
- no content flicker;
- 60fps target on modern desktop;
- mobile acceptable performance;
- reduced-motion disables nonessential transitions;
- dynamic grid does not reorder unexpectedly while user interacts.

## 12. Performance testing

Dataset fixtures:
- 25 projects;
- 100 projects;
- 1000+ ideas;
- 10k activity events.

Проверить:
- initial board render;
- filter/search;
- expanded card;
- timeline pagination;
- SSE burst;
- sync job isolation.

## 13. Observability

Structured logs:
- request_id;
- source;
- project_slug where safe;
- operation;
- duration;
- result.

Health endpoints:
- liveness;
- readiness;
- dependency health summary.

No secrets/user content dump in normal logs.

## 14. Operations

Docker Compose baseline:
- frontend/web;
- api;
- worker;
- telegram-bot;
- postgres optional.

Required operational commands:
- migrate DB;
- backup;
- restore;
- import legacy dry-run/apply;
- sync source;
- rebuild/export snapshot;
- health check.

## 15. Release gates

Нельзя cutover legacy, если:
- migration counts расходятся без объяснения;
- idea states потеряны;
- bot ещё пишет в legacy DB;
- destructive actions не защищены;
- backup restore не проверен;
- critical E2E flows fail;
- system не имеет rollback path.

## 16. Production acceptance

После deployment проверить:
- auth;
- API health;
- DB health;
- project count;
- idea count/state samples;
- inbox;
- bot intake;
- Wiki sync;
- GitHub sync;
- SSE/live update;
- mobile rendering;
- backup job;
- no secrets in logs/frontend bundle.
