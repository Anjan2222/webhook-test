async function fetchEvents() {
  const res = await fetch('/events');
  const events = await res.json();
  const list = document.getElementById('events-list');
  list.innerHTML = '';
  events.forEach(ev => {
    let text = '';
    if (ev.action_type === "PUSH") {
      text = `"${ev.author}" pushed to "${ev.to_branch}" on ${ev.timestamp}`;
    } else if (ev.action_type === "PULL_REQUEST") {
      text = `"${ev.author}" submitted a pull request from "${ev.from_branch}" to "${ev.to_branch}" on ${ev.timestamp}`;
    } else if (ev.action_type === "MERGE") {
      text = `"${ev.author}" merged branch "${ev.from_branch}" to "${ev.to_branch}" on ${ev.timestamp}`;
    }
    const li = document.createElement('li');
    li.textContent = text;
    list.appendChild(li);
  });
}
fetchEvents();
setInterval(fetchEvents, 15000);