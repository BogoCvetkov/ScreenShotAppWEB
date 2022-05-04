import { Utils } from "./components/utils.js";

export class UtilsView {
  static showMessage(response) {
    const msg = Utils.createNewMessage(response);
    document.body.append(msg);
    return msg;
  }

  static removeMsg(msg) {
    msg.remove();
  }
}
