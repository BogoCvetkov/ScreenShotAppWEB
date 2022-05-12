import { controllAuth } from "../callbacks.js";

// It is a simple page with one form, so I define the EventHandler directly here
const loginBtn = document.getElementById("login");
const forgetBtn = document.getElementById("forget");
const sendBtn = document.getElementById("sendReset");

loginBtn.addEventListener("click", () => {
  const form = document.querySelector(".login__form");
  const body = _getFieldData(form);
  controllAuth("login", body);
});

forgetBtn.addEventListener("click", () => {
  const logForm = document.querySelector(".login--form--wrapper");
  const forgetForm = document.querySelector(".forget--form--wrapper");
  logForm.classList.add("hidden");
  forgetForm.classList.remove("hidden");
});

sendBtn.addEventListener("click", () => {
  const form = document.querySelector(".forget__form");
  const body = _getFieldData(form);
  controllAuth("forgetPass", body).then(() => {
    const logForm = document.querySelector(".login--form--wrapper");
    const forgetForm = document.querySelector(
      ".forget--form--wrapper"
    );
    logForm.classList.remove("hidden");
    forgetForm.classList.add("hidden");
  });
});

function _getFieldData(form) {
  const fields = form.querySelectorAll("input");
  const body = {};
  for (let field of fields) {
    body[field.name] = field.value;
  }

  return body;
}
