# PJ-CORE Control Dashboard v2 — UX/UI Specification

Статус: Approved for implementation
Дата: 2026-08-13

## 1. Цель интерфейса

Интерфейс должен восприниматься как premium command center, а не как административная панель. Он должен быть одновременно красивым, быстрым, информативным и пригодным для ежедневной работы с десятками проектов.

Ключевой принцип: пользователь сначала видит систему целиком, затем раскрывает контекст проекта без потери ориентации, и только после этого при необходимости входит в полноценный Project Workspace.

## 2. Информационная архитектура

### 2.1 Global shell

Постоянные элементы:
- логотип/бренд PJ·CORE CONTROL;
- global search / command palette trigger;
- Founder Inbox counter;
- notifications;
- system health indicator;
- user/founder menu;
- fullscreen toggle.

На desktop не использовать постоянный тяжёлый sidebar. Навигация должна быть контекстной и появляться только когда нужна.

### 2.2 Control Board

Содержит:
- greeting/status sentence;
- operational strip;
- quick filters;
- adaptive project grid;
- optional compact old-project zone.

Operational strip:
- projects total;
- active;
- focus;
- ideas;
- blocked;
- Founder decisions.

Каждый counter является фильтром.

### 2.3 Project card states

#### Compact

Показывает:
- icon;
- title;
- status;
- один progress indicator;
- inactivity age;
- critical signals.

#### Normal

Показывает:
- icon/title/status/priority;
- short summary;
- current work;
- MVP/PROD;
- active developer/agent;
- signal strip.

#### Focus

Дополнительно:
- next action;
- latest important change;
- blocker;
- ML/IL;
- last activity source/time.

#### Expanded Card

Карточка занимает крупную часть grid, не меняя страницы.

Tabs:
- Overview;
- Activity;
- Ideas;
- Tasks;
- Agents;
- Resources.

Состояние tabs сохраняется локально для текущей сессии.

### 2.4 Project Workspace

Полноэкранный рабочий режим с тем же visual shell.

Основные зоны:
- header с identity/status/actions;
- tab navigation;
- content canvas;
- optional right context rail для quick actions/system metadata.

## 3. Детализация разделов Project Workspace

### Overview

Поля:
- summary;
- status;
- maturity level;
- integration level;
- lifecycle state;
- priority;
- focus;
- pinned;
- current work;
- next action;
- stage goal;
- blockers;
- developer;
- owner;
- MVP%;
- PROD%;
- latest important event;
- sync health.

Редактирование — inline или через compact sheet/popover, без тяжёлой admin-form страницы.

### Activity

Хронологический timeline.

Event row содержит:
- time;
- source icon;
- actor;
- action title;
- optional details;
- external link;
- severity/importance;
- provenance.

Фильтры:
- all;
- Founder;
- agents;
- GitHub;
- Wiki;
- deploy;
- system.

### Ideas

Группы:
- New;
- Seen;
- Done;
- Rejected.

Actions:
- mark seen;
- done;
- reject;
- restore;
- edit;
- delete where policy allows;
- convert to task/decision.

### Tasks

Минимальная модель v2:
- title;
- status;
- owner/agent;
- priority;
- due date optional;
- source;
- related idea/activity event;
- next action marker.

### Agents

Карточка агента:
- name;
- role;
- enabled state;
- lead/developer marker;
- last activity;
- current assignment;
- integration/availability;
- quick actions.

### Resources

Группы:
- GitHub;
- Wiki;
- Production;
- Staging;
- Documentation;
- Project tools;
- Telegram;
- External resources.

## 4. Founder Inbox UX

Открывается как right-side drawer, не modal.

Типы элементов:
- note;
- idea;
- question;
- decision_required;
- alert;
- task_candidate.

Actions:
- attach to project;
- convert;
- answer;
- mark resolved;
- dismiss;
- open source.

Unread/critical элементы имеют clear visual hierarchy.

## 5. Command Palette

Shortcut: `Cmd+K` / `Ctrl+K`.

