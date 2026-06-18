import { useCallback, useEffect, useState } from 'react';
import { customerService } from '../services/customerService';
import { useDebounce } from './useDebounce';

export function useCustomers(initialQuery = '') {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState(initialQuery);

  const debouncedQuery = useDebounce(query, 300);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await customerService.list({ q: debouncedQuery });
      setItems(data.items);
      setTotal(data.total);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  }, [debouncedQuery]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { items, total, loading, error, query, setQuery, refresh: fetch };
}
