import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SessionPage from './pages/Session';
import LoginPage from './pages/Login_page';
import Home from './pages/Home';
import CreateCommittee from './pages/CreateCommittee';
import UserDash from './pages/UserDashboard';
import Pricing from './pages/Info Pages/Pricing';

function App() {
	// We'll use react-router in order to develop our SPA 
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/pricing" element={<Pricing />} />
				<Route path="/committees/:committeeId/session" element={<SessionPage />} />
				<Route path="/login" element={<LoginPage />} />
				<Route path="/create-committee" element={<CreateCommittee />} />
				<Route path="/dashboard" element={<UserDash />} />
			</Routes>
			
		</BrowserRouter>
	);
}

export default App
