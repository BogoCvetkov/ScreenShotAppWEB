import { AccountsTableView, PagesTableView } from "../tableView.js";
import { AccountView, PageView } from "../resourceView.js";

// This class contains all Eventhandlers on the main page
export class EventHandlers {
  static todayScheduleBtn = document.getElementById("todaySchedule");
  static searchBtn = document.querySelector(".btn--search");
  static filterMenuBtn = document.getElementById("filterBtn");
  static filterMenu = document.getElementById("filterMenu");
  static addFilterBtn = document.getElementById("add-filter");
  static clearFilterBtn = document.getElementById("clear-filters");
  static filterCounter = document.getElementById("filterCounter");
  static switchTabs = document.querySelectorAll(".tab");
  static editBtn = document.getElementById("edit");
  static pauseBtn = document.getElementById("pause");
  static captureBtn = document.getElementById("captureMany");
  static activateBtn = document.getElementById("activate");
  static bulkBtn = document.getElementById("bulkActions");
  static schedJobBtn = document.getElementById("schedJobs");
  static persJobBtn = document.getElementById("yourJobs");
  static logoutBtn = document.getElementById("logout");

  // Show Job Queue
  static showQueueWindows(handler) {
    const queueWindow1 = document.querySelector(`.schedJobs`);
    this.schedJobBtn.addEventListener("click", (e) => {
      queueWindow1.classList.remove("hidden");
    });
    const queueWindow2 = document.querySelector(`.yourJobs`);
    this.persJobBtn.addEventListener("click", (e) => {
      queueWindow2.classList.remove("hidden");
    });
    this._closeWindowHandler(queueWindow1);
    this._closeWindowHandler(queueWindow2);
  }

  // Show Today's Schedule
  static showTodaySchedule(handler) {
    const todaySchedWrap = document.querySelector(
      ".today--schedule__wrapper"
    );
    this.todayScheduleBtn.addEventListener("click", (e) => {
      handler();
      todaySchedWrap.classList.remove("hidden");
    });
    this._closeWindowHandler(todaySchedWrap);
  }

  // Switch resource tables
  static switchTabHandler(handlerS) {
    const tabContainer = document.querySelector(
      ".main-col-2__nav_div"
    );
    tabContainer.addEventListener("click", (e) => {
      if (!e.target.classList.contains("tab")) return;
      const resource = e.target.dataset.resource;

      e.target.classList.add("tab_active");

      // Mark other tabs inactive. The active tab is used to get the resource to query
      const otherTabs = e.target.parentElement.querySelectorAll(
        `:not(.tab[data-resource='${resource}'])`
      );
      otherTabs.forEach((tab) => tab.classList.remove("tab_active"));

      const switchTable = document.querySelector(
        `.${resource}--table`
      );

      const idList = this._getCheckedAcc();

      // If an account is selected
      if (resource !== "accounts" && idList.length) {
        handlerS.getBulk(resource, idList);
      } else if (resource !== "accounts") {
        // Else display the assets of all accounts
        handlerS.getAll(resource);
      }

      switchTable.classList.remove("hidden");

      // Hide other Tables
      const otherTables = document.querySelectorAll(
        `.main-col-2__table_div table:not(.${resource}--table)`
      );
      otherTables.forEach((tb) => tb.classList.add("hidden"));
      // Reset Filters
      document.getElementById("clear-filters").click();
    });
  }

