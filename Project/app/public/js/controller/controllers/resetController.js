import { controllResetPass } from "../callbacks.js";

// It is a simple page with one form, so I define the EventHandler directly here
const resetBtn = document.getElementById("reset");

resetBtn.addEventListener("click", () => {
  const form = document.querySelector(".reset__form");
  const body = _getFieldData(form);
  const token = location.pathname.split("/").pop();
  controllResetPass(token, body);
});

function _getFieldData(form) {
  const fields = form.querySelectorAll("input");
  const body = {};
  for (let field of fields) {
    body[field.name] = field.value;
  }

  return body;
}
