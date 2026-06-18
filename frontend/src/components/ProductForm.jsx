import { useEffect, useState } from 'react';

/**
 * Product create/edit form. Receives `initial` (existing product or null),
 * `submitting` (bool), `onCancel`, `onSubmit(payload)`.
 */
export default function ProductForm({ initial, submitting, onCancel, onSubmit }) {
  const [values, setValues] = useState({
    name: '',
    sku: '',
    price: '',
    stock_quantity: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initial) {
      setValues({
        name: initial.name ?? '',
        sku: initial.sku ?? '',
        price: initial.price ?? '',
        stock_quantity: initial.stock_quantity ?? '',
      });
    } else {
      setValues({ name: '', sku: '', price: '', stock_quantity: '' });
    }
    setErrors({});
  }, [initial]);

  const set = (k, v) => setValues((prev) => ({ ...prev, [k]: v }));

  const validate = () => {
    const errs = {};
    if (!values.name.trim()) errs.name = 'Name is required';
    if (!values.sku.trim()) errs.sku = 'SKU is required';
    const priceNum = Number(values.price);
    if (values.price === '' || Number.isNaN(priceNum)) errs.price = 'Price is required';
    else if (priceNum < 0) errs.price = 'Price cannot be negative';
    const stockNum = Number(values.stock_quantity);
    if (values.stock_quantity === '' || Number.isNaN(stockNum)) errs.stock_quantity = 'Stock is required';
    else if (!Number.isInteger(stockNum) || stockNum < 0) errs.stock_quantity = 'Stock must be a non-negative integer';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="label">Name</label>
        <input
          className="input"
          value={values.name}
          onChange={(e) => set('name', e.target.value)}
          placeholder="e.g. Mechanical Keyboard"
          autoFocus
        />
        {errors.name && <p className="text-xs text-red-600 mt-1">{errors.name}</p>}
      </div>

      <div>
        <label className="label">SKU</label>
        <input
          className="input"
          value={values.sku}
          onChange={(e) => set('sku', e.target.value)}
          placeholder="e.g. KB-001"
        />
        {errors.sku && <p className="text-xs text-red-600 mt-1">{errors.sku}</p>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Price (USD)</label>
          <input
            className="input"
            type="number"
            step="0.01"
            min="0"
            value={values.price}
            onChange={(e) => set('price', e.target.value)}
            placeholder="0.00"
          />
          {errors.price && <p className="text-xs text-red-600 mt-1">{errors.price}</p>}
        </div>
        <div>
          <label className="label">Stock Qty</label>
          <input
            className="input"
            type="number"
            step="1"
            min="0"
            value={values.stock_quantity}
            onChange={(e) => set('stock_quantity', e.target.value)}
            placeholder="0"
          />
          {errors.stock_quantity && (
            <p className="text-xs text-red-600 mt-1">{errors.stock_quantity}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4 border-t border-slate-200">
        <button type="button" className="btn-secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Create product'}
        </button>
      </div>
    </form>
  );
}
