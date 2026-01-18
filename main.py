// API adresi (otomatik olarak nereden açıldıysa orası)
const API = window.location.origin;

async function addExpense() {
  const title = document.getElementById("title").value;
  const amount = document.getElementById("amount").value;

  if (!title || !amount) {
    alert("Açıklama ve tutar giriniz");
    return;
  }

  await fetch(API + "/expense", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: title,
      amount: Number(amount)
    })
  });

  document.getElementById("title").value = "";
  document.getElementById("amount").value = "";

  loadExpenses();
}

async function loadExpenses() {
  const res = await fetch(API + "/expenses");
  const data = await res.json();

  const list = document.getElementById("list");
  list.innerHTML = "";

  data.reverse().forEach(e => {
    list.innerHTML += `
      <div class="card">
        <div>${e.title}</div>
        <div class="amount">${e.amount} ₺</div>
      </div>
    `;
  });
}

// Sayfa açılınca otomatik yükle
loadExpenses();
