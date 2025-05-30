import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';

import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/layout/Layout';
import ProductList from './components/ProductList';
import About from './pages/About';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import RegisterPage from './pages/RegisterPage';
import VerifyEmailPage from './pages/VerifyEmailPage';
import CheckEmailPage from './pages/CheckEmailPage';
import CartPage from './pages/CartPage';
import { ensureCsrfCookie } from './services/csrf';
import Checkout from './pages/Checkout';

function App() {
  useEffect(() => {
    ensureCsrfCookie();
  }, []);

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<ProductList />} />
            <Route path="about" element={<About />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="sign_up" element={<RegisterPage />} />
            <Route path="verify/:token" element={<VerifyEmailPage />} />
            <Route path="check_email" element={<CheckEmailPage />} />
            <Route path="cart" element={<CartPage />} />
            <Route path="checkout" element={<Checkout />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
