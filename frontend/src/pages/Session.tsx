import { Navigate, useParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useCommitteeStore } from '../store/useCommitteeStore.ts'
import { SessionProvider } from '@/context/SessionContext.tsx';
import MotionsList from "@/components/session/Sidebar/motions-list.tsx"
import SpeakerList from "@/components/session/Sidebar/speaker-list.tsx"
import ModeratedDebate from "@/components/session/Sidebar/moderated-debate.tsx"
import UnmoderatedDebate from "@/components/session/Sidebar/unmoderated-debate.tsx"
import VotingMenu from "@/components/session/Sidebar/voting.tsx"
import BottomBar from "@/components/session/bottom-bar"
import TopBar from '@/components/session/top-bar';
import DelegationMap from '@/components/session/delegation-map';
import VotingPopup from '@/components/session/voting-popup.tsx';
import { Spinner } from "@/components/ui/spinner"
import { States } from '@/schemas/types.gen';
import { Clock8 } from 'lucide-react';

export default function SessionPage() {


    const { loading, token } = useAuth()
    // id that matches the name given in the Route path, at App.tsx 
    const { sessionId } = useParams<{ sessionId: string }>();
    const parsedSessionId = Number(sessionId);
    const all = useCommitteeStore();
    const currentState = useCommitteeStore((state) => state.current_state)

    if (loading) return (
        <div className="flex h-full w-full flex-col items-center justify-center gap-4">
            <Spinner className="mx-auto mt-10 h-16 w-16 text-primary" />
            < p > Loading session…</p >
        </div>
    );
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
                        {currentState === States.SETUP_ROOM && <div className='flex flex-1 items-center justify-center text-muted-foreground'><div className="flex flex-col gap-2 items-center"> <Clock8 className="h-10 w-10" /> <p>Aguarde a Sessão Começar</p></div></div>}
                        {currentState === States.OPEN_GSL && <SpeakerList />}
                        {currentState === States.MODERATED_CAUCUS && <ModeratedDebate />}
                        {currentState === States.UNMODERATED_CAUCUS && <UnmoderatedDebate />}
                        {currentState === States.VOTING_EXECUTION && <VotingMenu />}
                        {currentState !== States.SETUP_ROOM  && <MotionsList />}
                        
                    </div>
                </div>
                <BottomBar />
            </div>
        </SessionProvider>
    );
}
