import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

export default function SessionPage() {
  // id that matches the name given in the Route path, at App.tsx 
  const { commiteeId } = useParams();
  const [timerValue, setTimerValue] = useState(0);
  const [status, setStatus] = useState("Connecting...");

  useEffect(() => {
    // 1. Initialize WebSocket
    const socket = new WebSocket(`ws://localhost:8000/committees/ws/${commiteeId}`);

    socket.onopen = () => setStatus("Connected ✅");
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "TICK") {
        setTimerValue(data.value);
      }
    };

    socket.onclose = () => setStatus("Disconnected ❌");

    return () => socket.close(); // Cleanup on unmount
  }, [commiteeId]);

  return (
    <div className="p-10 text-center">
      <h1 className="text-xl font-mono">Committee: {commiteeId}</h1>
      <p>{status}</p>
      <div className="text-6xl font-bold mt-10">{timerValue}s</div>
    </div>
  );
}