Поддерживает:
- поиск проекта;
- навигацию;
- actions;
- quick create;
- natural-language intent parsing в более поздней фазе.

Примеры действий:
- открыть проект;
- добавить идею;
- сделать focus;
- изменить статус;
- добавить next action;
- открыть GitHub;
- открыть Wiki;
- передать агенту;
- открыть Inbox;
- показать blocked projects.

Перед destructive/critical actions требуется confirmation.

## 6. Visual Design System

### 6.1 Mood

- premium;
- technical;
- calm;
- spatial;
- precise;
- dark graphite;
- restrained futuristic accents.

### 6.2 Base surfaces

- background: near-black graphite, не pure black;
- cards: smoked glass / translucent graphite;
- elevated surfaces: subtle inner highlight + soft shadow;
- borders: 1px low-contrast neutral;
- active surfaces: restrained cool glow.

### 6.3 Color semantics

- blue/cyan: active/system/focus;
- violet: AI/agent-related;
- amber: attention/warning;
- red: blocker/error/destructive;
- green: healthy/production/success;
- neutral grey: dormant/inactive/metadata.

Не использовать случайные project-specific rainbow colors по умолчанию.

### 6.4 Typography

- display/headings: modern grotesk sans;
- body: highly readable sans;
- metadata/technical values: optional mono family;
- uppercase labels только для коротких metadata labels;
- не использовать bold в каждом блоке.

### 6.5 Spacing and shape

- 8px base spacing grid;
- desktop card radius 18–24px;
- controls 10–14px radius;
- generous white space в focus/expanded states;
- compact cards уменьшают padding пропорционально.

## 7. Motion Design

### 7.1 General rules

- Motion информирует о причинно-следственной связи.
- Не анимировать каждый декоративный элемент.
- Target 60fps.
- transform/opacity preferred.
- reduced-motion обязателен.

### 7.2 Card hover

- translateY 2–3px;
- border brightness + small elevation;
- 150–220ms.

### 7.3 Card expand

Фирменная shared-element transition:
- card сохраняет identity;
- icon/title/status физически перемещаются;
- соседние карточки перестраиваются мягко;
- content sections появляются после geometry transition;
- recommended duration 450–600ms;
- spring-like easing без bounce circus effect.

### 7.4 Tier change

При новой activity:
- subtle glow pulse;
- grid reflow;
- card grows/shrinks smoothly;
- badge/activity age refresh;
- изменение не должно дёргать весь экран.

### 7.5 Live event

Новый event:
- card gets a brief soft highlight;
- event row inserts with opacity/translate transition;
- counters animate only changed values.

## 8. Background

Lock/login screen может использовать Aurora/WebGL.

Основной Dashboard:
- calmer background;
- subtle radial illumination;
- lightweight noise texture;
- optional low-opacity entity/dot field;
- no constantly bright Aurora behind work content.

В перспективе dot field может отражать реальные PJ-CORE entities/links, но это не blocker MVP.

## 9. Responsive behavior

### Desktop >= 1280

12-column dense adaptive grid.

### Tablet 768–1279

6–8-column grid, cards укрупняются относительно viewport.

### Mobile < 768

Не shrink desktop.

Используется отдельная композиция:
- vertical project feed;
- focus first;
- operational counters in 2-column arrangement;
- bottom nav: Control / Inbox / Search / System;
- expanded card becomes full-width detail sheet/workspace.

## 10. Accessibility

- keyboard navigation;
- visible focus states;
- semantic landmarks;
- ARIA labels for icon controls;
- WCAG AA contrast target;
- reduced motion;
- no status encoded only by color;
- touch targets >= 44px on mobile.

## 11. UX acceptance criteria

- Founder может найти любой проект за <= 2 interactions.
- Добавление идеи к проекту <= 3 interactions.
- Focus/status/next action меняются без перехода на admin-form page.
- Expanded card сохраняет контекст grid.
- Mobile не требует horizontal scrolling.
- При 30+ проектах главный экран остаётся читаемым.
- При 100 activity events workspace остаётся отзывчивым.
- Ошибки sync видны, но не блокируют просмотр cached/local state.
