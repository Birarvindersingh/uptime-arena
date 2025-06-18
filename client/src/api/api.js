const BASE_URL = "http://localhost:5000";

export async function fetchSites() {
    const res = await fetch(`${BASE_URL}/api/sites`);
    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
    }
    return res.json();
}

export async function addSite(username, url) {
    const res = await fetch(`${BASE_URL}/api/sites`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, url }),
    });
    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
    }
    return res.json();
}