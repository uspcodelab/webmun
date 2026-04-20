import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useCommitteeStore } from '../store/useCommitteeStore.ts'

export default function SessionPage() {
  // id that matches the name given in the Route path, at App.tsx 
  const { commiteeId } = useParams<{ committeeId: string }>();

  // extract what we need from the committee store
  const { sessionStart, setSessionStart } = useCommitteeStore();

  const [status, setStatus] = useState("Connecting...");
  const [uptime, setUptime] = useState(0);

  useEffect(() => {
    // Initialize WebSocket
    const socket = new WebSocket(`ws://localhost:8000/committees/ws/${commiteeId}`);

    socket.onopen = () => setStatus("Connected");
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "INITIAL_STATE") {
		  setSessionStart(data.payload.start_time);
      }
    };

    socket.onclose = () => setStatus("Disconnected");

    return () => socket.close(); // Cleanup on unmount
  }, [commiteeId, setSessionStart, setStatus]);

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
        <div className="p-10 text-center">
            <p className={status === "connected" ? "text-green-500" : "text-red-500"}>
                {status}
            </p>
            <div className="text-6xl font-bold mt-10">
                {sessionStart ? `${uptime}s` : "Waiting for session..."}
            </div>
        </div>
    );
}
