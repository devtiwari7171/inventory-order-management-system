import { useMemo, useState } from 'react';
import { formatCurrency } from '../utils/formatters';

/**
 * Order create form.
 *
 * Props:
 *  - customers: CustomerResponse[]
 *  - products:  ProductResponse[]
 *  - submitting: bool
 *  - onCancel, onSubmit(payload)
 */
export default function OrderForm({ customers, products, submitting, onCancel, onSubmit }) {
  const [customerId, setCustomerId] = useState('');
  const [lines, setLines] = useState([{ productId: '', quantity: 1 }]);

  const productById = useMemo(() => {
    const map = {};
    products.forEach((p) => {
      map[String(p.id)] = p;
    });
    return map;
  }, [products]);

  const updateLine = (idx, patch) => {
    setLines((arr) => arr.map((l, i) => (i === idx ? { ...l, ...patch } : l)));
  };

  const addLine = () => setLines((arr) => [...arr, { productId: '', quantity: 1 }]);
  const removeLine = (idx) => setLines((arr) => arr.filter((_, i) => i !== idx));

  const total = lines.reduce((acc, l) => {
    const p = productById[String(l.productId)];
    if (!p) return acc;
    const qty = Math.max(0, Number(l.quantity) || 0);
    return acc + Number(p.price) * qty;
  }, 0);

  const hasStockIssue = lines.some((l) => {
    const p = productById[String(l.productId)];
    if (!p) return false;
    return Number(l.quantity) > p.stock_quantity;
  });

  const submit = (e) => {
    e.preventDefault();
    if (!customerId || lines.some((l) => !l.productId || Number(l.quantity) < 1)) return;
    onSubmit({
      customer_id: Number(customerId),
      items: lines.map((l) => ({
        product_id: Number(l.productId),
        quantity: Number(l.quantity),
      })),
    });
  };

  return (
    <form onSubmit={submit} className="space-y-4">
      <div>
        <label className="label">Customer</label>
        <select
          className="input"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
        >
          <option value="">— Select customer —</option>
          {customers.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name} ({c.email})
            </option>
          ))}
        </select>
        {customers.length === 0 && (
          <p className="text-xs text-amber-600 mt-1">
            No customers yet. Add a customer first.
          </p>
        )}
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="label !mb-0">Products</label>
          <button type="button" className="btn-secondary text-xs" onClick={addLine}>
            + Add line
          </button>
        </div>

        <div className="space-y-2">
          {lines.map((line, idx) => {
            const p = productById[String(line.productId)];
            const stockIssue =
              p && Number(line.quantity) > p.stock_quantity;
            return (
              <div
                key={idx}
                className="grid grid-cols-12 gap-2 items-end p-3 rounded-lg border border-slate-200"
              >
                <div className="col-span-7">
                  <label className="label text-xs">Product</label>
                  <select
                    className="input"
                    value={line.productId}
                    onChange={(e) => updateLine(idx, { productId: e.target.value })}
                  >
                    <option value="">— Select product —</option>
                    {products.map((p) => (
                      <option
                        key={p.id}
                        value={p.id}
                        disabled={p.stock_quantity === 0}
                      >
                        {p.name} · {p.sku} · stock {p.stock_quantity} · {formatCurrency(p.price)}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="col-span-3">
                  <label className="label text-xs">Quantity</label>
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={line.quantity}
                    onChange={(e) =>
                      updateLine(idx, { quantity: Math.max(1, Number(e.target.value) || 1) })
                    }
                  />
                </div>
                <div className="col-span-2 flex items-end">
                  <button
                    type="button"
                    className="btn-danger text-xs w-full"
                    onClick={() => removeLine(idx)}
                    disabled={lines.length === 1}
                  >
                    Remove
                  </button>
                </div>
                {p && (
                  <div className="col-span-12 text-xs text-slate-500">
                    Subtotal: {formatCurrency(Number(p.price) * Number(line.quantity))}
                    {stockIssue && (
                      <span className="ml-2 text-red-600 font-medium">
                        ⚠ Only {p.stock_quantity} in stock
                      </span>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
        <span className="text-sm font-medium text-slate-700">Order Total</span>
        <span className="text-xl font-bold text-brand-700">{formatCurrency(total)}</span>
      </div>

      {hasStockIssue && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
          One or more lines exceed available stock. Adjust quantities before placing the order.
        </p>
      )}

      <div className="flex justify-end gap-2 pt-2 border-t border-slate-200">
        <button type="button" className="btn-secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
        <button
          type="submit"
          className="btn-primary"
          disabled={submitting || !customerId || hasStockIssue}
        >
          {submitting ? 'Placing order…' : 'Place order'}
        </button>
      </div>
    </form>
  );
}
