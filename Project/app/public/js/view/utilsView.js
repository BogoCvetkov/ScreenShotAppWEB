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

  static showConfirmWindow(msg) {
    Utils.generateConfirmWindow(msg);
  }

  static showProcessWindow() {
    const win = Utils.generateProcessWindow();
    document.body.append(win);
    return win;
  }

  static removeProcessWindow(win) {
    win.remove();
  }
}
