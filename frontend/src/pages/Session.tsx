import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useCommitteeStore } from '../store/useCommitteeStore.ts'
import SpeakerList from "@/components/session/speaker-list"
import MotionsList from "@/components/session/motions-list"
import BottomBar from "@/components/session/bottom-bar"
import TopBar from '@/components/session/top-bar';

export default function SessionPage() {
    const speakers = [
        { id: "fr", position: 1, countryName: "Franca", countryCode: "fr", speechTime: "01:53", isSpeaking: true },
        { id: "br", position: 2, countryName: "Brasil", countryCode: "br", speechTime: "02:00" },
        { id: "es", position: 3, countryName: "Espanha", countryCode: "es", speechTime: "02:00" },
        { id: "br-3", position: 4, countryName: "Brasil", countryCode: "br", speechTime: "02:00" },
    ]

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
    const { committeeId } = useParams<{ committeeId: string }>();

    // extract what we need from the committee store
    const { sessionStart, setSessionStart } = useCommitteeStore();

    const [, setStatus] = useState("Connecting...");
    const [, setUptime] = useState(0);

    useEffect(() => {
        // Initialize WebSocket
        const socket = new WebSocket(`ws://localhost:8000/committees/ws/${committeeId}`);

        socket.onopen = () => setStatus("Connected");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "INITIAL_STATE") {
                setSessionStart(data.payload.start_time);
            }
        };

        socket.onclose = () => setStatus("Disconnected");

        return () => socket.close(); // Cleanup on unmount
    }, [committeeId, setSessionStart, setStatus]);

    // Useeffect for local uptime timer 
    useEffect(() => {
        if (!sessionStart) return;

        // calculate timer
        const interval = setInterval(() => {
            const start = new Date(sessionStart).getTime();
            const now = new Date().getTime();
            setUptime(Math.floor((now - start) / 1000));
        }, 1000);

        return () => clearInterval(interval);
    }, [sessionStart]);

    return (
        <div>
            {/* <p className={status === "connected" ? "text-green-500" : "text-red-500"}>
                {status}
            </p>
            <div className="text-6xl font-bold mt-10">
                {sessionStart ? `${uptime}s` : "Waiting for session..."}
            </div> */}


            <TopBar />
            <div className="flex flex-1 h-[82vh]">
                <div className="flex-1 bg-neutral-100">[MAP PLACEHOLDER]</div>
                <div className="fixed right-0 top-[10vh] h-[90vh] w-[20%] bg-white">
                    <SpeakerList speakers={speakers} />
                    <MotionsList motions={motions} />
                </div>
            </div>
            <BottomBar />
        </div>

    );
}
