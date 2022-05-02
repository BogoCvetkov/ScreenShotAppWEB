import { AccountsTableView, AssetsTableView } from "./tableView.js";
import { AccountView, AssetView } from "./resourceView.js";

// This class contains all Eventhandlers on the main page
export class EventHandlers {
  static searchBtn = document.querySelector(".btn--search");
  static filterMenuBtn = document.getElementById("filterBtn");
  static filterMenu = document.getElementById("filterMenu");
  static addFilterBtn = document.getElementById("add-filter");
  static clearFilterBtn = document.getElementById("clear-filters");
  static filterCounter = document.getElementById("filterCounter");
  static switchTabs = document.querySelectorAll(".tab");
  static editBtn = document.getElementById("edit");
  static deleteBtn = document.getElementById("delete");

  // Constructs the filters into a query
  static searchHandler(handler) {
    const searchField = document.getElementById("search");

    this.searchBtn.addEventListener("click", (e) => {
      let query = "";
      // Default search field in the input element is for /name/
      query = `name=${searchField.value}`;

      const filterRows = document.querySelectorAll(".filter__row");
      for (let row of filterRows) {
        const field = row.children[0].lastChild;
        const operator = row.children[1].lastChild;
        let value = row.children[2].lastChild;

        // Transform to timestamp
        if (value.type === "datetime-local") {
          value = new Date(value.value).getTime() / 1000;
        } else {
          value = value.value;
        }

        if (["includes", "is"].includes(operator.textContent)) {
          query = `${query}&${field.value}=${value}`;
        } else {
          query = `${query}&${field.value}=${operator.value},${value}`;
        }
      }

      handler(query);
    });
  }

  // Showing the filter menu
  static filterMenuHandler() {
    this.filterMenuBtn.addEventListener("click", (e) => {
      this.filterMenu.parentElement.classList.toggle("hidden");
    });
  }

  // Adding new filter row
  static addFilterHandler(handler) {
    this.addFilterBtn.addEventListener("click", (e) => {
      handler();
      this.filterCounter.classList.remove("hidden");
      this.filterCounter.textContent =
        this.filterMenu.children.length;
    });
  }

  // handles the logic of the filter fields
  static filterOperatorHandler() {
    this.filterMenu.addEventListener("change", (e) => {
      if (e.target.className != "filter--field") return;

      const filterOperator =
        e.target.parentElement.nextSibling.lastChild;
      const filterInput =
        e.target.parentElement.nextSibling.nextSibling.lastChild;
      const selectedField = e.target.children[e.target.selectedIndex];
      filterOperator.innerHTML = "";

      filterInput.type = "text";
      filterInput.placeholder = "Filter value";

      if (selectedField.dataset.type === "int") {
        const operators = [">", "<", "="];

        for (let op of operators) {
          const option = document.createElement("option");
          [option.value, option.textContent] = [op, op];
          filterOperator.append(option);
        }
      } else if (selectedField.dataset.type === "str") {
        const option = document.createElement("option");
        [option.value, option.textContent] = ["=", "includes"];
        filterOperator.append(option);
      } else if (selectedField.dataset.type === "bool") {
        const option = document.createElement("option");
        [option.value, option.textContent] = ["=", "is"];
        filterOperator.append(option);
        filterInput.placeholder = "True / False";
      } else if (selectedField.dataset.type === "date") {
        filterInput.type = "datetime-local";
        filterInput.required = true;
        const operators = [">", "<"];

        for (let op of operators) {
          const option = document.createElement("option");
          [option.value, option.textContent] = [op, op];
          filterOperator.append(option);
        }
      }
    });
  }

  // Removing all filters
  static clearFiltersHandler() {
    this.clearFilterBtn.addEventListener("click", (e) => {
      this.filterMenu.innerHTML = "";
      this.filterCounter.classList.add("hidden");
      this.filterCounter.textContent = "";
    });
  }

