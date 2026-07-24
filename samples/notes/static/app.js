const notesEl = document.getElementById("notes");
const form = document.getElementById("create");
const mcpUrl = document.getElementById("mcp-url");

mcpUrl.textContent = `${window.location.origin}/mcp`;

async function loadNotes() {
  const res = await fetch("/api/notes");
  const items = await res.json();
  notesEl.innerHTML = "";
  for (const note of items) {
    const li = document.createElement("li");
    li.id = `note-${note.id}`;
    li.innerHTML = `
      <h3></h3>
      <p class="id"></p>
      <p class="body"></p>
    `;
    li.querySelector("h3").textContent = note.title;
    li.querySelector(".id").textContent = note.id;
    li.querySelector(".body").textContent = note.body || "";
    notesEl.appendChild(li);
  }
  if (location.hash.startsWith("#note-")) {
    document.querySelector(location.hash)?.scrollIntoView({ behavior: "smooth" });
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  await fetch("/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: data.get("title"),
      body: data.get("body") || "",
    }),
  });
  form.reset();
  await loadNotes();
});

loadNotes();
