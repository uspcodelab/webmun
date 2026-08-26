-- Reset-only local development seed.
-- This file assumes `supabase db reset`: generated public-table IDs start at 1.
-- Do not run it against an existing database.

begin;

insert into public.conferences
    (name, status, owner_id, start_date, end_date)
values
    (
        'I WebMUN',
        'active',
        '11111111-1111-1111-1111-111111111111',
        timestamptz '2026-08-01 09:00:00+00',
        timestamptz '2026-08-03 18:00:00+00'
    );

-- Conference ID 1
insert into public.committees (conference_id, name, code, status)
values (1, 'CSNU', 'CSNU', 'planned');

-- Representation IDs 1–21, in the same order as the seat maps below.
insert into public.representations (name, code, identifier) values
    ('Albânia', 'al', 'al'),
    ('Alemanha', 'de', 'de'),
    ('Austrália', 'au', 'au'),
    ('Brasil', 'br', 'br'),
    ('China', 'cn', 'cn'),
    ('Coreia do Sul', 'kr', 'kr'),
    ('Emirados Árabes', 'ae', 'ae'),
    ('Estados Unidos', 'us', 'us'),
    ('Filipinas', 'ph', 'ph'),
    ('França', 'fr', 'fr'),
    ('Guatemala', 'gt', 'gt'),
    ('Hong Kong', 'hk', 'hk'),
    ('Índia', 'in', 'in'),
    ('Indonésia', 'id', 'id'),
    ('Japão', 'jp', 'jp'),
    ('Malásia', 'my', 'my'),
    ('Reino Unido', 'gb', 'gb'),
    ('Rússia', 'ru', 'ru'),
    ('Suíça', 'ch', 'ch'),
    ('Taiwan', 'tw', 'tw'),
    ('Turquia', 'tr', 'tr');

-- Layout ID 1
insert into public.layouts (name, conference_id, committee_id)
values ('Standard 21 Room', null, null);

insert into public.layout_seats (layout_id, representation_id, seat_label) values
    (1, 1, '3-4'), (1, 2, '2-5'), (1, 3, '2-4'), (1, 4, '3-2'),
    (1, 5, '1-6'), (1, 6, '3-5'), (1, 7, '3-9'), (1, 8, '1-2'),
    (1, 9, '2-2'), (1, 10, '1-4'), (1, 11, '3-7'), (1, 12, '3-1'),
    (1, 13, '3-6'), (1, 14, '3-3'), (1, 15, '2-1'), (1, 16, '2-3'),
    (1, 17, '1-3'), (1, 18, '1-5'), (1, 19, '3-8'), (1, 20, '1-1'),
    (1, 21, '2-6');

-- Committee ID 1
insert into public.committee_seats
    (committee_id, representation_id, seat_label)
values
    (1, 1, '3-4'), (1, 2, '2-5'), (1, 3, '2-4'), (1, 4, '3-2'),
    (1, 5, '1-6'), (1, 6, '3-5'), (1, 7, '3-9'), (1, 8, '1-2'),
    (1, 9, '2-2'), (1, 10, '1-4'), (1, 11, '3-7'), (1, 12, '3-1'),
    (1, 13, '3-6'), (1, 14, '3-3'), (1, 15, '2-1'), (1, 16, '2-3'),
    (1, 17, '1-3'), (1, 18, '1-5'), (1, 19, '3-8'), (1, 20, '1-1'),
    (1, 21, '2-6');

insert into public.conference_assignments
    (conference_id, user_id, name, email, role, committee_id, representation_id)
values
    (1, '11111111-1111-1111-1111-111111111111', 'Chair Person', 'chair@codelab.usp.br', 'chair', 1, null),
    (1, '22222222-2222-2222-2222-222222222222', 'Delegate Albania', 'albania@codelab.usp.br', 'participant', 1, 1),
    (1, '33333333-3333-3333-3333-333333333333', 'Delegate Germany', 'alemanha@codelab.usp.br', 'participant', 1, 2),
    (1, '44444444-4444-4444-4444-444444444444', 'Delegate Brazil', 'brazil@codelab.usp.br', 'participant', 1, 4);

-- Session ID 1
insert into public.sessions (committee_id) values (1);

commit;
