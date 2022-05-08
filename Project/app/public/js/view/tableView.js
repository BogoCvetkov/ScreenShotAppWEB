import { Table } from "./components/table.js";

// This module contains the VIEW of the MVC- in particular the view for the table on the main page

// A base class for declaring the methods used in the subclasses (works as an Abstract Base Class)
class TableView {
  static container = document.querySelector(".main-col-2__table_div");

  // Fill the data in the table
  static updateTable(data) {
    const tableBody = this.container.querySelector(
      `${this.tableClass} tbody`
    );
    tableBody.innerHTML = "";
    for (let el of data) {
      const row = Table.createRow(this.fields, el);
      tableBody.append(row);
    }
    document.getElementById(
      "accSummary"
    ).innerHTML = `Number of results: <span id="accSummary">${tableBody.childElementCount}</span>`;
  }

  // Create the Table - I moved the Table Template to the main HTML document
  // This is not currently being used
  static renderTable(opts) {
    const table = document.createElement("table");
    if (opts && opts.hidden) table.classList.add("hidden");
    table.classList.add(this.tableClass);
    const head = Table.createTableColumns(this.columns);
    const body = document.createElement("tbody");

    this.container.innerHTML = "";
    table.append(head, body);
    this.container.append(table);
  }

  static updateRow(id, data) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row)
      for (let field of this.fields) {
        if (data[field[0]] !== undefined) {
          const td = row.querySelector(
            `td[data-field="${field[0]}"]`
          );
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

export class PagesTableView extends TableView {
  static tableClass = ".pages--table";

  static fields = [
    ["active", "bool"],
    ["id", "int"],
    ["name", "str"],
    ["page_id", "str"],
    ["account_id", "int"],
  ];

  static columns = [
    "Active",
    "ID",
    "Page Name",
    "Page ID",
    "Account ID",
  ];
}

export class KeywordsTableView extends TableView {
  static tableClass = ".keywords--table";

  static fields = [
    ["active", "bool"],
    ["id", "int"],
    ["keyword", "str"],
    ["account_id", "int"],
  ];

  static columns = ["Active", "ID", "Keyword", "Account ID"];
}
