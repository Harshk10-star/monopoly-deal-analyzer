// import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Demo Auth Context that always returns authenticated
// const DemoAuthContext = React.createContext({
//   isAuthenticated: true,
//   user: { id: 1, email: 'demo@example.com', subscription_status: 'active', credits: 999 },
// });

// Override the useAuth hook for demo
// import { useAuth as originalUseAuth } from './contexts/AuthContext';
// Mock auth implementation for demo
// Commented out to avoid unused variable warning
/*
const mockAuthHook = () => ({
  isAuthenticated: true,
  user: { id: 1, email: 'demo@example.com', subscription_status: 'active', credits: 999 },
  login: () => Promise.resolve(),
  register: () => Promise.resolve(),
  logout: () => {},
  updateUser: () => {},
});
*/

// Use the mock auth
// const useAuth = mockAuthHook; // Commented out to avoid unused variable warning

function AppDemo() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-background">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard/*" element={<Dashboard />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default AppDemo;
