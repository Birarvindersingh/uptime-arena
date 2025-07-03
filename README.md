<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>

  <h1>🎮 Uptime Arena – Gamified Website Uptime Tracker</h1>

  <p>
    <strong>Uptime Arena</strong> is a full-stack cloud project that monitors website uptime and displays the results in a fun, gamified leaderboard. Built using Flask (backend) and React.js (frontend), it includes real-time uptime checks, Dockerized deployment, GitHub Actions for CI/CD, and observability tools like Prometheus and Grafana. Ideal for DevOps learners, this project demonstrates real-world cloud skills including monitoring, CI/CD, and containerization—all deployed on AWS EC2.
  </p>

  <h2>🚀 Project Highlights</h2>
  <ul>
    <li>📡 Periodic website uptime checks using Flask + Python</li>
    <li>🎨 React.js frontend with dynamic leaderboard</li>
    <li>🕹️ Gamified interface based on uptime %</li>
    <li>🐳 Dockerized full stack with Prometheus & Grafana</li>
    <li>🔄 CI/CD pipeline via GitHub Actions</li>
    <li>📈 Grafana dashboards powered by Prometheus</li>
    <li>☁️ Hosted on AWS EC2 (Ubuntu)</li>
  </ul>

  <h2>🛠️ Technologies Used</h2>
  <ul>
    <li>React.js (Frontend)</li>
    <li>Python & Flask (Backend)</li>
    <li>Docker & Docker Hub</li>
    <li>Prometheus + Grafana</li>
    <li>GitHub Actions</li>
    <li>AWS EC2 (Ubuntu)</li>
    <li>SQLite3 (Database)</li>
  </ul>

  <h2>📊 Architecture Overview</h2>
  <ul>
    <li>Flask backend checks uptime and exposes metrics via <code>/metrics</code></li>
    <li>React frontend fetches data and displays the leaderboard</li>
    <li>Prometheus scrapes Flask metrics periodically</li>
    <li>Grafana visualizes response time and availability</li>
    <li>Dockerized full stack auto-built and deployed via GitHub Actions</li>
  </ul>

  <h2>📸 Project Screenshots</h2>
  <img src="https://github.com/Birarvindersingh/uptime-arena/blob/main/screenshots/main.PNG" width="600" alt="Uptime Arena Leaderboard" />
  <br />
  <img src="https://github.com/Birarvindersingh/uptime-arena/blob/main/screenshots/docker.PNG" width="600" alt="Docker Setup Screenshot" />
  <br />
  <img src="https://github.com/Birarvindersingh/uptime-arena/blob/main/screenshots/prometheus.PNG" width="600" alt="Prometheus Dashboard" />
  <br />
  <img src="https://github.com/Birarvindersingh/uptime-arena/blob/main/screenshots/grafana.PNG" width="600" alt="Grafana Monitoring" />

  <h2>📈 Monitoring with Grafana + Prometheus</h2>
  <ul>
    <li>Prometheus scrapes metrics from Flask at <code>/metrics</code></li>
    <li>Grafana connects to Prometheus to visualize uptime and response time</li>
    <li>Dashboards include detailed trends and availability history</li>
  </ul>

  <h2>🛡️ CI/CD Pipeline</h2>
  <ul>
    <li>GitHub Actions builds and pushes the Docker image on each push</li>
    <li>Automatically deploys to AWS EC2 via SSH</li>
    <li>EC2 instance pulls the latest Docker image and runs the container automatically</li>
  </ul>

  <h2>🌐 Live Preview</h2>
  <p>App is live and accessible at:</p>
  <p>🔗 <a href="http://3.140.213.227:5000/" target="_blank">http://3.140.213.227:5000/</a></p>

  <h2>✅ Conclusion</h2>
  <p>This project demonstrates hands-on DevOps experience by combining cloud deployment, containerization, and real-time monitoring into a seamless, production-ready solution.</p>

</body>
</html>
