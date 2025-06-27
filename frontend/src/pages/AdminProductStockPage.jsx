import { useState } from "react";
import axios from "axios";
import api from "../services/api"; // Adjust the import path as needed

export default function AdminProductStockPage() {
  // ----- state -----
  const [articleNr, setArticleNr] = useState("");
  const [product, setProduct] = useState(null);
  const [newStock, setNewStock] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  // ----- helpers -----
  const reset = () => {
    setProduct(null);
    setNewStock("");
  };

  // ----- fetch -----
  const fetchProduct = async () => {
    if (!articleNr) return;
    setLoading(true);
    setMessage(null);
    try {
      const res = await api.get(`/adminpanel/stock_updater/?article_nr=${articleNr}`);
      setProduct(res.data);
      setNewStock(res.data.stock);
    } catch (err) {
      reset();
      setMessage(err.response?.data?.error || "No product found");
    } finally {
      setLoading(false);
    }
  };

  const updateStock = async () => {
    if (!product) return;
    setLoading(true);
    setMessage(null);
    try {
      await api.patch("/adminpanel/stock_updater/", {
        article_nr: product.article_nr,
        new_stock: Number(newStock),
      });
      setProduct({ ...product, stock: Number(newStock) });
      setMessage("New stock saved ✔️");
    } catch (err) {
      setMessage(err.response?.data?.error || "Save failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Stock‑Updater</h1>

      {/* Suche */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Artikelnummer"
          value={articleNr}
          onChange={(e) => setArticleNr(e.target.value)}
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          onClick={fetchProduct}
          disabled={!articleNr || loading}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {loading ? "loading..." : "Search"}
        </button>
      </div>

      {/* Produktinfo */}
      {product && (
        <div className="border rounded p-4 space-y-3">
          <div className="font-semibold text-lg">{product.name}</div>
          <div className="text-sm text-gray-600">Artikel‑Nr.: {product.article_nr}</div>
          <div className="flex items-center gap-2">
            <span>Current Stock:</span>
            <span className="font-bold">{product.stock}</span>
          </div>

          {/* Stock ändern */}
          <div className="flex gap-2 items-center mt-2">
            <input
              type="number"
              min="0"
              value={newStock}
              onChange={(e) => setNewStock(e.target.value)}
              className="w-24 border rounded px-2 py-1"
            />
            <button
              onClick={updateStock}
              disabled={loading || newStock === ""}
              className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {loading ? "Save..." : "Save Stock"}
            </button>
          </div>
        </div>
      )}

      {/* Meldung */}
      {message && (
        <div className="p-3 rounded bg-gray-100 text-center text-sm">{message}</div>
      )}
    </div>
  );
}
