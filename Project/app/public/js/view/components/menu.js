import { HTMlMarkup } from "./markup.js";

// This module contains the components for the different menus related to resources

export class ResourceMenu {
  static generateCreateMenu(resource) {
    if (resource === "accounts") {
      document.body.insertAdjacentHTML(
        "beforeend",
        HTMlMarkup.createAccountMenu()
      );
    }
  }

  static showStatusDot(element, status) {
    element.innerHTML = HTMlMarkup.statusDot(status);
  }

  static generateLogTable(data) {
    let logs_table = document.querySelector(
      ".account--logs-table tbody"
    );
    logs_table.innerHTML = "";
    for (let record of data) {
      logs_table.insertAdjacentHTML(
        "beforeend",
        HTMlMarkup.createAccLogRow(record)
      );
    }
  }

  static generateScheduleMenu() {
    document.body.insertAdjacentHTML(
      "beforeend",
      HTMlMarkup.checkScheduleMenu()
    );
  }

  static generateCreateScheduleMenu() {
    document.body.insertAdjacentHTML(
      "beforeend",
      HTMlMarkup.createScheduleMenu()
    );
  }

  static generateCreatePageMenu() {
    document.body.insertAdjacentHTML(
      "beforeend",
      HTMlMarkup.createPageMenu()
    );
  }

  static generateCreateKeywordMenu() {
    document.body.insertAdjacentHTML(
      "beforeend",
      HTMlMarkup.createKeywordMenu()
    );
  }

  static generateUsersGridElement(data) {
    return HTMlMarkup.createUsersGridElement(data);
  }

  static generateCreateUserForm() {
    return HTMlMarkup.createCreateUserForm();
  }

  static generateUpdateUserForm(data) {
    return HTMlMarkup.createUpdateUserForm(data);
  }
}
