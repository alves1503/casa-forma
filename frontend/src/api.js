const API_BASE = (
  import.meta.env.VITE_API_URL
  || (import.meta.env.DEV ? "" : window.location.origin)
).replace(/\/$/, "");

export function imageUrl(path) {
  if (!path) return "";
  return path.startsWith("http://") || path.startsWith("https://")
    ? path
    : `${API_BASE}${path}`;
}

function authorizationHeader(credentials) {
  const encoded = new TextEncoder().encode(`${credentials.username}:${credentials.password}`);
  const binary = Array.from(encoded, (byte) => String.fromCharCode(byte)).join("");
  return `Basic ${btoa(binary)}`;
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, options);
  } catch {
    throw new Error("Não foi possível conectar à API. Verifique se o servidor está funcionando.");
  }

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = body.detail || body.error || "Ocorreu um erro. Tente novamente.";
    throw new Error(typeof message === "string" ? message : "Ocorreu um erro. Tente novamente.");
  }
  return body;
}

export function getFurniture() {
  return request("/api/furniture");
}

export function generatePreview(photo, furnitureId) {
  const form = new FormData();
  form.append("room_photo", photo);
  form.append("furniture_id", furnitureId);
  return request("/api/preview", { method: "POST", body: form });
}

export function adminLogin(credentials) {
  return request("/api/admin/session", {
    headers: { Authorization: authorizationHeader(credentials) },
  });
}

export function getAdminFurniture(credentials) {
  return request("/api/admin/furniture", {
    headers: { Authorization: authorizationHeader(credentials) },
  });
}

export function uploadFurniturePhoto(credentials, furnitureId, photo) {
  const form = new FormData();
  form.append("photo", photo);
  return request(`/api/admin/furniture/${encodeURIComponent(furnitureId)}/photo`, {
    method: "POST",
    headers: { Authorization: authorizationHeader(credentials) },
    body: form,
  });
}

export { API_BASE };
