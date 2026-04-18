import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SessionPage from './pages/Session';

function App() {
	// We'll use react-router in order to develop our SPA 
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/commitees/:commiteeId/session" element={<SessionPage />} />
			</Routes>
		</BrowserRouter>
	);
}

export default App
