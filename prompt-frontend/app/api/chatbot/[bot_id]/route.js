export default function handler(req, res) {
  const { bot_id } = req.query;

  // Validate bot_id
  if (!bot_id) {
    return res.status(400).send("Missing bot_id");
  }

  // Serve JavaScript dynamically
  const script = `
      (function() {
        console.log("Chatbot initialized for bot_id: ${bot_id}");
        const botWidget = document.createElement('div');
        botWidget.innerHTML = '<p>Chatbot Loaded for ID: ${bot_id}</p>';
        document.body.appendChild(botWidget);
      })();
    `;

  res.setHeader("Content-Type", "application/javascript");
  res.send(script);
}
