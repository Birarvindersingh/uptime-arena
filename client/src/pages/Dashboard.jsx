import React, { useEffect, useState, useMemo } from "react";
import { fetchSites } from "../api/api";
import SiteCard from "../components/SiteCard";
import AddSiteForm from "../components/AddSiteForm";

export default function Dashboard() {
  const [sites, setSites] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const loadSites = async () => {
    try {
      const data = await fetchSites();
      setSites(data.sort((a, b) => b.uptime - a.uptime));
    } catch (e) {
      console.error("Error loading sites:", e);
    }
  };

  useEffect(() => {
    loadSites();
    const intervalId = setInterval(loadSites, 30000);
    return () => clearInterval(intervalId);
  }, []);

  const filteredSites = useMemo(() => {
    if (!searchTerm) {
      return sites;
    }
    return sites.filter(site =>
      site.url.toLowerCase().includes(searchTerm.toLowerCase()) ||
      site.user.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [sites, searchTerm]);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header-section">
        <h1 className="dashboard-title">🚀 Uptime Arena</h1>
        <p className="dashboard-slogan">
          Monitor your site uptime like a champion!
        </p>
      </header>

      <section className="add-site-section">
        <h2 className="section-title">Add Your Site</h2>
        <AddSiteForm onRefresh={loadSites} />
      </section>

      <section className="leaderboard-section">
        <h2 className="section-title">🏆 Leaderboard</h2>
        <div className="search-bar-container"> {}
          <input
            type="text"
            placeholder="Search sites by URL or username..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-input search-input"
          />
        </div>
        {filteredSites.length === 0 && sites.length > 0 ? (
          <p className="empty-state-message">
            No sites match your search.
          </p>
        ) : filteredSites.length === 0 && sites.length === 0 ? (
          <p className="empty-state-message">
            No sites yet. Add one above to get started!
          </p>
        ) : (
          <div className="leaderboard-grid">
            {filteredSites.map((site, i) => (
              <div key={`${site.user}-${site.url}`} className="leaderboard-card-wrapper">
                <h3 className="leaderboard-rank">#{i + 1}</h3>
                <SiteCard site={site} />
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}