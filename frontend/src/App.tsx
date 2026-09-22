import AdminApp from './AdminApp.tsx';
import PublicApp from './PublicApp.tsx';

function App() {
  const hostname = window.location.hostname;

  const isAdmin =
    hostname === "admin.webmun.net" ||
    hostname === "admin.localhost";

  return isAdmin ? <AdminApp /> : <PublicApp />;
}
export default App;