  // Constructs the filters into a query
  static searchHandler(handler) {
    const searchField = document.getElementById("search");

    this.searchBtn.addEventListener("click", (e) => {
      const resource = this._checkResource();
      let query = "";
      // Default search field in the input element is for /name/
      resource !== "keywords"
        ? (query = `name=${searchField.value}`)
        : (query = `keyword=${searchField.value}`);

      const filterRows = document.querySelectorAll(".filter__row");
      if (filterRows.length) query = ``;

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

      handler(resource, query);
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
      handler(this._checkResource());
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
    const tables = document.querySelectorAll("table");
    tables.forEach((tb) =>
      tb.addEventListener("change", (e) => {
        if (!e.target.dataset.type === "selected--field") return;
        const selectedRows = tb.querySelectorAll(".checkbox:checked");
        // Disable Editing if more than one row is selected
        if (selectedRows[1]) {
          this.editBtn.classList.add("disabled");
          this.editBtn.dataset.disabled = true;
        } else {
          this.editBtn.classList.remove("disabled");
          this.editBtn.dataset.disabled = false;
        }
        // Show number of selected accounts
        if (e.target.closest(".accounts--table"))
          document.querySelector("#tab_accounts span").textContent =
            selectedRows.length;
      })
    );
  }

  // Selecting all rows if the checkbox in the header is selected
  static selectAllHandler() {
    const selectAllBox = document.querySelectorAll(".select-all");
    selectAllBox.forEach((box) =>
      box.addEventListener("change", (e) => {
        const table = box.closest("table");
        const allBoxes = table.querySelectorAll(".checkbox");
        if (e.target.checked) {
          allBoxes.forEach((el) => (el.checked = true));
        } else {
          allBoxes.forEach((el) => (el.checked = false));
        }
      })
    );
  }

  // Show Actions dropdown
  static showBulkActionsHandler(innerHandlers) {
    this.bulkBtn.addEventListener("click", () => {
      const bulkDropDown = document.querySelector(
        ".btn_bulk__container"
      );
      bulkDropDown.classList.toggle("hidden");
    });
    this._pauseManyHandler(innerHandlers.updateResource);
    this._activateManyHandler(innerHandlers.updateResource);
    this._captureManyHandler(innerHandlers.accServices);
  }

  // Pause many
  static _pauseManyHandler(handler) {
    this.pauseBtn.addEventListener("click", (e) => {
      const table = document.querySelector(
        `.${this._checkResource()}--table`
      );
      const selectedRows = table.querySelectorAll(
        "td .checkbox:checked"
      );

      for (let row of selectedRows) {
        const id = row.dataset.id;
        const body = { active: false };
        const resource = this._checkResource();
        handler(resource, id, body);
      }
      const bulkDropDown = document.querySelector(
        ".btn_bulk__container"
      );
      bulkDropDown.classList.toggle("hidden");
    });
  }

  // Activate many
  static _activateManyHandler(handler) {
    this.activateBtn.addEventListener("click", (e) => {
      const table = document.querySelector(
        `.${this._checkResource()}--table`
      );
      const selectedRows = table.querySelectorAll(
        "td .checkbox:checked"
      );

      for (let row of selectedRows) {
        const id = row.dataset.id;
        const body = { active: true };
        const resource = this._checkResource();
        handler(resource, id, body);
      }
      const bulkDropDown = document.querySelector(
        ".btn_bulk__container"
      );
      bulkDropDown.classList.toggle("hidden");
    });
  }

  // Capture many
  static _captureManyHandler(handler) {
    this.captureBtn.addEventListener("click", (e) => {
      const table = document.querySelector(`.accounts--table`);
      const selectedRows = table.querySelectorAll(
        "td .checkbox:checked"
      );

      const idList = [];

      for (let row of selectedRows) {
        idList.push(row.dataset.id);
      }

      handler("scrape", idList);

      const bulkDropDown = document.querySelector(
        ".btn_bulk__container"
      );
      bulkDropDown.classList.toggle("hidden");
    });
  }

  // Showing the update menu. The actual logic and event handlers of the update menu are in a separate class.
  static updateMenuHandler(handlers, innerHandlers) {
    UpdateMenuHandlers.showMenuHandler(handlers, innerHandlers);
  }

  // Showing the create menu. The actual logic and event handlers of the update menu are in a separate class.
  static createMenuHandler(handler, innerHandlers) {
    CreateMenuHandlers.showMenuHandler(handler, innerHandlers);
  }

  static tableSliderHandler(handler) {
    const tableWrap = document.querySelector(`.table_div__wrapper`);
    tableWrap.addEventListener("click", (e) => {
      if (e.target.className !== "slider round") return;
      const tr = e.target.closest("tr");
      const resource = this._checkResource();
      const body = {
        active: !e.target.previousElementSibling.checked,
      };
      handler(resource, tr.dataset.id, body);
    });
  }

  // HELPER FUNCTIONS

  // Get's the resource type from the active tab
  static _checkResource() {
    const tab = document.querySelector(".tab_active");
    return tab.dataset.resource;
  }

  //Close window
  static _closeWindowHandler(element) {
    const closeBtn = element.querySelector(".close-X");
    closeBtn.addEventListener("click", (e) => {
      element.classList.add("hidden");
    });
  }

  // Check all checked accounts
  static _getCheckedAcc() {
    const accTable = document.querySelector(".accounts--table tbody");
    const selectedAcc = accTable.querySelectorAll(
      "td .checkbox:checked"
    );
    let idList = [];
    if (selectedAcc.length)
      selectedAcc.forEach((el) => {
        idList.push(el.dataset.id);
      });

    return idList;
  }
}
/////////////////////////////////////////////////////////////////////
// Contains all handlers for elements inside the Update Menu of a resource
class UpdateMenuHandlers {
  static updateMenu = document.querySelector(".update__wrapper");
  static logMenu = document.querySelector(".logs__wrapper");
  static editBtn = document.getElementById("edit");
  static updateBtn = document.querySelectorAll("#update");
  static delBtn = document.querySelectorAll("#deleteResource");
  static logsBtn = document.getElementById("checkLogs");
  static checkSchedBtn = document.getElementById("checkSchedule");
  static addSchedBtn = document.getElementById("addSchedule");
  static addPageBtn = document.getElementById("addPage");
  static addKeywordBtn = document.getElementById("addKeyword");
  static pdfBtn = document.getElementById("lastPDF");
  static captureBtn = document.getElementById("captureAcc");
  static emailBtn = document.getElementById("sendEmail");

  static showMenuHandler(handlers, innerHandlers) {
    this.editBtn.addEventListener("click", (e) => {
      if (this.editBtn.dataset.disabled === "false") {
        const resource = EventHandlers._checkResource();
        const table = document.querySelector(`.${resource}--table`);
        const selectedRow = table.querySelector(".checkbox:checked");
        const accId = selectedRow.dataset.id;
        resource !== "accounts"
          ? handlers.getAsset(resource, accId)
          : handlers.getAccount(resource, accId);
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
    this._showAddPageHandler(
      innerHandlers.showCreatePage,
      innerHandlers
    );
    this._showAddKeywordHandler(
      innerHandlers.showCreateKeyword,
      innerHandlers
    );
    this._checkLastPDFHandler();
    this._captureAccHandler(innerHandlers.accServices);
    this._showEmailConfirmHandler(
      innerHandlers.showConfirm,
      innerHandlers
    );
    this._showDeleteConfirmHandler(
      innerHandlers.showConfirm,
      innerHandlers
    );
  }

  // Check PDf
  static _checkLastPDFHandler() {
    this.pdfBtn.addEventListener("click", (e) => {
      const pdfLoc = e.currentTarget.dataset.pdf;
      window.open(pdfLoc, "_blank");
    });
  }

  //Capture Account
  static _captureAccHandler(handler) {
    this.captureBtn.addEventListener("click", (e) => {
      const accId = this.updateMenu.dataset.id;
      handler("scrape", [accId]);
    });
  }

  // Show Email Confirmation
  static _showEmailConfirmHandler(handler, innerHandlers) {
    this.emailBtn.addEventListener("click", (e) => {
      const checkWindow = document.querySelector(".confirm--screen");
      if (!checkWindow) {
        const email = this.updateMenu.querySelector(
          "input[name='email']"
        );
        handler(`Send email to : ${email.textContent} ?`);
      }
      const func = () => {
        const accId = this.updateMenu.dataset.id;
        innerHandlers.accServices("email", [accId]);
      };
      //  Handling the emailing after confirmation
      this._executeConsent(func);
    });
  }

  // Updating the resource
  static _updateResourceHandler(handler) {
    this.updateBtn.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const resource = this.updateMenu.dataset.resource;
        const menu = this.updateMenu.querySelector(
          `.update--resource__window.${resource}--resource`
        );
        const body = this._getFieldData(menu);
        const resourceId = this.updateMenu.dataset.id;
        handler(resource, resourceId, body);
      })
    );
  }

  // Show delete confirmation
  static _showDeleteConfirmHandler(handler, innerHandlers) {
    this.delBtn.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        const checkWindow = document.querySelector(
          ".confirm--screen"
        );
        // If no such window has been shown, show it
        if (!checkWindow) {
          handler(
            `Delete this ${this.updateMenu.dataset.resource} resource?`
          );
        }
        // Define the function that the confirmation will execute
        const func = () => {
          const resource = this.updateMenu.dataset.resource;
          const resourceId = this.updateMenu.dataset.id;
          innerHandlers
            .deleteResource(resource, resourceId)
            // Remove the row from table
            .then(() => {
              document
                .querySelector(
                  `.table_div__wrapper table:not(.hidden) tr[data-id='${resourceId}']`
                )
                .remove();
              // Hide the menu
              this.updateMenu.classList.add("hidden");
            });
        };
        //  Handling the deletion after confirmation
        this._executeConsent(func);
      })
    );
  }

  // Handle confirmation on certain actions
  static async _executeConsent(func) {
    const confirmWindow = document.querySelector(".confirm--screen");
    confirmWindow.addEventListener("click", (e) => {
      if (e.target.tagName !== "BTN") return;
      // Function that the confirmation will execute
      if (e.target.id === "YES") func();

      confirmWindow.remove();
    });
  }

  // Show the logs menu of an account
  static _showAccLogsHandler(handler) {
    this.logsBtn.addEventListener("click", () => {
      const accId = this.updateMenu.dataset.id;
      handler(accId);
    });
  }

  // Show the menu for creating a new page
  static _showAddPageHandler(handler, innerHandlers) {
    this.addPageBtn.addEventListener("click", () => {
      const checkTable = document.querySelector(".create__wrapper");
      if (!checkTable) {
        handler();
        this._removeWindowHandler();
        // Handling the creation of new Page
        this._createNewPage(innerHandlers.createResource);
      }
    });
  }

  // Creating new page
  static _createNewPage(handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      let body = this._getFieldData(createMenu);
      let resource = createMenu.dataset.resource;
      body["account_id"] = createMenu.dataset.id;
      handler(resource, body);
    });
  }

  // Show the menu for creating a new keyword
  static _showAddKeywordHandler(handler, innerHandlers) {
    this.addKeywordBtn.addEventListener("click", () => {
      const checkTable = document.querySelector(".create__wrapper");
      if (!checkTable) {
        handler();
        this._removeWindowHandler();
        // Handling the creation of new Keyword
        this._createNewKeyword(innerHandlers.createResource);
      }
    });
  }

  // Creating new keyword
  static _createNewKeyword(handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      let body = this._getFieldData(createMenu);
      let resource = createMenu.dataset.resource;
      body["account_id"] = createMenu.dataset.id;
      handler(resource, body);
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
          this._deleteScheduleHour(innerHandlers.deleteResource);
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
        this._createNewSchedule(innerHandlers.createResource);
      }
    });
  }

  // Creating new schedule
  static _createNewSchedule(handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      let body = this._getFieldData(createMenu);
      let resource = createMenu.dataset.resource;
      body["account_id"] = createMenu.dataset.id;
      body["email"] = this.addSchedBtn.dataset.email;
      handler(resource, body);
    });
  }

  // Hide the menu
  static _hideWindowHandler() {
    const closeBtn = this.updateMenu.querySelectorAll(".close-X");
    closeBtn.forEach((btn) =>
      btn.addEventListener("click", (e) => {
        this.updateMenu.classList.add("hidden");

        // Hide the respective resource menu
        this.updateMenu
          .querySelector(".update--resource__window:not(.hidden)")
          .classList.add("hidden");
      })
    );
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
      const resource = e.target.closest(".hour-tab").dataset.resource;

      // Delete it and remove it from the HTML
      handler(resource, id).then(() =>
        e.target.closest(".hour-tab").remove()
      );
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

  // Helper Fucntions

  // gets the values of all input fields in a menu
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
    console.log(body);
    return body;
  }
}

///////////////////////////////////////////////////////////////

// Contains all handlers for the create menu of an account
class CreateMenuHandlers {
  static addNewBtn = document.getElementById("addNew");

  static showMenuHandler(handler, innerHandlers) {
    this.addNewBtn.addEventListener("click", (e) => {
      const checkTable = document.querySelector(".create__wrapper");
      const resource = EventHandlers._checkResource();
      if (!checkTable) {
        handler(resource);
        this._removeWindowHandler();
        this._createNewResourceHandler(
          resource,
          innerHandlers.createResource
        );
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

  static _createNewResourceHandler(resource, handler) {
    const createMenu = document.querySelector(".create__wrapper");
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      const body = this._getFieldData(createMenu);
      console.log(body);
      handler(resource, body);
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
