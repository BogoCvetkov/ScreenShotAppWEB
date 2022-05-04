import { HTMlMarkup } from "./markup.js";

export class Utils {
  static createNewMessage(response) {
    const newMsg = document.createElement("div");
    newMsg.classList.add(
      "message--container",
      response.status === "success" ? "msg--success" : "msg--fail"
    );
    const msg = document.createElement("p");
    msg.textContent = response.msg;
    newMsg.append(msg);
    return newMsg;
  }
}
