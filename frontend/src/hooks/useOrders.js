import { useCallback, useEffect, useState } from 'react';
import { orderService } from '../services/orderService';

export function useOrders() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await orderService.list();
      setItems(data.items);
      setTotal(data.total);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { items, total, loading, error, refresh: fetch };
}