  // Takes care to disable editing if more than one row is selected
  static selectedListenerHandler() {
    const table = document.querySelector("table");
    table.addEventListener("change", (e) => {
      if (!e.target.dataset.type === "selected--field") return;
      const selectedRows = document.querySelectorAll(
        ".checkbox:checked"
      );
      // Disable Editing if more than one row is selected
      if (selectedRows[1]) {
        this.editBtn.classList.add("disabled");
        this.editBtn.dataset.disabled = true;
      } else {
        this.editBtn.classList.remove("disabled");
        this.editBtn.dataset.disabled = false;
      }
    });
  }

  // Selecting all rows if the checkbox in the header is selected
  static selectAllHandler() {
    const selectAllBox = document.getElementById("selectAll");
    selectAllBox.addEventListener("change", (e) => {
      const allBoxes = document.querySelectorAll(".checkbox");
      if (e.target.checked) {
        allBoxes.forEach((el) => (el.checked = true));
      } else {
        allBoxes.forEach((el) => (el.checked = false));
      }
    });
  }

  // Showing the update menu. The actual logic and event handlers of the update menu are in a separate class.
  static updateMenuHandler(handler, innerHandlers) {
    let resource = this._checkResource();
    UpdateMenuHandlers.showMenuHandler(
      resource,
      handler,
      innerHandlers
    );
  }

  // Showing the create menu. The actual logic and event handlers of the update menu are in a separate class.
  static createMenuHandler(handler) {
    let resource = this._checkResource();
    CreateMenuHandlers.showMenuHandler(resource, handler);
  }

  // Get's the resource type from the active tab
  static _checkResource() {
    let resource;
    this.switchTabs[0].classList.contains("tab_active")
      ? (resource = "accounts")
      : (resource = "assets");
    return resource;
  }
}

// Contains all handlers for the Update Menu of a resource
class UpdateMenuHandlers {
  static updateMenu = document.querySelector(".update__wrapper");
  static logMenu = document.querySelector(".logs__wrapper");
  static editBtn = document.getElementById("edit");
  static updateBtn = document.getElementById("update");
  static logsBtn = document.getElementById("checkLogs");
  static checkSchedBtn = document.getElementById("checkSchedule");
  static addSchedBtn = document.getElementById("addSchedule");

  static showMenuHandler(resource, handler, innerHandlers) {
    this.editBtn.addEventListener("click", (e) => {
      if (this.editBtn.dataset.disabled === "false") {
        const selectedRow = document.querySelector(
          ".checkbox:checked"
        );
        const accId = selectedRow.closest("tr").dataset.id;
        handler(resource, accId);
      }
    });
    // All Eventhandlers of menus inside this menu are attached here
    this._attachInnerHandlers(innerHandlers);
  }

  static _attachInnerHandlers(innerHandlers) {
    this._hideWindowHandler();
    this._clearCloseLogsMenuHandler();
    this._updateResourceHandler(innerHandlers.updateResource);
    this._showAccLogsHandler(innerHandlers.getAccLogs);
    this._showAccScheduleHandler(
      innerHandlers.getAccSched,
      innerHandlers
    );
    this._showCreateSchedMenuHandler(
      innerHandlers.showCreateSched,
      innerHandlers
    );
  }

  // Updating the resource
  static _updateResourceHandler(handler) {
    this.updateBtn.addEventListener("click", (e) => {
      const body = this._getFieldData(this.updateMenu);
      const resourceId = this.updateMenu.dataset.id;
      const resource = this.updateMenu.dataset.resource;
      handler(resource, resourceId, body);
    });
  }

  // Show the logs menu of an account
  static _showAccLogsHandler(handler) {
    this.logsBtn.addEventListener("click", () => {
      const accId = this.updateMenu.dataset.id;
      handler(accId);
    });
  }

