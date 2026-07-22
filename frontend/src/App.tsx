import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import type { ReactNode } from 'react';
import { useAuth } from '@/context/AuthContext';
import SessionPage from './pages/Session';
import LoginPage from './pages/Login_page';
import Home from './pages/Home';
import CreateCommittee from './pages/CreateCommittee';
import UserDash from './pages/UserDashboard';

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
				<Route path="/login" element={<LoginPage />} />
				<Route path="/create-committee" element={<CreateCommittee />} />
				<Route path="/dashboard" element={<UserDash />} />
			</Routes>
			
		</BrowserRouter>
	);
}

export default App
