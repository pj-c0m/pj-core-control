# PJ-CORE Control Dashboard v2 — Unified Data Model

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Цель

Сохранить полезную legacy-модель `pj-core` и расширить её данными нового Control, не создавая параллельные сущности с одинаковым смыслом.

## 2. Core entities

### Project

Ключевые поля:

- `id` — internal numeric/UUID id;
- `slug` — стабильный внешний id для URL/API;
- `key` — короткий routing key;
- `alias` — human alias;
- `name`;
- `icon`;
- `summary`;
- `status`;
- `lifecycle_state`;
- `maturity_level`;
- `integration_level`;
- `priority`;
- `is_focus`;
- `is_pinned`;
- `activity_policy` (`adaptive|persistent|manual`);
- `stage_goal`;
- `current_work`;
- `next_action`;
- `blocker`;
- `owner`;
- `developer`;
- `mvp_pct`;
- `prod_pct`;
- `project_root`;
- `repository_url`;
- `wiki_path`;
- `production_url`;
- `staging_url`;
- `last_activity_at`;
- `last_activity_source`;
- `activity_tier`;
- `created_at`;
- `updated_at`.

Constraints:
- `slug`, `key` unique;
- только один `Project.is_focus=true`, если policy v2 остаётся single-focus; если позже разрешён multi-focus — это отдельная schema decision;
- progress 0..100;
- maturity/integration должны валидироваться по утверждённым enum/spec.

### ProjectNote

Сохраняется legacy-сущность.

Поля:
- `id`;
- `project_id`;
- `type` (`idea|thought|question|decision|note`);
- `content`;
- `idea_state` nullable;
- `source`;
- `created_by`;
- `created_at`;
- `updated_at`.

Idea state:
- `new`;
- `seen`;
- `done`;
- `rejected`.

### InboxItem

Поля:
- `id`;
- `type` (`note|idea|question|decision_required|alert|task_candidate`);
- `content`;
- `state` (`new|triaged|attached|resolved|dismissed`);
- `project_id` nullable;
- `source`;
- `actor`;
- `source_ref`;
- `severity`;
- `created_at`;
- `resolved_at`.

### Task

Новая сущность.

Поля:
- `id`;
- `project_id`;
- `title`;
- `description`;
- `status` (`open|in_progress|blocked|done|cancelled`);
- `priority`;
- `owner_type` (`founder|agent|human|system`);
- `owner_ref`;
- `due_at` nullable;
- `source_type`;
- `source_ref` nullable;
- `is_next_action`;
- `created_at`;
- `updated_at`;
- `completed_at` nullable.

### ActivityEvent

Центральная новая сущность.

Поля:
- `id`;
- `project_id` nullable для global events;
- `event_type`;
- `source`;
- `actor_type`;
- `actor_ref`;
- `title`;
- `details` nullable;
- `importance` (`low|normal|high|critical`);
- `external_url` nullable;
- `external_id` nullable;
- `dedupe_key` nullable unique per source;
- `metadata_json`;
- `confirmed_activity` boolean;
- `occurred_at`;
- `ingested_at`.

`confirmed_activity=false` используется для событий, которые не должны поднимать карточку, например автоматическое чтение Dashboard.

### ProjectTool

Legacy + расширение:
- `id`;
- `project_id`;
- `name`;
- `kind`;
- `url`;
- `icon` nullable;
- `sort_order`;
- `created_at`.

### GlobalTool

То же без `project_id`.

### AgentType

Legacy entity:
- `id`;
- `key`;
- `name`;
- `description`.

### AgentBinding

Расширение legacy:
- `id`;
- `project_id`;
- `agent_type_id`;
- `agent_ref` nullable;
- `label`;
- `role`;
- `enabled`;
- `is_developer`;
- `is_lead`;
- `current_assignment` nullable;
- `last_activity_at` nullable;
- `config_json` nullable.

### TelegramTarget

Legacy entity сохраняется:
- `id`;
- `project_id`;
- `name`;
- `chat_id`;
- `token_ref`;
- `created_at`.

Секретный token в БД не хранить.

### ResourceLink

Новая унифицированная сущность для project resources:
- `id`;
- `project_id`;
- `kind` (`github|wiki|production|staging|docs|telegram|external`);
- `label`;
- `url`;
- `source`;
- `is_primary`;
- `health_state` nullable;
- `last_checked_at` nullable.

### SyncState

Поля:
- `id`;
- `project_id`;
- `source`;
- `status` (`ok|pending|stale|conflict|error|disabled`);
- `last_success_at`;
- `last_attempt_at`;
- `last_error` nullable;
- `source_revision` nullable;
- `local_revision` nullable;
- `conflict_json` nullable.

### Notification

Поля:
- `id`;
- `project_id` nullable;
- `type`;
- `severity`;
- `title`;
- `body`;
- `source_event_id` nullable;
- `requires_action`;
- `read_at` nullable;
- `resolved_at` nullable;
- `created_at`.

## 3. Provenance

Поля, приходящие из внешних canonical sources, должны иметь происхождение.

Рекомендуемая таблица `FieldProvenance`:
- `project_id`;
- `field_name`;
- `source`;
- `source_ref`;
- `source_updated_at`;
- `synced_at`;
- `value_hash`.

Это позволяет показать в UI, откуда взялось значение и почему возник конфликт.

## 4. Computed fields

Не хранить как независимую истину без необходимости:
- `inactive_days` — вычисляется;
- counters ideas/blockers — query/cache;
- `activity_tier` можно кэшировать, но пересчитывать из `last_activity_at` + policy;
- overall readiness не вводить без утверждённой формулы.

## 5. Relationships

```text
Project
  1 ─ N ProjectNote
  1 ─ N InboxItem
  1 ─ N Task
  1 ─ N ActivityEvent
  1 ─ N ProjectTool
  1 ─ N AgentBinding
  1 ─ N TelegramTarget
  1 ─ N ResourceLink
  1 ─ N SyncState
  1 ─ N Notification
```

## 6. Migration mapping from legacy

- `Project.progress_pct` не теряется; временно map в `mvp_pct` только если нет отдельного подтверждённого значения, с migration marker `derived_from_legacy_progress=true`.
- legacy `status` переносится напрямую через mapping table.
- `stage_goal`, `next_action`, `priority`, `is_focus`, `project_root` переносятся напрямую.
- `ProjectNote` переносится полностью.
- idea state переносится без изменения.
- `InboxItem` переносится полностью с mapping legacy states.
- tools, agent bindings, Telegram targets переносятся полностью.

## 7. Audit requirements

Изменения управляющих полей должны создавать audit/activity event:
- status;
- focus;
- priority;
- developer;
- lifecycle;
- blocker;
- next action;
- progress;
- idea state;
- sync conflict resolution.
