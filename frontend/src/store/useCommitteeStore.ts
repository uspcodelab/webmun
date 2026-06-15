import { create } from 'zustand'
import {type SessionLiveState} from '../schemas/types.gen'

export const useCommitteeStore = create<SessionLiveState>(() =>({
	session_id: -1,
	start_time: "",

	delegations: [],

	current_state: undefined,

    timer_is_running: false,
    timer_expiration: null,
    timer_remaining_seconds: 0,
    current_speaker: null,

    gsl_queue: [],
    can_set_motion: false,
    gsl_default_time_seconds: 0,
    caucus_list: [],

    debate: null,

    submitted_motions: [],
    submitted_questions: [],

	agenda_topics: [],
	active_topic_index: null,
	voting: null,
	voting_choice: null,

    roll_call: {},
}));

export const UpdateStore = (state:SessionLiveState) => useCommitteeStore.setState(state)