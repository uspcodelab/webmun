import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SessionPage from './pages/Session';
import LoginPage from './pages/Login_page';

function App() {
	// We'll use react-router in order to develop our SPA 
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/commitees/:commiteeId/session" element={<SessionPage />} />
				<Route path="/login" element={<LoginPage />} />
			</Routes>
		</BrowserRouter>
	);
}

export default App
