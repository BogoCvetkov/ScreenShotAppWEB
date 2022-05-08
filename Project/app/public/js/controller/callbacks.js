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

/* This is where the Model connects to the View */

// Get
export async function controllGetResource(resource, id) {
  const options = { url_param: id };
  const result = await fetchApi(resource, "get", [options]);

  const view = getView(resource);
  view.showUpdateMenu(result.data[0], resource);
}

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
  controllUpdateBotData();
});

//// More custom callbacks /////

// Get data for multiple id's
export async function controllGetResourceInBulk(resource, idList) {
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
}

export async function controllAddFilter(resource) {
  const view = getTableView(resource);
  view.addFilter();
}

export async function controllSearch(resource, query) {
  let options = { query };

  const result = await fetchApi(resource, "get", [options]);

  const view = getTableView(resource);
  view.updateTable(result.data);
}

// Load all resources to table
export async function controllGetAllResources(resource) {
  const result = await fetchApi(resource, "get", [{}]);

  const view = getTableView(resource);
  view.updateTable(result.data);
}

// Getting the asset and it's account data to display it in the update menu
export async function controllGetAssetWithAccountData(resource, id) {
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

// Get account logs
export async function controllGetAccLogs(id) {
  const options = { query: `account_id==,${id}&sort=desc,date` };
  const result = await fetchApi("logs", "get", [options]);
  AccountView.showAccLogTable(result.data);
}

// Showing the accounts schedules
export async function controllGetAccSchedule(id) {
  const options = { query: `account_id==,${id}&sort=asc,hour` };
  const result = await fetchApi("schedules", "get", [options]);
  AccountView.showAccSchedule(result.data);
}

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
export async function controllGetTodaySchedule() {
  let day = new Date().getDay() - 1;
  // Sunday is 0 in JS and 6 in the DB
  if (day < 0) day = 6;
  const options = { query: `day==,${day}&sort=asc,hour` };
  const result = await fetchApi("schedules", "get", [options]);
  GeneralView.updateTodaySchedWindow(result.data);
}

// Update Job Queue Windows
export async function controllUpdateBotData() {
  const result = await fetchApi("services", "get");
  GeneralView.updateScheduleQueueWindow(result.data[0]);
  GeneralView.updatePersonalQueueWindow(result.data[0]);
  GeneralView.updateBots(result.data[0]);
}

// Update table row
export async function controllUpdateAccRow(id) {
  const options = { url_param: id };
  const result = await fetchApi("accounts", "get", [options]);

  AccountsTableView.updateRow(id, result.data);
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
  };

  const win = UtilsView.showProcessWindow();
  const result = await model[opsMap[operation]](...input);
  UtilsView.removeProcessWindow(win);

  return result;
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
      const msg = UtilsView.showMessage(e.response);

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
