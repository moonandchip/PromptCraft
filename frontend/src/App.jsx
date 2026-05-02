import AppRoutes from "./router/AppRouter";
import { AuthProvider } from "./components/AuthContext";
import ErrorBoundary from "./components/ErrorBoundary";
import { LoadingProvider } from "./components/LoadingContext";

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <LoadingProvider>
          <AppRoutes />
        </LoadingProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
