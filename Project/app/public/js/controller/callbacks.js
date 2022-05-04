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

/* This is where the Model connects to the View */

export async function controllSearch(resource, query) {
  let options = { query };

  const result = await fetchApi(resource, "get", { options });

  const view = getTableView(resource);
  view.updateTable(result.data);
}

export async function controllAddFilter(resource) {
  const view = getTableView(resource);
  view.addFilter();
}

export async function controllShowCreateMenu(resource) {
  const view = getView(resource);
  view.showCreateMenu();
}

// Get
export async function controllGetResource(resource, id) {
  const options = { url_param: id };
  const result = await fetchApi(resource, "get", { options });

  const view = getView(resource);
  view.showUpdateMenu(result.data[0], resource);
}

// Create
export const controllCreateResource = errorWrapper(async function (
  resource,
  body
) {
  const result = await fetchApi(resource, "create", { body });
  const msg = UtilsView.showMessage(result);

  // Remove the message Element
  setTimeout(() => UtilsView.removeMsg(msg), 5000);
});

// Update
export const controllUpdateResource = errorWrapper(async function (
  resource,
  id,
  body
) {
  const result = await fetchApi(resource, "update", { id, body });
  const msg = UtilsView.showMessage(result);

  // Remove the message Element
  setTimeout(() => UtilsView.removeMsg(msg), 5000);
});

// Delete
export const controllDeleteResource = errorWrapper(async function (
  resource,
  id
) {
  const result = await fetchApi(resource, "delete", { id });
  const msg = UtilsView.showMessage(result);

  // Remove the message Element
  setTimeout(() => UtilsView.removeMsg(msg), 5000);
});

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

//// More custom callbacks /////

// Load all resources to table
export async function controllGetAllResources(resource) {
  const result = await fetchApi(resource, "get", {});

  const view = getTableView(resource);
  view.updateTable(result.data);
}

// Getting the asset and it's account data to display it in the update menu
export async function controllGetAssetWithAccountData(resource, id) {
  const options = { url_param: id };
  const result = await fetchApi(resource, "get", { options });

  const optionsAcc = {
    url_param: result.data[0]["account_id"],
  };
  const resultAcc = await fetchApi("accounts", "get", { optionsAcc });

  // Solve double name attribute collision
  resultAcc.data[0].acc_name = resultAcc.data[0].name;
  delete resultAcc.data[0].name;
  delete resultAcc.data[0].id;
  delete resultAcc.data[0].active;

  result.data[0] = { ...result.data[0], ...resultAcc.data[0] };
  const view = getView(resource);
  view.showUpdateMenu(result.data[0], resource);
}
export async function controllGetAccLogs(id) {
  const options = { query: `account_id==,${id}&sort=desc,date` };
  const result = await fetchApi("logs", "get", { options });
  AccountView.showAccLogTable(result.data);
}

// Showing the accounts schedules
export async function controllGetAccSchedule(id) {
  const options = { query: `account_id==,${id}&sort=asc,hour` };
  const result = await fetchApi("schedules", "get", { options });
  AccountView.showAccSchedule(result.data);
}

// Showing the menu for creating a new schedule
export async function controllShowCreateSchedule() {
  AccountView.showCreateSchedMenu();
}

// Helper Function
async function fetchApi(resource, operation, input = {}) {
  const api = new APIResource(resource);
  const model = new Model(api);

  let result;
  if (operation === "get") {
    result = await model.getResources(input.options);
  } else if (operation === "create") {
    result = await model.createResource(input.body);
  } else if (operation === "update") {
    result = await model.updateResource(input.id, input.body);
  } else if (operation === "delete") {
    result = await model.deleteResource(input.id);
  }
  return result;
}

// Displays failed responses from the API
function errorWrapper(func) {
  const newFunc = async (...args) => {
    func(...args).catch((e) => {
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
