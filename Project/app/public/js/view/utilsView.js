import { Utils } from "./components/utils.js";

export class UtilsView {
  static showMessage(response) {
    let message;
    response.msg instanceof Array
      ? (message = `${response.msg[0].field} - ${response.msg[0].info[0]}`)
      : (message = response.msg);

    const msg = Utils.createNewMessage(response.status, message);
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
    document.body.prepend(win);
    return win;
  }

  static removeProcessWindow(win) {
    win.remove();
  }
}
