import { controllUpdateResource } from "../callbacks.js";

// It is a simple page with one form, so I define the EventHandler directly here
const updateBtn = document.getElementById("update");

updateBtn.addEventListener("click", () => {
  const form = document.querySelector(".user__form");
  const body = _getFieldData(form);
  controllUpdateResource("me", undefined, body);
});

function _getFieldData(form) {
  const fields = form.querySelectorAll("input");
  const body = {};
  for (let field of fields) {
    body[field.name] = field.value;
  }

  return body;
}
