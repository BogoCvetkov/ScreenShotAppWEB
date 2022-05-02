import { Table } from "./components/table.js";

// This module contains the VIEW of the MVC- in particular the view for the table on the main page

// A base class for declaring the methods used in the subclasses (works as an Abstract Base Class)
class TableView {
  static container = document.querySelector(".main-col-2__table_div");

  // Fill the data in the table
  static updateTable(data) {
    const tableBody = this.container.querySelector("tbody");
    tableBody.innerHTML = "";
    for (let el of data) {
      const row = Table.createRow(this.fields, el);
      tableBody.append(row);
    }
  }

  // Create the Table
  static renderTable() {
    const table = document.createElement("table");
    table.classList.add(this.tableClass);
    const head = Table.createTableColumns(this.columns);
    const body = document.createElement("tbody");

    this.container.innerHTML = "";
    table.append(head, body);
    this.container.append(table);
  }

  static updateRow(id, data) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    for (let field of this.fields) {
      if (data[field[0]] !== undefined) {
        const td = row.querySelector(`td[data-field="${field[0]}"]`);
        td.textContent = data[field[0]];
      }
    }
  }

  static addFilter() {
    Table.createFilterRow(this.columns, this.fields);
  }
}

export class AccountsTableView extends TableView {
  static tableClass = ".accounts--table";
  static fields = [
    ["active", "bool"],
    ["id", "int"],
    ["email", "str"],
    ["name", "str"],
    ["last_scrape_fail", "bool"],
    ["last_email_fail", "bool"],
    ["last_scraped", "date"],
    ["last_emailed", "date"],
  ];

  static columns = [
    "Active",
    "ID",
    "Account Email",
    "Account Name",
    "Last screenshot fail",
    "Last email fail",
    "Last screenshot date",
    "Last email date",
  ];
}

export class AssetsTableView extends TableView {
  static tableClass = ".assets--table";

  static fields = [
    ["id", "int"],
    ["name", "str"],
    ["page_id", "str"],
  ];

  static columns = ["ID", "Asset Name", "Page ID"];
}
