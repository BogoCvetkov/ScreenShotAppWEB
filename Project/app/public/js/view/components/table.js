import { HTMlMarkup } from "./markup.js";

// This module contains the components of the main table

export class Table {
  static createRow(fields, data) {
    let row = document.createElement("tr");
    row.dataset.id = data["id"];
    row.classList.add("striped");
    // Append a checkbox to every row
    let checkTd = document.createElement("td");
    checkTd.append(this._newCheckBox(data["id"]));
    checkTd.firstElementChild.dataset.type = "selected--field";
    row.append(checkTd);

    // Append the data to the row
    for (let field of fields) {
      let td = document.createElement("td");
      td.dataset.field = field[0];
      td.dataset.type = field[1];
      // Adding a slider for the active field
      if (field[0] === "active") {
        td.insertAdjacentHTML(
          "beforeend",
          HTMlMarkup.statusSlider(data[field[0]])
        );
      } else {
        td.textContent = data[field[0]];
      }
      row.append(td);
    }

    return row;
  }

  static createTableColumns(columns) {
    const head = document.createElement("thead");
    // Append a checkbox to table head
    let checkTh = document.createElement("th");
    checkTh.append(this._newCheckBox());
    checkTh.firstElementChild.id = "selectAll";
    head.append(checkTh);

    for (let col of columns) {
      let th = document.createElement("th");
      th.textContent = col;
      head.append(th);
    }

    return head;
  }

  static createFilterRow(columns, fields) {
    const filterMenu = document.getElementById("filterMenu");
    const filterRow = this._newFilterRow(columns, fields);
    filterMenu.append(filterRow);
  }

  static _newFilterRow(columns, fields) {
    const filterRow = document.createElement("div");
    filterRow.classList.add("filter__row");

    const div1 = document.createElement("div");
    const div2 = document.createElement("div");
    const div3 = document.createElement("div");

    const label1 = document.createElement("label");
    label1.textContent = "Field";
    const select1 = document.createElement("select");
    select1.classList.add("filter--field");

    const label2 = document.createElement("label");
    label2.textContent = "Operator";
    const select2 = document.createElement("select");
    select2.classList.add("filter--operator");

    const label3 = document.createElement("label");
    label3.textContent = "Value";
    const input3 = document.createElement("input");
    input3.classList.add("filter--value");
    input3.placeholder = "Filter value";

    const option = document.createElement("option");
    option.value = undefined;
    option.textContent = "-Select a field-";
    select1.append(option);

    for (let i = 0; i < columns.length; i++) {
      const option = document.createElement("option");
      option.value = fields[i][0];
      option.dataset.type = fields[i][1];
      option.textContent = columns[i];
      select1.append(option);
    }

    div1.append(label1, select1);
    div2.append(label2, select2);
    div3.append(label3, input3);

    filterRow.append(div1, div2, div3);

    return filterRow;
  }

  static _newCheckBox(id) {
    const checkBox = document.createElement("input");
    checkBox.type = "checkbox";
    checkBox.dataset.id = id;
    checkBox.classList.add("checkbox");
    return checkBox;
  }
}
