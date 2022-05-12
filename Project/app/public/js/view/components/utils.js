import { HTMlMarkup } from "./markup.js";

export class Utils {
  static createNewMessage(status, message) {
    const newMsg = document.createElement("div");
    newMsg.classList.add(
      "message--container",
      status === "success" ? "msg--success" : "msg--fail"
    );
    const msg = document.createElement("p");
    msg.textContent = message;
    newMsg.append(msg);
    return newMsg;
  }

  // Creating an element this way, allows it to be referenced
  // Each window needs to be deleted individually
  static generateProcessWindow() {
    const newProcWin = document.createElement("div");
    newProcWin.className = "loading--screen";
    newProcWin.innerHTML = `<h2> Processing</h2>
    <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>`;
    return newProcWin;
  }

  static generateConfirmWindow(msg) {
    document.body.insertAdjacentHTML(
      "beforeend",
      HTMlMarkup.createConfirmWindow(msg)
    );
  }
}
