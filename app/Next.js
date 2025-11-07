async function sendPrompt() {
  const res = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: "Hello Gemini!" }),
  });

  const data = await res.json();
  console.log(data.text);
}
