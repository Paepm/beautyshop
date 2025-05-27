import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import ProductList from './components/ProductList';
import About from './pages/About';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<ProductList />} />
            <Route path="about" element={<About />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
