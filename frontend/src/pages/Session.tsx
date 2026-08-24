import { Navigate, useParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useCommitteeStore } from '../store/useCommitteeStore.ts'
import { SessionProvider } from '@/context/SessionContext.tsx';
import MotionsList from "@/components/session/motions-list"
import SpeakerList from "@/components/session/speaker-list"
import BottomBar from "@/components/session/bottom-bar"
import TopBar from '@/components/session/top-bar';
import DelegationMap from '@/components/session/delegation-map';
import VotingPopup from '@/components/session/voting-popup.tsx';

export default function SessionPage() {

    const {loading, token } = useAuth()
    // id that matches the name given in the Route path, at App.tsx 
    const { sessionId } = useParams<{ sessionId: string }>();
    const parsedSessionId = Number(sessionId);
    const all = useCommitteeStore();

    if (loading) return <p>Loading session…</p>;
    if (!token) return <Navigate to="/login" replace />;
    if (!Number.isInteger(parsedSessionId) || parsedSessionId < 1) {
        return <p>Invalid session ID.</p>;
    }

    console.log(all);
    return (
    <SessionProvider>
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
                    {//{debateType === DebateTypes.UNMODERATED_DEBATE && <UnmoderatedDebate />}
                    //{debateType === DebateTypes.MODERATED_DEBATE && <ModeratedDebate />}
                    //{debateType === DebateTypes.SPEAKERS_LIST && <SpeakerList />}
                    }
                    <SpeakerList />
                    <MotionsList  />
                </div>
            </div>
            <BottomBar />
        </div>
    </SessionProvider>
    );
}
