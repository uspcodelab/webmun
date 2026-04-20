import { create } from 'zustand'

interface CommitteeState {
	committeeId: number;
	committeeName: string;
	sessionStart: string; // ISO string for datetime

	setCommiteeId: (id: number) => void;
	setCommitteeName: (name: string) => void;
	setSessionStart: (time: string) => void;

}

export const useCommitteeStore = create<CommitteeState>((set) =>({
	committeeId: null,
	committeeName: null,
	sessionStart: null,

	setCommiteeId: (id) => set({committeeId: id}),
	setCommitteeName: (name) => set({committeeName: name}),
	setSessionStart: (time) => set({sessionStart: time}),
}));
