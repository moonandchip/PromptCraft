import AppRoutes from "./router/AppRouter";
import { AuthProvider } from "./components/AuthContext";
import { LoadingProvider } from "./components/LoadingContext";

function App() {
  return (
    <AuthProvider>
      <LoadingProvider>
        <AppRoutes />
      </LoadingProvider>
    </AuthProvider>
  );
}

export default App;
