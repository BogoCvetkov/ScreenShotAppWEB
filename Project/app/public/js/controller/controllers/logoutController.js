import { controllLogOut } from "../callbacks.js";
const logoutBtn = document.getElementById("logout");

logoutBtn.addEventListener("click", () => {
  controllLogOut();
});
