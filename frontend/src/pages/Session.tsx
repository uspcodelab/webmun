import { useEffect, useState} from 'react';
import { Navigate, useParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { UpdateStore, useCommitteeStore } from '../store/useCommitteeStore.ts'
import MotionsList from "@/components/session/motions-list"
import SpeakerList from "@/components/session/speaker-list"
import ModeratedDebate from "@/components/session/moderated-debate"
import UnmoderatedDebate from "@/components/session/unmoderated-debate"
import BottomBar from "@/components/session/bottom-bar"
import TopBar from '@/components/session/top-bar';
import DelegationMap from '@/components/session/delegation-map';
import VotingPopup from '@/components/session/voting-popup.tsx';
import { DebateTypes } from '@/schemas/types.gen';

let socket : WebSocket | null = null;

/*
Use this function to send events to the backend, 
any data with one of the Event types in schemas/types.gen.ts should work
*/
export function sendMessage(data: any) {
    if (socket && socket.readyState === WebSocket.OPEN) 
    {
        socket.send(JSON.stringify(data));
    } 
    else 
    {
        console.error("WebSocket is not connected.");
    }
}


export default function SessionPage() {

    const { loading, token } = useAuth()

    const debateType = useCommitteeStore((state) => state.debate?.debate_type)

    const motions = [
        {
            id: "motion-1",
            timestamp: "15:58",
            title: "Mocao para debate moderado, de 3 discursos",
            proposer: "Republica Francesa",
            proposerCode: "fr",
            priority: 2,
        },
        {
            id: "motion-2",
            timestamp: "16:02",
            title: "Mocao para caucus nao moderado, de 10 minutos",
            proposer: "Brasil",
            proposerCode: "br",
            priority: 3,
        },
        {
            id: "motion-3",
            timestamp: "16:05",
            title: "Mocao para extensao de tempo de debate",
            proposer: "Espanha",
            proposerCode: "es",
            priority: 3,
        },
    ]

    // id that matches the name given in the Route path, at App.tsx 
    const { sessionId } = useParams<{ sessionId: string }>();
    const parsedSessionId = Number(sessionId);
    //const {start_time} = useCommitteeStore();
    const all = useCommitteeStore();

    const [, setStatus] = useState("Connecting...");
    //const [, setUptime] = useState(0);

    useEffect(() => {
        if (!token || !Number.isInteger(parsedSessionId) || parsedSessionId < 1) {
            return;
        }

        const ws = new WebSocket(
            `${import.meta.env.VITE_WS_URL}/ws/${parsedSessionId}`,
        );
		socket = ws;

        ws.onopen = () => {
            ws?.send(JSON.stringify({ access_token: token }));
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

    if (loading) return <p>Loading session…</p>;
    if (!token) return <Navigate to="/login" replace />;
    if (!Number.isInteger(parsedSessionId) || parsedSessionId < 1) {
        return <p>Invalid session ID.</p>;
    }

    // Useeffect for local uptime timer 
    /*useEffect(() => {

        if (!start_time) return;

        // calculate timer
        const interval = setInterval(() => {
            const start = new Date(start_time).getTime();
            const now = new Date().getTime();
            setUptime(Math.floor((now - start) / 1000));
        }, 1000);


        return () => clearInterval(interval);
    }, [start_time]);*/
    console.log(all);
    return (
        <div>
            {/* <p className={status === "connected" ? "text-green-500" : "text-red-500"}>
                {status}
            </p>
            <div className="text-6xl font-bold mt-10">
                {sessionStart ? `${uptime}s` : "Waiting for session..."}
            </div> */}

            <VotingPopup />
            <TopBar />
            <div className="flex h-[82vh] w-full">
                <div className="min-w-0 flex-1 bg-neutral-100">
                    <DelegationMap
                        semicircleCount={3}
                        buttonsPerSemicircle={[6, 6, 9]}
                    />
                </div>
                <div className="flex h-full w-[25%] shrink-0 flex-col bg-white">
                    {debateType === DebateTypes.UNMODERATED_DEBATE && <UnmoderatedDebate />}
                    {debateType === DebateTypes.MODERATED_DEBATE && <ModeratedDebate />}
                    {debateType === DebateTypes.SPEAKERS_LIST && <SpeakerList />}
                    <MotionsList motions={motions} />
                </div>
            </div>
            <BottomBar />
        </div>

    );
}
