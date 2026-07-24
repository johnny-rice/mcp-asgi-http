const mcpUrl = document.getElementById("mcp-url");
const trialsEl = document.getElementById("trials");
const companiesEl = document.getElementById("companies");
const targetsEl = document.getElementById("targets");
const form = document.getElementById("search");

mcpUrl.textContent = `${window.location.origin}/mcp`;

async function loadTrials(q = "") {
  const url = q ? `/api/trials?q=${encodeURIComponent(q)}` : "/api/trials";
  const trials = await fetch(url).then((r) => r.json());
  trialsEl.innerHTML = "";
  for (const t of trials) {
    const li = document.createElement("li");
    li.id = `trial-${t.id}`;
    li.innerHTML = `<h3></h3><p class="meta"></p><p class="muted"></p>`;
    li.querySelector("h3").textContent = `${t.title} (${t.id})`;
    li.querySelector(".meta").textContent =
      `${t.phase} · ${t.status} · ${t.condition} · ${t.start_date}`;
    li.querySelector(".muted").textContent = t.summary;
    trialsEl.appendChild(li);
  }
  if (location.hash.startsWith("#trial-")) {
    document.querySelector(location.hash)?.scrollIntoView({ behavior: "smooth" });
  }
}

async function loadMeta() {
  const [companies, targets] = await Promise.all([
    fetch("/api/companies").then((r) => r.json()),
    fetch("/api/targets").then((r) => r.json()),
  ]);

  companiesEl.innerHTML = "";
  for (const c of companies) {
    const li = document.createElement("li");
    li.id = `company-${c.id}`;
    li.innerHTML = `<h3></h3><p class="meta"></p>`;
    li.querySelector("h3").textContent = `${c.name} (${c.id})`;
    li.querySelector(".meta").textContent = `${c.hq} · ${c.focus.join(", ")}`;
    companiesEl.appendChild(li);
  }

  targetsEl.innerHTML = "";
  for (const t of targets) {
    const li = document.createElement("li");
    li.id = `target-${t.id}`;
    li.innerHTML = `<h3></h3><p class="meta"></p>`;
    li.querySelector("h3").textContent = `${t.symbol} — ${t.name}`;
    li.querySelector(".meta").textContent = t.modality_fit.join(", ");
    targetsEl.appendChild(li);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const q = new FormData(form).get("q") || "";
  await loadTrials(String(q));
});

loadTrials();
loadMeta();
