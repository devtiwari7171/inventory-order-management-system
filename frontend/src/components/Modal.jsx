import { useEffect } from 'react';

/**
 * Reusable modal dialog. Closes on backdrop click or Escape.
 */
export default function Modal({ open, onClose, title, children, footer, size = 'md' }) {
  useEffect(() => {
    if (!open) return undefined;
    const onKey = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open) return null;

  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
  };

  return (
    <div
      className="fixed inset-0 z-50 bg-slate-900/50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className={`bg-white rounded-xl shadow-xl w-full ${sizes[size]} max-h-[90vh] flex flex-col`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 text-2xl leading-none"
            aria-label="Close"
          >
            ×
          </button>
        </div>
        <div className="p-5 overflow-y-auto">{children}</div>
        {footer && (
          <div className="p-4 border-t border-slate-200 flex justify-end gap-2 bg-slate-50 rounded-b-xl">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
