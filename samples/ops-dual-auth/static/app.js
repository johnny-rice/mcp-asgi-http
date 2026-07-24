const mcpUrl = document.getElementById("mcp-url");
const jwtStatus = document.getElementById("jwt-status");
const servicesEl = document.getElementById("services");
const deploysEl = document.getElementById("deploys");
const freezesEl = document.getElementById("freezes");

mcpUrl.textContent = `${window.location.origin}/mcp`;

function badge(status) {
  const cls = status === "healthy" ? "healthy" : status === "degraded" ? "degraded" : "";
  return `<span class="badge ${cls}">${status}</span>`;
}

async function load() {
  const [cfg, services, deploys, freezes] = await Promise.all([
    fetch("/api/config").then((r) => r.json()),
    fetch("/api/services").then((r) => r.json()),
    fetch("/api/deploys").then((r) => r.json()),
    fetch("/api/freeze-windows").then((r) => r.json()),
  ]);

  jwtStatus.textContent = cfg.jwt_configured
    ? "JWT path enabled (issuer/audience/JWKS configured)"
    : "JWT path not configured (API key only until JWT_* is set)";

  servicesEl.innerHTML = "";
  for (const svc of services) {
    const freeze = await fetch(`/api/services/${svc.id}/freeze`).then((r) => r.json());
    const li = document.createElement("li");
    li.id = `service-${svc.id}`;
    li.innerHTML = `
      <h3></h3>
      <p class="meta"></p>
      <p class="muted freeze"></p>
    `;
    li.querySelector("h3").textContent = `${svc.name} (${svc.id})`;
    li.querySelector(".meta").innerHTML = [
      badge(svc.status),
      `<span>owner ${svc.owner}</span>`,
      `<span>${svc.env}</span>`,
      `<span>v${svc.version}</span>`,
    ].join("");
    li.querySelector(".freeze").textContent = freeze.message;
    servicesEl.appendChild(li);
  }

  deploysEl.innerHTML = "";
  for (const d of deploys) {
    const li = document.createElement("li");
    li.innerHTML = `<h3></h3><p class="meta"></p>`;
    li.querySelector("h3").textContent = `${d.id} → ${d.service_id}`;
    li.querySelector(".meta").textContent =
      `${d.status} · v${d.version} · ${d.actor} · ${d.deployed_at}`;
    deploysEl.appendChild(li);
  }

  freezesEl.innerHTML = "";
  for (const fz of freezes) {
    const li = document.createElement("li");
    li.innerHTML = `<h3></h3><p class="meta"></p>`;
    li.querySelector("h3").innerHTML =
      `${fz.name} <span class="badge ${fz.active ? "active" : "idle"}">${fz.active ? "active" : "scheduled"}</span>`;
    li.querySelector(".meta").textContent =
      `${fz.starts_at} → ${fz.ends_at} · ${fz.applies_to.join(", ")}`;
    freezesEl.appendChild(li);
  }

  if (location.hash.startsWith("#service-")) {
    document.querySelector(location.hash)?.scrollIntoView({ behavior: "smooth" });
  }
}

load();
