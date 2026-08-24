import { useContext, type ReactNode } from 'react';
import { createContext, useEffect, useState } from 'react';
import { useAuth } from './AuthContext';
import { useParams } from 'react-router-dom';
import { UpdateStore } from '@/store/useCommitteeStore';
import {type SessionEvent, type SessionRepresentation} from '@/schemas/types.gen';


interface SessionContextType{
  role: string
  representation_id: number | null
}

const SessionContext = createContext<SessionContextType>({
  role: "",
  representation_id: null,
});

let socket : WebSocket|null = null

export function SessionProvider({ children }: { children: ReactNode }) 
{
    const { token } = useAuth()
    const { sessionId } = useParams<{ sessionId: string }>();
    const parsedSessionId = Number(sessionId);

    const [, setStatus] = useState("Connecting...");

    useEffect(() => {
        if (!token || !Number.isInteger(parsedSessionId) || parsedSessionId < 1) {
            return;
        }

        const ws = new WebSocket(
            `${import.meta.env.VITE_WS_URL}/ws/${parsedSessionId}`,
        );
		socket = ws

        ws.onopen = () => {
            ws?.send(JSON.stringify({ type: 'authenticate', access_token: token }));
            setStatus("Connected");
        }

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
            UpdateStore(data);
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
                method:"GET",
                headers:{
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            }
        ).then((response)=>
        {
            if(!response.ok) throw new Error("Error when getting role")
            return response.json()
        }).then((data : SessionRepresentation) => {setRole(data.role); setRepresentation_id(data.representation_id);})
    }, [parsedSessionId, token])

    const value ={
        role: role,
        representation_id: representation_id
    }

    return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function sendMessage(event: SessionEvent) {
    if (socket && socket.readyState === WebSocket.OPEN) 
    {
        socket.send(JSON.stringify({
            type: 'event',
            request_id: crypto.randomUUID(),
            event,
        }));
    } 
    else 
    {
        console.error("WebSocket is not connected.");
    }
}

export const useSession = () => useContext(SessionContext)
