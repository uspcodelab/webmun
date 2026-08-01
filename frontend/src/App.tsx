import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Pricing from './pages/Info Pages/Pricing';
import OurTeam from './pages/Info Pages/OurTeam';
import ContactUs from './pages/Info Pages/Contact-us';
import LoginPage from './pages/Login_page';
import SignupPage from './pages/Signup';
import UserDash from './pages/UserDashboard';
import DashHome from './components/userDashboard/dash-home.tsx';
import CreateCommittee from './pages/CreateCommittee';
import SessionPage from './pages/Session';
import BasicInfo from './components/userDashboard/conferenceMenus/about/MUN-basic-info';



function App() {
	// We'll use react-router in order to develop our SPA 
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/pricing" element={<Pricing />} />
				<Route path="/our-team" element={<OurTeam />} />
				<Route path="/contact-us" element={<ContactUs />} />
				<Route path="/login" element={<LoginPage />} />
				<Route path="/signup" element={<SignupPage />} />
				<Route path="/dashboard" element={<UserDash />}>
					<Route index element={<DashHome />} />
					<Route path="conference/about/basic-info" element={<BasicInfo />} />
				</Route>
				<Route path="/create-committee" element={<CreateCommittee />} />
				<Route path="/committees/:committeeId/session" element={<SessionPage />} />
			</Routes>
			
		</BrowserRouter>
	);
}

export default App
