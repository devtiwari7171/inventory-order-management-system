import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';
import ConfirmDialog from '../components/ConfirmDialog.jsx';
import OrderForm from '../components/OrderForm.jsx';
import { orderService } from '../services/orderService';
import { customerService } from '../services/customerService';
import { productService } from '../services/productService';
import { useOrders } from '../hooks/useOrders';
import { formatCurrency, formatDate } from '../utils/formatters';

export default function Orders() {
  const { items, total, loading, error, refresh } = useOrders();
  const [modalOpen, setModalOpen] = useState(false);
  const [viewing, setViewing] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [loadingForm, setLoadingForm] = useState(false);
  const [confirmCancel, setConfirmCancel] = useState(null);

  const openCreate = async () => {
    setLoadingForm(true);
    setModalOpen(true);
    try {
      const [c, p] = await Promise.all([
        customerService.list({ limit: 200 }),
        productService.list({ limit: 200 }),
      ]);
      setCustomers(c.items);
      setProducts(p.items);
    } catch (e) {
      toast.error(e.message || 'Failed to load form data');
      setModalOpen(false);
    } finally {
      setLoadingForm(false);
    }
  };

  const onSubmit = async (payload) => {
    setSubmitting(true);
    try {
      const created = await orderService.create(payload);
      toast.success(`Order #${created.id} created for ${formatCurrency(created.total_amount)}`);
      setModalOpen(false);
      await refresh();
    } catch (e) {
      toast.error(e.message || 'Failed to create order');
    } finally {
      setSubmitting(false);
    }
  };

  useEffect(() => {
    if (viewing) {
      orderService.get(viewing.id).then(setViewing).catch(() => {});
    }
  }, [viewing]);

  const onCancelOrder = async () => {
    if (!confirmCancel) return;
    try {
      await orderService.remove(confirmCancel.id);
      toast.success(`Order #${confirmCancel.id} cancelled — stock restored`);
      setConfirmCancel(null);
      if (viewing?.id === confirmCancel.id) setViewing(null);
      await refresh();
    } catch (e) {
      toast.error(e.message || 'Failed to cancel order');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Orders</h2>
          <p className="text-sm text-slate-500 mt-1">
            {total} {total === 1 ? 'order' : 'orders'} in history
          </p>
        </div>
        <button className="btn-primary" onClick={openCreate}>
          + Create Order
        </button>
      </div>

      {loading ? (
        <Spinner label="Loading orders…" />
      ) : error ? (
        <div className="card p-6 border-red-200 bg-red-50">
          <p className="text-red-700">{error.message}</p>
        </div>
      ) : items.length === 0 ? (
        <div className="card p-12 text-center text-slate-500">
          <p className="text-lg">No orders yet</p>
          <p className="text-sm mt-1">Create your first order to get started.</p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600 text-left">
                <tr>
                  <th className="px-5 py-3 font-medium">Order #</th>
                  <th className="px-5 py-3 font-medium">Customer</th>
                  <th className="px-5 py-3 font-medium">Items</th>
                  <th className="px-5 py-3 font-medium">Total</th>
                  <th className="px-5 py-3 font-medium">Created</th>
                  <th className="px-5 py-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((o) => (
                  <tr key={o.id} className="hover:bg-slate-50">
                    <td className="px-5 py-3 font-mono">#{o.id}</td>
                    <td className="px-5 py-3 text-slate-800">
                      Customer #{o.customer_id}
                    </td>
                    <td className="px-5 py-3">{o.items?.length ?? 0}</td>
                    <td className="px-5 py-3 font-semibold">
                      {formatCurrency(o.total_amount)}
                    </td>
                    <td className="px-5 py-3 text-xs text-slate-500">
                      {formatDate(o.created_at)}
                    </td>
                    <td className="px-5 py-3 text-right">
                      <button
                        className="btn-secondary text-xs mr-2"
                        onClick={() => setViewing(o)}
                      >
                        View
                      </button>
                      <button
                        className="btn-danger text-xs"
                        onClick={() => setConfirmCancel(o)}
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create order modal */}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Create Order"
        size="xl"
      >
        {loadingForm ? (
          <Spinner label="Loading customers & products…" />
        ) : (
          <OrderForm
            customers={customers}
            products={products}
            submitting={submitting}
            onCancel={() => setModalOpen(false)}
            onSubmit={onSubmit}
          />
        )}
      </Modal>

      {/* Order details modal */}
      <Modal
        open={Boolean(viewing)}
        onClose={() => setViewing(null)}
        title={viewing ? `Order #${viewing.id}` : 'Order'}
        size="lg"
      >
        {viewing && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-slate-500">Customer ID</p>
                <p className="font-medium text-slate-800">#{viewing.customer_id}</p>
              </div>
              <div>
                <p className="text-slate-500">Created</p>
                <p className="font-medium text-slate-800">{formatDate(viewing.created_at)}</p>
              </div>
              <div className="col-span-2">
                <p className="text-slate-500">Total</p>
                <p className="text-2xl font-bold text-brand-700">
                  {formatCurrency(viewing.total_amount)}
                </p>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-slate-800 mb-2">Items</h4>
              <div className="border border-slate-200 rounded-lg overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-slate-50 text-slate-600 text-left">
                    <tr>
                      <th className="px-4 py-2 font-medium">Product</th>
                      <th className="px-4 py-2 font-medium">Qty</th>
                      <th className="px-4 py-2 font-medium">Unit</th>
                      <th className="px-4 py-2 font-medium text-right">Subtotal</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {viewing.items.map((it) => (
                      <tr key={it.id}>
                        <td className="px-4 py-2">#{it.product_id}</td>
                        <td className="px-4 py-2">{it.quantity}</td>
                        <td className="px-4 py-2">{formatCurrency(it.unit_price)}</td>
                        <td className="px-4 py-2 text-right font-medium">
                          {formatCurrency(it.subtotal)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </Modal>

      <ConfirmDialog
        open={Boolean(confirmCancel)}
        title="Cancel order?"
        message={
          confirmCancel
            ? `Cancelling Order #${confirmCancel.id} will restore the stock of all items back to inventory. This action cannot be undone.`
            : ''
        }
        confirmText="Cancel order"
        onCancel={() => setConfirmCancel(null)}
        onConfirm={onCancelOrder}
      />
    </div>
  );
}
