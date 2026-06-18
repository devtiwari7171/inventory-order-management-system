import { useEffect, useState } from 'react';

export default function CustomerForm({ initial, submitting, onCancel, onSubmit }) {
  const [values, setValues] = useState({ name: '', email: '', phone: '' });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initial) {
      setValues({
        name: initial.name ?? '',
        email: initial.email ?? '',
        phone: initial.phone ?? '',
      });
    } else {
      setValues({ name: '', email: '', phone: '' });
    }
    setErrors({});
  }, [initial]);

  const set = (k, v) => setValues((p) => ({ ...p, [k]: v }));

  const validate = () => {
    const errs = {};
    if (!values.name.trim()) errs.name = 'Name is required';
    if (!values.email.trim()) errs.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email))
      errs.email = 'Enter a valid email';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    onSubmit({
      name: values.name.trim(),
      email: values.email.trim(),
      phone: values.phone.trim() || null,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="label">Name</label>
        <input
          className="input"
          value={values.name}
          onChange={(e) => set('name', e.target.value)}
          placeholder="Jane Doe"
          autoFocus
        />
        {errors.name && <p className="text-xs text-red-600 mt-1">{errors.name}</p>}
      </div>
      <div>
        <label className="label">Email</label>
        <input
          className="input"
          type="email"
          value={values.email}
          onChange={(e) => set('email', e.target.value)}
          placeholder="jane@example.com"
        />
        {errors.email && <p className="text-xs text-red-600 mt-1">{errors.email}</p>}
      </div>
      <div>
        <label className="label">Phone (optional)</label>
        <input
          className="input"
          value={values.phone}
          onChange={(e) => set('phone', e.target.value)}
          placeholder="555-123-4567"
        />
      </div>
      <div className="flex justify-end gap-2 pt-4 border-t border-slate-200">
        <button type="button" className="btn-secondary" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? 'Saving…' : initial ? 'Save changes' : 'Add customer'}
        </button>
      </div>
    </form>
  );
}
