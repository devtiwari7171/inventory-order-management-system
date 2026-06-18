import Modal from './Modal.jsx';

export default function ConfirmDialog({
  open,
  title = 'Confirm',
  message,
  confirmText = 'Delete',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  danger = true,
}) {
  return (
    <Modal
      open={open}
      onClose={onCancel}
      title={title}
      size="sm"
      footer={
        <>
          <button className="btn-secondary" onClick={onCancel}>
            {cancelText}
          </button>
          <button
            className={danger ? 'btn-danger' : 'btn-primary'}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
        </>
      }
    >
      <p className="text-slate-600">{message}</p>
    </Modal>
  );
}
