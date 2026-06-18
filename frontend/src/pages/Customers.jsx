import { useState } from 'react';
import toast from 'react-hot-toast';
import Spinner from '../components/Spinner.jsx';
import Modal from '../components/Modal.jsx';
import ConfirmDialog from '../components/ConfirmDialog.jsx';
import CustomerForm from '../components/CustomerForm.jsx';
import { useCustomers } from '../hooks/useCustomers';
import { customerService } from '../services/customerService';
import { formatDate } from '../utils/formatters';

export default function Customers() {
  const { items, total, loading, error, query, setQuery, refresh } = useCustomers();
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [confirmDel, setConfirmDel] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const openCreate = () => {
    setEditing(null);
    setModalOpen(true);
  };
  const openEdit = (c) => {
    setEditing(c);
    setModalOpen(true);
  };

  const onSubmit = async (values) => {
    setSubmitting(true);
    try {
      if (editing) {
        await customerService.update(editing.id, values);
        toast.success(`Updated ${values.name}`);
      } else {
        await customerService.create(values);
        toast.success(`Added ${values.name}`);
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
      await customerService.remove(confirmDel.id);
      toast.success(`Deleted ${confirmDel.name}`);
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
          <h2 className="text-2xl font-bold text-slate-800">Customers</h2>
          <p className="text-sm text-slate-500 mt-1">
            {total} {total === 1 ? 'customer' : 'customers'}
          </p>
        </div>
        <button className="btn-primary" onClick={openCreate}>
          + Add Customer
        </button>
      </div>

      <div className="card p-4">
        <input
          className="input max-w-md"
          placeholder="Search by name or email…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <Spinner label="Loading customers…" />
      ) : error ? (
        <div className="card p-6 border-red-200 bg-red-50">
          <p className="text-red-700">{error.message}</p>
        </div>
      ) : items.length === 0 ? (
        <div className="card p-12 text-center text-slate-500">
          <p className="text-lg">No customers found</p>
          <p className="text-sm mt-1">Add your first customer to start taking orders.</p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600 text-left">
                <tr>
                  <th className="px-5 py-3 font-medium">Name</th>
                  <th className="px-5 py-3 font-medium">Email</th>
                  <th className="px-5 py-3 font-medium">Phone</th>
                  <th className="px-5 py-3 font-medium">Created</th>
                  <th className="px-5 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50">
                    <td className="px-5 py-3 font-medium text-slate-800">{c.name}</td>
                    <td className="px-5 py-3 text-slate-600">{c.email}</td>
                    <td className="px-5 py-3 text-slate-600">{c.phone || '—'}</td>
                    <td className="px-5 py-3 text-slate-500 text-xs">
                      {formatDate(c.created_at)}
                    </td>
                    <td className="px-5 py-3 text-right">
                      <button
                        className="btn-secondary text-xs mr-2"
                        onClick={() => openEdit(c)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn-danger text-xs"
                        onClick={() => setConfirmDel(c)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? `Edit ${editing.name}` : 'Add Customer'}
        size="md"
      >
        <CustomerForm
          initial={editing}
          submitting={submitting}
          onCancel={() => setModalOpen(false)}
          onSubmit={onSubmit}
        />
      </Modal>

      <ConfirmDialog
        open={Boolean(confirmDel)}
        title="Delete customer?"
        message={
          confirmDel
            ? `This will permanently delete "${confirmDel.name}". Customers with order history cannot be deleted.`
            : ''
        }
        onCancel={() => setConfirmDel(null)}
        onConfirm={onDelete}
      />
    </div>
  );
}
