create type activity_status as enum ('active', 'closed', 'planned', 'cancelled');
create type asset_type as enum ('preset', 'custom');
create type committee_role as enum ('chair', 'delegate', 'observer');
create type conference_role as enum (
	'owner',
	'secretary_general',
	'director',
	'moderator',
	'rapporteur',
	'crisis_staff',
	'press',
	'logistics',
	'staff'
);

-------------------------------
-- Conferences and committees
-------------------------------

create table conferences (
	id bigint primary key generated always as identity,
	name varchar(255) not null,
	status activity_status not null default 'planned',
	owner_id uuid null references auth.users(id) on delete set null,
	location varchar(255),
	logo_url varchar(1000),
	theme_color varchar(7),
	start_date timestamptz,
	end_date timestamptz,
	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now(),

	constraint conferences_theme_color_hex check (
		theme_color is null or theme_color ~ '^#[0-9A-Fa-f]{6}$'
	),
	constraint conferences_date_range check (
		start_date is null or end_date is null or start_date <= end_date
	)
);

create table committees (
	id bigint primary key generated always as identity,
	conference_id bigint not null references conferences(id) on delete cascade,
	name varchar(64) not null,
	status activity_status not null default 'planned',
	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now(),

	-- Enables conference_assignments to verify committee_id belongs to the same conference_id.
	constraint committees_id_conference_unique unique (id, conference_id)
);

-------------------------------
-- Representations and layouts
-------------------------------

-- Preset/custom separation is represented here, but detailed policy can stay in app logic for now.
create table representations (
	id bigint primary key generated always as identity,
	name varchar(64) not null,
	rep_type asset_type not null default 'preset',
	code varchar(10),
	identifier varchar(255) not null,
	conference_id bigint null references conferences(id) on delete cascade,
	created_at timestamptz not null default now()
);

create table layouts (
	id bigint primary key generated always as identity,
	name varchar(64) not null,
	conference_id bigint null references conferences(id) on delete cascade,
	committee_id bigint null references committees(id) on delete cascade,
	created_at timestamptz not null default now()
);

create table layout_seats (
	layout_id bigint not null references layouts(id) on delete cascade,
	representation_id bigint not null references representations(id) on delete cascade,
	seat_label varchar(10),

	primary key (layout_id, representation_id)
);

-- Real committee seats. These are copied from a layout when a committee is configured.
create table committee_seats (
	committee_id bigint not null references committees(id) on delete cascade,
	representation_id bigint not null references representations(id) on delete cascade,
	seat_label varchar(10),

	primary key (committee_id, representation_id)
);

-------------------------------
-- Assignments
-------------------------------

create table conference_assignments (
	id bigint primary key generated always as identity,
	conference_id bigint not null references conferences(id) on delete cascade,
	user_id uuid not null references auth.users(id) on delete cascade,
	role conference_role not null,
	committee_id bigint null,
	created_at timestamptz not null default now(),

	-- A committee-scoped conference role must point to a committee in that same conference.
	constraint conference_assignments_committee_in_conference foreign key (
		committee_id,
		conference_id
	) references committees(id, conference_id) on delete cascade
);

-- Split uniqueness because NULL committee_id values are not equal in a regular unique constraint.
create unique index conference_assignments_unique_conference_role
	on conference_assignments (conference_id, user_id, role)
	where committee_id is null;

-- Committee-scoped roles dedupe separately from conference-wide roles.
create unique index conference_assignments_unique_committee_role
	on conference_assignments (conference_id, user_id, role, committee_id)
	where committee_id is not null;

create table committee_assignments (
	user_id uuid not null references auth.users(id) on delete cascade,
	committee_id bigint not null references committees(id) on delete cascade,
	role committee_role not null,
	representation_id bigint null references representations(id),

	primary key (user_id, committee_id),
	constraint committee_assignments_delegate_has_representation check (
		role <> 'delegate' or representation_id is not null
	)
);

create unique index committee_assignments_unique_representation
	on committee_assignments (committee_id, representation_id)
	where representation_id is not null;

-------------------------------
-- Sessions
-------------------------------

create table sessions (
	id bigint primary key generated always as identity,
	committee_id bigint not null references committees(id) on delete cascade,
	name varchar(64),
	status activity_status not null default 'planned',
	started_at timestamptz,
	ended_at timestamptz,
	state_snapshot jsonb
);
