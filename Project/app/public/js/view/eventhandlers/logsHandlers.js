import { LogsView } from "../logsView.js";

export class LogsEventHandler {
  static searchBtn = document.querySelector(".btn--search");

  static getAllLogsHandler(handler) {
    this.searchBtn.addEventListener("click", () => {
      const param = document.getElementById("logsParams");
      const term = document.querySelector(".search_logs input");
      const query = `${param.value}=${term.value}&sort=desc,date`;
      console.log(query);
      handler(query);
    });
  }
}
