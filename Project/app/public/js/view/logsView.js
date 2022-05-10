import { Table } from "./components/table.js";

// Contains the view for the Logs Page
export class LogsView {
  static generateAllLogsTable(data) {
    const table = document.querySelector(".all_logs--table tbody");

    table.innerHTML = "";
    for (let record of data) {
      const tr = Table.generateAllLogsRow(record);
      table.insertAdjacentHTML("beforeend", tr);
    }
  }
}
