create type activity_status as enum ('active', 'closed', 'planned', 'cancelled');
create type committee_role as enum ('chair', 'delegate');
create type asset_type as enum ('preset', 'custom');

create table conferences (
	id bigint primary key generated always as identity, 
	name varchar(255) not null,
	status activity_status not null default 'planned',
	owner_id uuid not null references auth.users on delete cascade
);

create table committees (
	id bigint primary key generated always as identity,
	conference_id bigint not null references conferences(id),
	name varchar(64) not null,
	status activity_status not null default 'planned'
);

-- This table references preset/custom representations that we might work with. We can perhaps separate the two of them later
create table representations (
	id bigint primary key generated always as identity,
	name varchar(64), 
	rep_type asset_type not null default 'preset',
	code varchar(10),
	identifier varchar(255) not null, -- this can be either an url if the rep_type is custom, or a code (like 'br')
	conference_id bigint null -- if set references a specific conference. if we delete that conference entry, we might setup a custom handler on the
	-- backend
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

create table committee_assignments (
	user_id uuid not null references auth.users(id) on delete cascade, 
	committee_id bigint not null references committees(id) on delete cascade,
	role committee_role not null,
	representation_id bigint null references representations(id), 

	primary key (user_id, committee_id)
);

create table sessions (
	id bigint primary key generated always as identity,
	committee_id bigint not null references committees(id) on delete cascade,
	status activity_status not null default 'planned',
	started_at timestamptz,
	ended_at timestamptz,
	state_snapshot JSONB
);

