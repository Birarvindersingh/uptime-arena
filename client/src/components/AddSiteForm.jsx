import React, { useState } from "react";
import { addSite } from "../api/api";

export default function AddSiteForm({ onRefresh }) {
  const [username, setUsername] = useState("");
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState("");

  function isValidSiteUrl(url) {
    const domainPattern = /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return domainPattern.test(url.trim());
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isValidSiteUrl(url)) {
      setStatusMsg("❌ Invalid URL format");
      setTimeout(() => setStatusMsg(""), 3000);
      return;
    }

    setLoading(true);
    setStatusMsg("");
    try {
      await addSite(username, url);
      setStatusMsg("✅ Added!");
      setUsername("");
      setUrl("");
      onRefresh();
    } catch (err) {
      setStatusMsg(`❌ ${err.message}`);
    } finally {
      setLoading(false);
      setTimeout(() => setStatusMsg(""), 3000);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-site-form">
      <input
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
        required
        className="form-input"
      />
      <input
        value={url}
        onChange={e => setUrl(e.target.value)}
        placeholder="Site URL (e.g. google.com)"
        required
        className="form-input"
      />
      <button type="submit" disabled={loading} className="form-button">
        {loading ? "⏳ Adding..." : "➕ Add Site"}
      </button>
      {statusMsg && <p className="form-status-message">{statusMsg}</p>}
    </form>
  );
}
