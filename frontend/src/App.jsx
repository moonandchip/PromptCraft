import AppRoutes from "./router/AppRouter";
import { AuthProvider } from "./components/AuthContext";

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
