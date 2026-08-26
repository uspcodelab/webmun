------------------------------------------------------
-- ENUMS AND TYPES
------------------------------------------------------
create type activity_status as enum ('active', 'closed', 'planned', 'cancelled');
create type asset_type as enum ('preset', 'custom');
create type conference_role as enum (
	'admin',        -- Secretary general / Organizer
	'chair',        -- Director / Moderator
	'press',        -- Press / Media team
	'staff',        -- General logistics / Crisis backroom
	'participant'  -- Delegate / Delegation
);

------------------------------------------------------
-- CORE CONFERENCE HIERARCHY
------------------------------------------------------
create table conferences (
	id bigint primary key generated always as identity, 
	name varchar(255) not null,
	slug varchar(100), 
	status activity_status not null default 'planned',
	owner_id uuid not null references auth.users on delete cascade,
	
	location varchar(255),
	logo varchar(1000),
	color varchar(7) not null default '#0f172a',
	start_date timestamptz not null,
	end_date timestamptz not null,

	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now()
);

create table committees (
	id bigint primary key generated always as identity,
	conference_id bigint not null references conferences(id) on delete cascade,

	name varchar(128) not null, -- full name
	code varchar(64) not null, -- code name
	logo varchar(1000),
	topic TEXT,
	status activity_status not null default 'planned',

	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now()
);

create table sessions (
	id bigint primary key generated always as identity,
	committee_id bigint not null references committees(id) on delete cascade,
	name varchar(64),
	status activity_status not null default 'planned',
	started_at timestamptz,
	ended_at timestamptz,
	state_snapshot JSONB
);

------------------------------------------------------
-- REPRESENTATIONS & LAYOUTS
------------------------------------------------------

-- This table references preset/custom representations that we might work with. We can perhaps separate the two of them later
create table representations (
	id bigint primary key generated always as identity,
	name varchar(64), 
	rep_type asset_type not null default 'preset',
	code varchar(10),
	identifier varchar(255) not null, -- this can be either an url if the rep_type is custom, or a code (like 'br')
	conference_id bigint null references conferences(id) on delete cascade
);

-- preset layouts for conferences
create table layouts (
	id bigint primary key generated always as identity,
	name varchar(64),
	conference_id bigint null references conferences(id) on delete cascade,
	-- if conference_id is null, its a preset. else, its an overall layout for a conference
	committee_id bigint null references committees(id) on delete cascade -- we can also customize for a committee
);

-- present layout seats for conferences
create table layout_seats (
	layout_id bigint not null references layouts(id) on delete cascade,
	representation_id bigint not null references representations(id) on delete cascade, 
	seat_label varchar(3), 

	primary key (layout_id, representation_id)
);

-- real committee seats. We'll use a copy-on-create strategy (thx codex) to populate this
create table committee_seats (
	committee_id bigint not null references committees(id) on delete cascade,
	representation_id bigint not null references representations(id) on delete cascade,
	seat_label varchar(3), 
		
	primary key (committee_id, representation_id)
);

------------------------------------------------------
--- CONFERENCE MEMBERS & ASSIGNMENTS
------------------------------------------------------

create table conference_assignments (
	id bigint primary key generated always as identity,
	conference_id bigint not null references conferences(id) on delete cascade,

	user_id uuid references auth.users(id) on delete set null, 
	name varchar(255) not null,
	email varchar(255) not null,
	institution varchar(255),

	-- Assign role and permissions
	role conference_role not null default 'participant',

	-- null if conference_role is admin/press/staff
	committee_id bigint references committees(id) on delete set null,

	-- null if not participant/delegation
	representation_id bigint null references representations(id) on delete set null, 

	created_at timestamptz not null default now(),
	unique (conference_id, email, committee_id)
);

create index idx_conf_assignments_user on conference_assignments(user_id);
create index idx_conf_assignments_comm on conference_assignments(committee_id);
create index idx_conf_assignments_conf on conference_assignments(conference_id);
