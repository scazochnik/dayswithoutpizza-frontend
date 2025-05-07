document.addEventListener("DOMContentLoaded", () => {
  const tg = window.Telegram.WebApp;
  tg.expand();

  const user_id = tg.initDataUnsafe?.user?.id || 0;

  fetch("https://dayswithoutpizza-backend.onrender.com/get_user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("score").innerText = `Очки: ${data.points}`;
    });

  window.answerQuiz = function () {
    fetch("https://dayswithoutpizza-backend.onrender.com/quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id })
    })
      .then(res => res.json())
      .then(data => alert(data.message));
  };

  window.inviteFriend = function () {
    fetch("https://dayswithoutpizza-backend.onrender.com/invite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id })
    })
      .then(res => res.json())
      .then(data => alert(data.message));
  };
});
