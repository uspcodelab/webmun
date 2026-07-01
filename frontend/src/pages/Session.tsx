import { useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';
import { UpdateStore } from '../store/useCommitteeStore.ts'
import SpeakerList from "@/components/session/speaker-list"
import MotionsList from "@/components/session/motions-list"
import BottomBar from "@/components/session/bottom-bar"
import TopBar from '@/components/session/top-bar';
import DelegationMap from '@/components/session/delegation-map';

let socket : WebSocket | null = null;

/*
Use this function to send events to the backend, 
any data with one of the Event types in schemas/types.gen.ts should work
*/
export function sendMessage(data: unknown) {
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
    //const {start_time} = useCommitteeStore();
    const [, setStatus] = useState("Connecting...");
    //const [, setUptime] = useState(0);

    useEffect(() => {
        // Initialize WebSocket
        socket = new WebSocket(`ws://localhost:8000/committees/ws/0?role=CHAIR&display_name=Chair`);

        socket.onopen = () => 
            {
                setStatus("Connected");
            }

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            UpdateStore(data);
        };

        socket.onclose = () => setStatus("Disconnected");

        return () => socket?.close(); // Cleanup on unmount
    }, [committeeId]);

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
    return (
        <div>
            {/* <p className={status === "connected" ? "text-green-500" : "text-red-500"}>
                {status}
            </p>
            <div className="text-6xl font-bold mt-10">
                {sessionStart ? `${uptime}s` : "Waiting for session..."}
            </div> */}


            <TopBar />
            <div className="flex h-[82vh] w-full">
                <div className="min-w-0 flex-1 bg-neutral-100">
                    <DelegationMap
                        semicircleCount={3}
                        buttonsPerSemicircle={[6, 6, 9]}
                    />
                </div>
                <div className="flex h-full w-[20%] shrink-0 flex-col bg-white">
                    <SpeakerList />
                    <MotionsList motions={motions} />
                </div>
            </div>
            <BottomBar />
        </div>

    );
}
