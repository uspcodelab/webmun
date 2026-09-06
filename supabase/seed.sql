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

insert into layouts
	(name, conference_id, committee_id)
values
	('Standard 21 Room', null, null);

insert into layout_seats 
	(layout_id, representation_id, seat_label) 
values
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'al'), '3-4'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'de'), '2-5'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'au'), '2-4'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'br'), '3-2'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'cn'), '1-6'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'kr'), '3-5'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'ae'), '3-9'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'us'), '1-2'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'ph'), '2-2'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'fr'), '1-4'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'gt'), '3-7'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'hk'), '3-1'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'in'), '3-6'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'id'), '3-3'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'jp'), '2-1'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'my'), '2-3'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'gb'), '1-3'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'ru'), '1-5'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'ch'), '3-8'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'tw'), '1-1'),
    ((select id from layouts where name = 'Standard 21 Room'), (select id from representations where code = 'tr'), '2-6');
