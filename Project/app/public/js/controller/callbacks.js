import { APIResource } from "../model/apiFetch.js";
import { Model } from "../model/model.js";
import {
  AccountsTableView,
  KeywordsTableView,
  PagesTableView,
} from "../view/tableView.js";
import {
  AccountView,
  KeywordView,
  PageView,
} from "../view/resourceView.js";
import { UtilsView } from "../view/utilsView.js";
import { GeneralView } from "../view/generalView.js";
import { LogsView } from "../view/logsView.js";
import { UsersView } from "../view/usersView.js";

/* This is where the Model connects to the View */

// Get
export const controllGetResource = errorWrapper(async function (
  resource,
  id
) {
  const options = { url_param: id };
  const result = await fetchApi(resource, "get", [options]);

  const view = getView(resource);
  view.showUpdateMenu(result.data[0], resource);
});

// Create
export const controllCreateResource = errorWrapper(async function (
  resource,
  body
) {
  const result = await fetchApi(resource, "create", [body]);
  displayMsg(result);
});

// Update
export const controllUpdateResource = errorWrapper(async function (
  resource,
  id,
  body
) {
  const result = await fetchApi(resource, "update", [id, body]);
  displayMsg(result);
  const view = getTableView(resource);
  view.updateRow(id, result.data[0]);
});

// Delete
export const controllDeleteResource = errorWrapper(async function (
  resource,
  id
) {
  const result = await fetchApi(resource, "delete", [id]);
  displayMsg(result);
});

/// SERVICES ///

// Manage Services
export const controllService = errorWrapper(async function (
  service,
  id_list
) {
  const options = { query: `type=${service}` };
  const result = await fetchApi("services", "rpc", [
    { id_list },
    options,
  ]);
  displayMsg(result);

  // Update Bot Status
  setTimeout(() => {
    controllUpdateBotData();
  }, 1000);
});

//// More custom callbacks /////

// Get data for multiple id's
export const controllGetResourceInBulk = errorWrapper(async function (
  resource,
  idList
) {
  let data = [];
  const api = new APIResource(resource);
  const model = new Model(api);
  async function getData() {
    for (let id of idList) {
      const result = await model.getResources({
        query: `account_id==,${id}`,
      });
      data = data.concat(result.data);
    }
  }
  await getData();

  const view = getTableView(resource);
  view.updateTable(data);
});

export async function controllAddFilter(resource) {
  const view = getTableView(resource);
  view.addFilter();
}

export const controllSearch = errorWrapper(async function (
  resource,
  query
) {
  let options = { query };

  const result = await fetchApi(resource, "get", [options]);

  const view = getTableView(resource);
  view.updateTable(result.data);
});

// Load all resources to table
export const controllGetAllResources = errorWrapper(async function (
  resource
) {
  const result = await fetchApi(resource, "get", [{}]);

  const view = getTableView(resource);
  view.updateTable(result.data);
});

// Getting the asset and it's account data to display it in the update menu
export const controllGetAssetWithAccountData = errorWrapper(
  async function (resource, id) {
    const options = { url_param: id };
    const result = await fetchApi(resource, "get", [options]);

    const optionsAcc = {
      url_param: result.data[0]["account_id"],
    };
    const resultAcc = await fetchApi("accounts", "get", [optionsAcc]);

    // Solve double name attribute collision
    resultAcc.data[0].acc_name = resultAcc.data[0].name;
    delete resultAcc.data[0].name;
    delete resultAcc.data[0].id;
    delete resultAcc.data[0].active;

    result.data[0] = { ...result.data[0], ...resultAcc.data[0] };
    const view = getView(resource);
    view.showUpdateMenu(result.data[0], resource);
  }
);

// Get account logs
export const controllGetAccLogs = errorWrapper(async function (id) {
  const options = { query: `account_id==,${id}&sort=desc,date` };
  const result = await fetchApi("logs", "get", [options]);
  AccountView.showAccLogTable(result.data);
});

// Showing the accounts schedules
export const controllGetAccSchedule = errorWrapper(async function (
  id
) {
  const options = { query: `account_id==,${id}&sort=asc,hour` };
  const result = await fetchApi("schedules", "get", [options]);
  AccountView.showAccSchedule(result.data);
});

// Showing the menu for creating a new account
export async function controllShowCreateMenu(resource) {
  const view = getView(resource);
  view.showCreateMenu();
}

// Showing the menu for creating a new page
export async function controllShowCreatePage() {
  AccountView.showCreatePageMenu();
}
// Showing the menu for creating a new keyword
export async function controllShowCreateKeyword() {
  AccountView.showCreateKeywordMenu();
}

