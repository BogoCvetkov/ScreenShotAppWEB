import { ResourceMenu } from "./components/menu.js";
import { AccountsTableView, AssetsTableView } from "./tableView.js";

// This module contains the VIEW of the MVC- in particular the view for the menus related to resource management - CRUD

class baseResourceView {
  static showCreateMenu() {
    // Creating the menu everytime. Generating the HTML code
    ResourceMenu.generateCreateMenu(this.type);
  }

  //  Unhiding the menu - part of the main HTML code
  static showUpdateMenu(data, resource) {
    const updateMenu = document.querySelector(".update__wrapper");
    // Set the Resource id and type in the menu
    updateMenu.dataset.id = data.id;
    updateMenu.dataset.resource = resource;
    // Update all fields of the respective resource
    this.fields.forEach((field) => {
      if (field[1] !== "bool") {
        const element = updateMenu.querySelector(
          `[name='${field[0]}']`
        );
        if (element) {
          // For inputs
          element.value = data[field[0]];
          // For text fields
          element.innerText = data[field[0]];
        }
      } else if (field[0] !== "active") {
        // For status fields
        const element = updateMenu.querySelector(
          `[name='${field[0]}']`
        );
        if (element)
          ResourceMenu.showStatusDot(element, data[field[0]]);
      }
    });
    // Mark active/inactive
    const slider = updateMenu.querySelector("input[type='checkbox']");
    slider.checked = data.active;
    // Show Menu
    updateMenu.classList.remove("hidden");
  }
}

export class AccountView extends baseResourceView {
  static type = "accounts";
  static fields = AccountsTableView.fields.concat([
    ["email_body", "str"],
  ]);

  static showAccLogTable(data) {
    // Container is in the main HTML file
    let logs__wrapper = document.querySelector(".logs__wrapper");
    logs__wrapper.classList.remove("hidden");
    ResourceMenu.generateLogTable(data);
  }

  static showAccSchedule(data) {
    ResourceMenu.generateScheduleMenu();
    for (let sched of data) {
      // Select the column for the day
      const dayRow = document.querySelector(
        `.grid-section:nth-child(${sched.day + 1})`
      );
      // Create and add the hour tab
      const hourTab = document.createElement("div");
      hourTab.className = "hour-tab";
      hourTab.textContent = sched.hour;
      hourTab.dataset.id = sched.id;
      hourTab.insertAdjacentHTML(
        "beforeend",
        "<div class='close-X'>X</div>"
      );
      dayRow.append(hourTab);
    }
  }

  static showCreateSchedMenu() {
    ResourceMenu.generateCreateScheduleMenu();
    const schedMenu = document.querySelector(".create__wrapper");
    const accId = document.querySelector(".update__wrapper").dataset
      .id;
    schedMenu.dataset.id = accId;
  }
}

export class AssetView extends baseResourceView {
  static type = "assets";
  static fields = AssetsTableView.fields;
}
