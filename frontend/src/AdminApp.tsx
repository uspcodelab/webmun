import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import type { ReactNode } from 'react';
import { useAuth } from '@/context/AuthContext';

import AdminLoginPage from './pages/Admin/AdminLogin.tsx';
import AdminDash from './pages/Admin/AdminDashboard.tsx';




function RequireAuth({ children }: { children: ReactNode }) {
    const { loading, token } = useAuth();

    if (loading) return <p>Loading session…</p>;
    if (!token) return <Navigate to="/login" replace />;

    return children;
}

function PublicApp() {
    // We'll use react-router in order to develop our SPA 
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<AdminLoginPage />} />

                
                <Route path="/dashboard" element={<RequireAuth><AdminDash/></RequireAuth>}>

                </Route>

            </Routes>
            
        </BrowserRouter>
    );
}

export default PublicApp