// Showing the menu for creating a new schedule
export async function controllShowCreateSchedule() {
  AccountView.showCreateSchedMenu();
}

// Showing the confirm window
export async function controllShowConfirmWindow(msg) {
  UtilsView.showConfirmWindow(msg);
}

// Get today's Scheduled accounts
export const controllGetTodaySchedule = errorWrapper(
  async function () {
    let day = new Date().getDay() - 1;
    // Sunday is 0 in JS and 6 in the DB
    if (day < 0) day = 6;
    const options = { query: `day==,${day}&sort=asc,hour` };
    const result = await fetchApi("schedules", "get", [options]);
    GeneralView.updateTodaySchedWindow(result.data);
  }
);

// Update Job Queue Windows
export const controllUpdateBotData = errorWrapper(async function () {
  const result = await fetchApi("services", "get");
  GeneralView.updateScheduleQueueWindow(result.data[0]);
  GeneralView.updatePersonalQueueWindow(result.data[0]);
  GeneralView.updateBots(result.data[0]);
});

// Update table row
export const controllUpdateAccRow = errorWrapper(async function (id) {
  const options = { url_param: id };
  const result = await fetchApi("accounts", "get", [options]);

  AccountsTableView.updateRow(id, result.data);
});

// Logout
export async function controllLogOut() {
  await fetchApi("logOut", "logout");
  setTimeout(() => {
    location.assign(location.origin);
  }, 500);
}

//// LOGIN PAGE ////
export const controllAuth = errorWrapper(async function (
  resource,
  body
) {
  const result = await fetchApi(resource, "auth", [body]);
  displayMsg(result);
  setTimeout(() => {
    location.assign(location.origin);
  }, 1000);
});

export const controllResetPass = errorWrapper(async function (
  token,
  body
) {
  const result = await fetchApi("resetPass", "reset", [token, body]);
  displayMsg(result);
  setTimeout(() => {
    location.assign(location.origin + "/login");
  }, 2000);
});

//// ALL LOGS PAGE ////

export const controllGetAllLogs = errorWrapper(async function (
  query
) {
  const options = { query };
  const result = await fetchApi("logs", "get", [options]);
  LogsView.generateAllLogsTable(result.data);
});

//// USERS PAGE ////

export const controllGetAllUsers = errorWrapper(async function () {
  const result = await fetchApi("users", "get");
  UsersView.generateUsersGrid(result.data);
});

// Showing the create user form
export async function controllShowCreateUserForm() {
  UsersView.generateCreateUserForm();
}

// Showing the update user form
export async function controllShowUpdateUserForm(id) {
  const options = { url_param: id };
  const result = await fetchApi("users", "get", [options]);
  UsersView.generateUpdateUserForm(result.data[0]);
}

////////////////////////
// Helper Function
async function fetchApi(resource, operation, input = []) {
  const api = new APIResource(resource);
  const model = new Model(api);
  const opsMap = {
    get: "getResources",
    create: "createResource",
    update: "updateResource",
    delete: "deleteResource",
    rpc: "useService",
    auth: "authenticate",
    reset: "resetPass",
    logout: "logOut",
  };
  const win = UtilsView.showProcessWindow();
  try {
    const result = await model[opsMap[operation]](...input);
    UtilsView.removeProcessWindow(win);
    return result;
  } catch (e) {
    UtilsView.removeProcessWindow(win);
    throw e;
  }
}

// Display API responses
async function displayMsg(result) {
  const msg = UtilsView.showMessage(result);

  // Remove the message Element
  setTimeout(() => UtilsView.removeMsg(msg), 5000);
}

// Displays failed responses from the API
function errorWrapper(func) {
  const newFunc = async (...args) => {
    func(...args).catch((e) => {
      // Check if user token is expired and refresh the view
      if (e.response.status === 401) location.assign(location.origin);

      const msg = UtilsView.showMessage(e.response.data);

      // Remove the message Element
      setTimeout(() => UtilsView.removeMsg(msg), 5000);
    });
  };
  return newFunc;
}

function getTableView(resource) {
  let view;
  if (resource === "accounts") view = AccountsTableView;
  if (resource === "pages") view = PagesTableView;
  if (resource === "keywords") view = KeywordsTableView;
  return view;
}

function getView(resource) {
  let view;
  if (resource === "accounts") view = AccountView;
  if (resource === "pages") view = PageView;
  if (resource === "keywords") view = KeywordView;
  return view;
}
