import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import type { ReactNode } from 'react';
import { useAuth } from '@/context/AuthContext';
import SessionPage from './pages/Session';
import LoginPage from './pages/Login_page';
import Home from './pages/Home';
import Pricing from './pages/Info Pages/Pricing';
import OurTeam from './pages/Info Pages/OurTeam';
import ContactUs from './pages/Info Pages/Contact-us';
import SignupPage from './pages/Signup';
import UserDash from './pages/UserDashboard';
import DashHome from './components/userDashboard/dash-home.tsx';
import CreateCommittee from './pages/CreateCommittee';
import BasicInfo from './components/userDashboard/conferenceMenus/about/conference-basic-info.tsx';


import ConferenceOverview from './components/userDashboard/conferenceMenus/conference-overview';
import Enrollment from './components/userDashboard/conferenceMenus/participants/enrollment';
import ParticipantListAllocation from './components/userDashboard/conferenceMenus/participants/list-allocation';
import PresenceCertificates from './components/userDashboard/conferenceMenus/participants/presence-certificates';
import ConferenceSchedule from './components/userDashboard/conferenceMenus/about/conference-schedule';
import TeamStructure from './components/userDashboard/conferenceMenus/team/team-structure';
import TeamAllocate from './components/userDashboard/conferenceMenus/team/team-alocate';
import CommitteeManagement from './components/userDashboard/conferenceMenus/committee-managemant';
import ConferenceDocs from './components/userDashboard/conferenceMenus/about/conference-docs';
import ManagePermsRoles from './components/userDashboard/conferenceMenus/team/manage-perms-roles.tsx';
import CommitteeSessions from './components/userDashboard/committeeMenus/committee-sessions.tsx';
import CommitteeDocs from './components/userDashboard/committeeMenus/committee-docs.tsx';
import CommitteeInfo from './components/userDashboard/committeeMenus/committee-info.tsx';



function RequireAuth({ children }: { children: ReactNode }) {
	const { loading, token } = useAuth();

	if (loading) return <p>Loading session…</p>;
	if (!token) return <Navigate to="/login" replace />;

	return children;
}

function App() {
	// We'll use react-router in order to develop our SPA 
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route
					path="/sessions/:sessionId"
					element={<RequireAuth><SessionPage /></RequireAuth>}
				/>
				<Route path="/pricing" element={<Pricing />} />
				<Route path="/our-team" element={<OurTeam />} />
				<Route path="/contact-us" element={<ContactUs />} />
				<Route path="/login" element={<LoginPage />} />
				<Route path="/signup" element={<SignupPage />} />
				<Route path="/dashboard" element={<UserDash />}>
					<Route index element={<DashHome />} />
					<Route path="conference/overview" element={<ConferenceOverview />} />
					<Route path="conference/about/basic-info" element={<BasicInfo />} />
					<Route path="conference/about/schedule" element={<ConferenceSchedule />} />
					<Route path="conference/about/docs" element={<ConferenceDocs />} />
					<Route path="conference/committees" element={<CommitteeManagement />} />
					<Route path="conference/team/onboarding" element={<TeamAllocate />} />
					<Route path="conference/team/structure" element={<TeamStructure />} />
					<Route path="conference/team/manage-perms-roles" element={<ManagePermsRoles />} />
					<Route path="conference/participants/enrollment" element={<Enrollment />} />
					<Route path="conference/participants/list-allocation" element={<ParticipantListAllocation />} />
					<Route path="conference/participants/presence-certificates" element={<PresenceCertificates />} />
					<Route path="committees/sessions" element={<CommitteeSessions />} />
					<Route path="committees/docs" element={<CommitteeDocs />} />
					<Route path="committees/info" element={<CommitteeInfo />} />
				</Route>
				<Route path="/create-committee" element={<CreateCommittee />} />
				<Route path="/committees/:committeeId/session" element={<SessionPage />} />
			</Routes>
			
		</BrowserRouter>
	);
}

export default App
