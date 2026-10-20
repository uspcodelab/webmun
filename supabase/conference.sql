-- Seeds a conference with one committee and assigns the users created in users.sql.
-- Must run after seed.sql (representations, layouts) and users.sql (auth users).
DO $$
DECLARE
  id_chair     uuid := '11111111-1111-1111-1111-111111111111';
  id_albania   uuid := '22222222-2222-2222-2222-222222222222';
  id_alemanha  uuid := '33333333-3333-3333-3333-333333333333';
  id_brazil    uuid := '44444444-4444-4444-4444-444444444444';
  v_conference_id bigint;
  v_committee_id  bigint;
  v_layout_id     bigint;
BEGIN

  INSERT INTO conferences (name, status, owner_id, location, theme_color, start_date, end_date)
  VALUES ('WebMUN 2026', 'active', id_chair, 'São Paulo, SP', '#1D4ED8', now(), now() + interval '3 days')
  RETURNING id INTO v_conference_id;

  INSERT INTO committees (conference_id, name, acronym, committee_type, theme_color, status)
  VALUES (v_conference_id, 'Assembleia Geral', 'AGNU', 'General Assembly', '#1D4ED8', 'active')
  RETURNING id INTO v_committee_id;

  -- Copy the standard layout into the committee's real seats.
  SELECT id INTO v_layout_id FROM layouts WHERE name = 'Standard 21 Room';

  INSERT INTO committee_seats (committee_id, representation_id, seat_label)
  SELECT v_committee_id, representation_id, seat_label
  FROM layout_seats
  WHERE layout_id = v_layout_id;

  -- Conference-level roles.
  INSERT INTO conference_assignments (conference_id, user_id, role, committee_id) VALUES
    (v_conference_id, id_chair,    'owner',       null),
    (v_conference_id, id_chair,    'director',    v_committee_id),
    (v_conference_id, id_albania,  'participant', v_committee_id),
    (v_conference_id, id_alemanha, 'participant', v_committee_id),
    (v_conference_id, id_brazil,   'participant', v_committee_id);

  -- Committee-level roles.
  INSERT INTO committee_assignments (user_id, committee_id, role, representation_id) VALUES
    (id_chair,    v_committee_id, 'chair',    null),
    (id_albania,  v_committee_id, 'delegate', (SELECT id FROM representations WHERE code = 'al' AND committee_id IS NULL)),
    (id_alemanha, v_committee_id, 'delegate', (SELECT id FROM representations WHERE code = 'de' AND committee_id IS NULL)),
    (id_brazil,   v_committee_id, 'delegate', (SELECT id FROM representations WHERE code = 'br' AND committee_id IS NULL));

END $$;
