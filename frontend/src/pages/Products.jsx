import { useState } from 'react';
import toast from 'react-hot-toast';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';
import ConfirmDialog from '../components/ConfirmDialog.jsx';
import ProductForm from '../components/ProductForm.jsx';
import { useProducts } from '../hooks/useProducts';
import { productService } from '../services/productService';
import { formatCurrency } from '../utils/formatters';
import { LOW_STOCK_THRESHOLD } from '../utils/constants';

export default function Products() {
  const { items, total, loading, error, query, setQuery, refresh } = useProducts();
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [confirmDel, setConfirmDel] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const openCreate = () => {
    setEditing(null);
    setModalOpen(true);
  };

  const openEdit = (product) => {
    setEditing(product);
    setModalOpen(true);
  };

  const onSubmit = async (values) => {
    setSubmitting(true);
    try {
      const payload = {
        ...values,
        price: Number(values.price),
        stock_quantity: Number(values.stock_quantity),
      };
      if (editing) {
        await productService.update(editing.id, payload);
        toast.success(`Updated "${values.name}"`);
      } else {
        await productService.create(payload);
        toast.success(`Created "${values.name}"`);
      }
      setModalOpen(false);
      setEditing(null);
      await refresh();
    } catch (e) {
      toast.error(e.message || 'Save failed');
    } finally {
      setSubmitting(false);
    }
  };

  const onDelete = async () => {
    if (!confirmDel) return;
    try {
      await productService.remove(confirmDel.id);
      toast.success(`Deleted "${confirmDel.name}"`);
      setConfirmDel(null);
      await refresh();
    } catch (e) {
      toast.error(e.message || 'Delete failed');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Products</h2>
          <p className="text-sm text-slate-500 mt-1">
            {total} {total === 1 ? 'product' : 'products'} in catalog
          </p>
        </div>
        <button className="btn-primary" onClick={openCreate}>
          + Add Product
        </button>
      </div>

      <div className="card p-4">
        <input
          className="input max-w-md"
          placeholder="Search by name or SKU…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <Spinner label="Loading products…" />
      ) : error ? (
        <div className="card p-6 border-red-200 bg-red-50">
          <p className="text-red-700">{error.message}</p>
        </div>
      ) : items.length === 0 ? (
        <div className="card p-12 text-center text-slate-500">
          <p className="text-lg">No products found</p>
          <p className="text-sm mt-1">Try a different search, or add your first product.</p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600 text-left">
                <tr>
                  <th className="px-5 py-3 font-medium">SKU</th>
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Price</th>
                  <th className="px-5 py-3 font-medium">Stock</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((p) => {
                  const isLow = p.stock_quantity <= LOW_STOCK_THRESHOLD;
                  const isOut = p.stock_quantity === 0;
                  return (
                    <tr key={p.id} className="hover:bg-slate-50">
                      <td className="px-5 py-3 font-mono text-xs">{p.sku}</td>
                      <td className="px-5 py-3 font-medium text-slate-800">{p.name}</td>
                      <td className="px-5 py-3">{formatCurrency(p.price)}</td>
                      <td className="px-5 py-3 font-semibold">{p.stock_quantity}</td>
                      <td className="px-5 py-3">
                        <span
                          className={`badge ${
                            isOut
                              ? 'bg-red-100 text-red-700'
                              : isLow
                              ? 'bg-amber-100 text-amber-700'
                              : 'bg-emerald-100 text-emerald-700'
                          }`}
                        >
                          {isOut ? 'Out of stock' : isLow ? 'Low' : 'In stock'}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right">
                        <button
                          className="btn-secondary text-xs mr-2"
                          onClick={() => openEdit(p)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn-danger text-xs"
                          onClick={() => setConfirmDel(p)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? `Edit ${editing.name}` : 'Add Product'}
        size="md"
      >
        <ProductForm
          initial={editing}
          submitting={submitting}
          onCancel={() => setModalOpen(false)}
          onSubmit={onSubmit}
        />
      </Modal>

      <ConfirmDialog
        open={Boolean(confirmDel)}
        title="Delete product?"
        message={
          confirmDel
            ? `This will permanently delete "${confirmDel.name}". This action cannot be undone.`
            : ''
        }
        onCancel={() => setConfirmDel(null)}
        onConfirm={onDelete}
      />
    </div>
  );
}
