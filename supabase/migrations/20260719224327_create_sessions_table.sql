create type session_status as enum ('Open', 'Closed');
create type session_role as enum ('CHAIR', 'DELEGATE');

create table sessions (
	id bigint primary key generated always as identity,
	name varchar(255),
	created_at timestamptz default now(),
	status session_status not null default 'Open',
	delegations_config JSONB NOT NULL DEFAULT '[]'::jsonb
);

create table session_assignments (
	user_id uuid not null references auth.users on delete cascade, 
	session_id bigint not null references sessions(id) on delete cascade,
	role session_role not null,
	delegation_id int null, 

	primary key (user_id, session_id)
);