  // Show the schedule of an account
  static _showAccScheduleHandler(handler, innerHandlers) {
    this.checkSchedBtn.addEventListener("click", () => {
      const accId = this.updateMenu.dataset.id;
      const checkMenu = document.querySelector(".schedule__wrapper");
      if (!checkMenu)
        handler(accId).then(() => {
          this._removeScheduleMenuHandler();
          // Handling schedule deletion
          this._deleteScheduleHour(innerHandlers.deleteSched);
        });
    });
  }

  // Show the menu for creating a new schedule
  static _showCreateSchedMenuHandler(handler, innerHandlers) {
    this.addSchedBtn.addEventListener("click", () => {
      const checkTable = document.querySelector(".create__wrapper");
      if (!checkTable) {
        handler();
        this._removeWindowHandler();
        // Handling the creation of new Schedule
        this._createNewSchedule(innerHandlers.createSched);
      }
    });
  }

  // Creating new schedule
  static _createNewSchedule(handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      let body = this._getFieldData(createMenu);
      body["account_id"] = createMenu.dataset.id;
      handler(body);
    });
  }

  // Hide the menu
  static _hideWindowHandler() {
    const closeBtn = this.updateMenu.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      this.updateMenu.classList.add("hidden");
    });
  }

  // Clear the LogsMenu
  static _clearCloseLogsMenuHandler() {
    const closeBtn = this.logMenu.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      // Clear table
      const table = this.logMenu.querySelector("tbody");
      table.innerHTML = "";
      this.logMenu.classList.add("hidden");
    });
  }

  // Removing the ScheduleMenu from HTML
  static _removeScheduleMenuHandler() {
    const scheduleMenu = document.querySelector(".schedule__wrapper");
    const closeBtn = scheduleMenu.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      scheduleMenu.remove();
    });
  }

  static _deleteScheduleHour(handler) {
    const scheduleMenu = document.querySelector(".schedule-grid");
    scheduleMenu.addEventListener("click", (e) => {
      if (e.target.className !== "close-X") return;

      // Get the id of the scheduled hour
      const id = e.target.closest(".hour-tab").dataset.id;

      console.log(id);

      // Delete it and remove it from the HTML
      handler(id).then(() => e.target.closest(".hour-tab").remove());
    });
  }

  // Remove create menu
  static _removeWindowHandler() {
    const createMenu = document.querySelector(".create__wrapper");
    const closeBtn = createMenu.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      createMenu.remove();
    });
  }

  // Helper Function - gets the values of all input fields in a menu
  static _getFieldData(element) {
    // All text fields are marked with data-input
    let fields = element.querySelectorAll("[data-input='true']");
    const active = element.querySelector(
      "input[type='checkbox']"
    )?.checked;
    const body = {};
    body.active = active;
    fields.forEach((el) => {
      if (el !== undefined) body[el.name] = el.value;
    });
    return body;
  }
}

// Contains all handlers for the create menu of a resource
class CreateMenuHandlers {
  static addNewBtn = document.getElementById("addNew");

  static showMenuHandler(resource, handler) {
    this.addNewBtn.addEventListener("click", (e) => {
      const checkTable = document.querySelector(".create__wrapper");
      if (!checkTable) {
        handler(resource);
        this._removeWindowHandler();
      }
    });
  }

  static _removeWindowHandler() {
    const createMenu = document.querySelector(".create__wrapper");
    const closeBtn = createMenu.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      createMenu.remove();
    });
  }

  static _createNewResource(handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      let body = this._getFieldData(createMenu);
      handler(body);
    });
  }

  // Helper Function - gets the values of all input fields in a menu
  static _getFieldData(element) {
    // All text fields are marked with data-input
    let fields = element.querySelectorAll("[data-input='true']");
    const active = element.querySelector(
      "input[type='checkbox']"
    )?.checked;
    const body = {};
    body.active = active;
    fields.forEach((el) => {
      if (el !== undefined) body[el.name] = el.value;
    });
    return body;
  }
}
