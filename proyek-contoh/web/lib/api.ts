// Klien API. Dipanggil dari komponen server, jadi API_URL tidak dikirim ke browser.
const API_URL = process.env.API_URL ?? 'http://localhost:4000';

type Health = { status: string; time: string };

export async function getHealth(): Promise<Health | null> {
  try {
    const res = await fetch(`${API_URL}/api/health`, { cache: 'no-store' });
    if (!res.ok) return null;
    const body = (await res.json()) as { data?: Health };
    return body.data ?? null;
  } catch {
    return null;
  }
}
