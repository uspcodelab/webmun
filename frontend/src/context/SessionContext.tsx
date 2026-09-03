import { useContext, type ReactNode } from 'react';
import { createContext, useEffect, useState } from 'react';
import { useAuth } from './AuthContext';
import { useParams } from 'react-router-dom';
import { UpdateStore } from '@/store/useCommitteeStore';
import { type SessionEvent, type SessionRepresentation, type AuthenticateMessage, type ServerSessionMessage, type EventMessage, SessionEffectType, type SessionEffect } from '@/schemas/types.gen';


interface SessionContextType {
	role: string
	representation_id: number | null
}

const SessionContext = createContext<SessionContextType>({
	role: "",
	representation_id: null,
});

let socket: WebSocket | null = null



// 2. Augment the global HTMLElementEventMap (or WindowEventMap)
declare global {
  interface HTMLElementEventMap {
    'voteclose': CustomEvent<SessionEffect>;
  }
}

export function SessionProvider({ children }: { children: ReactNode }) {
	const { token } = useAuth()
	const { sessionId } = useParams<{ sessionId: string }>();
	const parsedSessionId = Number(sessionId);

	const [, setStatus] = useState("Connecting...");

	useEffect(() => {
		if (!token || !Number.isInteger(parsedSessionId) || parsedSessionId < 1) {
			return;
		}

		const ws = new WebSocket(
			`${import.meta.env.VITE_WS_URL}/${parsedSessionId}/ws`,
		);
		socket = ws

		ws.onopen = () => {
			const auth_payload: AuthenticateMessage = {
				'type': 'authenticate', // explicitly pass the type here
				'access_token': token,
			};

			ws?.send(JSON.stringify(auth_payload));
			setStatus("Connected");
		}

		ws.onmessage = (event) => {
			// Route each message received
			const data = JSON.parse(event.data) as ServerSessionMessage;
			console.log("Received data", data);
			switch (data.type) {
				case 'state_snapshot': {
					UpdateStore(data.state)
					break;
				}
				case 'dispatch_result': {
					UpdateStore(data.state);
					if (data.effect) {
						console.log("Side effect / event result", data.effect);
					
						if(data.effect?.type === SessionEffectType.VOTE_CLOSED){
							const closeevnt = new CustomEvent("voteclose", {"detail": data.effect});
							window.dispatchEvent(closeevnt); //possibly inefficient
						}
					}
					break;
				}
				case 'event_rejected': {
					console.log(`Event was rejected. Code: [${data.code}]\n Message: ${data.message}`);
					break;
				}
				default: {
					console.warn("Unhandled message received:", data);
					break;
				}
			}
		};

		ws.onclose = () => setStatus("Disconnected");

		return () => {
			ws.close();
			if (socket === ws) socket = null;
		}
	}, [parsedSessionId, token]);

	const [role, setRole] = useState("")
	const [representation_id, setRepresentation_id] = useState<number | null>(null)

	useEffect(() => {
		fetch(`${import.meta.env.VITE_API_URL}/access/sessions/${parsedSessionId}/me`,
			{
				method: "GET",
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				}
			}
		).then((response) => {
			if (!response.ok) throw new Error("Error when getting role")
			return response.json()
		}).then((data: SessionRepresentation) => { setRole(data.role); setRepresentation_id(data.representation_id); })
	}, [parsedSessionId, token])

	const value = {
		role: role,
		representation_id: representation_id
	}

	return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function sendMessage(event: SessionEvent) {
	if (socket && socket.readyState === WebSocket.OPEN) {
		// Send EventMessage payload
		const payload: EventMessage = {
			'type': 'event',
			request_id: crypto.randomUUID(),
			event,
		}
		socket.send(JSON.stringify(payload));
	}
	else {
		console.error("WebSocket is not connected.");
	}
}

export const useSession = () => useContext(SessionContext)
