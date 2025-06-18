const SiteCard = ({ site }) => {
  const { user: username, url, uptime } = site;

  const getInitials = (name) => {
    if (!name) return "?";
    return name
      .split(/\s+/)
      .filter(Boolean)
      .map((w) => w[0]?.toUpperCase())
      .join("")
      .slice(0, 2);
  };

  let badge = "❌",
      progressClass = "progress-red",
      uptimeTextColorClass = "text-red";

  if (typeof uptime === "number") {
    if (uptime >= 90) {
      badge = "✅";
      progressClass = "progress-green";
      uptimeTextColorClass = "text-green";
    } else if (uptime >= 50) {
      badge = "⚠️";
      progressClass = "progress-yellow";
      uptimeTextColorClass = "text-yellow";
    }
  }

  return (
    <div className="site-card">
      <div className="site-card-header">
        <div className="site-avatar">{getInitials(username)}</div>
        <h2 className="site-url" title={url}>{url}</h2>
      </div>

      <p className="site-details">
        <span className="icon">👤</span>
        <span className="site-username">@{username || "N/A"}</span>
        <span className="site-badge">{badge}</span>
      </p>

      <div className="site-uptime-section">
        <div className="site-uptime-info">
          <span className="uptime-label">Uptime</span>
          <span className={`uptime-percentage ${uptimeTextColorClass}`}>
            {typeof uptime === "number" ? `${uptime.toFixed(1)}%` : "?%"}
          </span>
        </div>
        <div className="progress-bar-container">
          <div
            className={`progress-bar ${progressClass}`}
            style={{
              width: `${typeof uptime === "number" ? uptime : 0}%`
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default SiteCard;