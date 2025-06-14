import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';

import { AuthProvider } from './contexts/AuthContext';
import { CartProvider } from './contexts/CartContext';

import HomePage from './pages/HomePage'; // ✅ Neu: Startseite
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
import Checkout from './pages/CheckoutPage';
import LoosePwPage from './pages/LoosePwPage';
import PasswordResetPage from './pages/PasswordResetPage';
import ProductDetailPage from './pages/ProductDetailPage';
import OrderList from './pages/OrderListPage';
import OrderDetail from './pages/OrderDetailPage';
import PaymentSuccessPage from './pages/PaymentSuccessPage';
import PaymentCanclePage from './pages/PaymentCanclePage';
import AdminOrdersPage from './pages/AdminOrdersPage';
import AdminUserPage from './pages/AdminUsersPage';
import AdminPanelPage from './pages/AdminPanelPage';
import AdminOrdersDetailPage from './pages/AdminOrdersDetailPage';
import AdminOrderStatusManager from './pages/AdminOrderStatusManager';
import ImprintPage from './pages/ImprintPage';
import PrivacyPage from './pages/PrivacyPage';
import GTCPage from './pages/GTCPage';
import ContactPage from './pages/ContactPage';
import WishlistPage from './pages/WishlistPage';
import { WishlistProvider } from './contexts/WishlistContext';

function App() {
  useEffect(() => {
    ensureCsrfCookie();
  }, []);

  return (
    <BrowserRouter>
      <AuthProvider>
        <WishlistProvider>
          <CartProvider>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path="productlist" element={<ProductList />} />
                <Route path="about" element={<About />} />
                <Route path="login" element={<LoginPage />} />
                <Route path="profile" element={<ProfilePage />} />
                <Route path="sign_up" element={<RegisterPage />} />
                <Route path="verify/:token" element={<VerifyEmailPage />} />
                <Route path="check_email" element={<CheckEmailPage />} />
                <Route path="cart" element={<CartPage />} />
                <Route path="checkout" element={<Checkout />} />
                <Route path="password_reset" element={<LoosePwPage />} />
                <Route path="password_reset/:token" element={<PasswordResetPage />} />
                <Route path="products/:id" element={<ProductDetailPage />} />
                <Route path="orderlist" element={<OrderList />} />
                <Route path="order_detail/:id" element={<OrderDetail />} />
                <Route path="payments/success_payment/:orderId" element={<PaymentSuccessPage />} />
                <Route path="payments/cancel_payment" element={<PaymentCanclePage />} />
                <Route path="adminpanel/orders" element={<AdminOrdersPage />} />
                <Route path="adminpanel/users" element={<AdminUserPage />} />
                <Route path="adminpanel" element={<AdminPanelPage />} />
                <Route path="adminpanel/orders/:id" element={<AdminOrdersDetailPage />} />
                <Route path="adminpanel/order_status_manager" element={<AdminOrderStatusManager />} />
                <Route path="imprint" element={<ImprintPage />} />
                <Route path="privacy" element={<PrivacyPage />} />
                <Route path="gtc" element={<GTCPage />} />
                <Route path="contact" element={<ContactPage />} />
                <Route path="wishlist" element={<WishlistPage />} />
              </Route>
            </Routes>
          </CartProvider>
        </WishlistProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
