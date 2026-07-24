async function load() {
  const res = await fetch("/api/items");
  const items = await res.json();
  const root = document.getElementById("items");
  root.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.id = `item-${item.id}`;
    li.innerHTML = `
      <span class="name"></span>
      <span class="price"></span>
      <span class="meta"></span>
    `;
    li.querySelector(".name").textContent = item.name;
    li.querySelector(".price").textContent = `$${(item.price_cents / 100).toFixed(2)}`;
    li.querySelector(".meta").textContent = `id ${item.id}`;
    root.appendChild(li);
  }
  if (location.hash.startsWith("#item-")) {
    document.querySelector(location.hash)?.scrollIntoView({ behavior: "smooth" });
  }
}

load();
