import { useEffect, useState } from "react";
import { getFurniture } from "./api";

export function useFurniture() {
  const [furniture, setFurniture] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    getFurniture()
      .then((items) => { if (active) setFurniture(items); })
      .catch((requestError) => { if (active) setError(requestError.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  return { furniture, loading, error };
}
