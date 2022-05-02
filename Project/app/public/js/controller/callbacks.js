import { APIResource } from "../model/apiFetch.js";
import { Model } from "../model/model.js";
import {
  AccountsTableView,
  AssetsTableView,
} from "../view/tableView.js";
import { AccountView, AssetView } from "../view/resourceView.js";

/* This is where the Model connects to the View */

export async function controllSearch(query) {
  let options = { query };
  const api = new APIResource("accounts");
  const model = new Model(api);
  const result = await model.getResources(options);
  AccountsTableView.updateTable(result.data);
}

export async function controllAddFilter() {
  AccountsTableView.addFilter();
}

export async function controllCreateResource(resource) {
  resource = "accounts"
    ? AccountView.showCreateMenu()
    : AssetView.showCreateMenu();
}

export async function controllGetResource(resource, id) {
  const api = new APIResource(resource);
  const model = new Model(api);
  const result = await model.getResources({ url_param: id });
  AccountView.showUpdateMenu(result.data[0], resource);
}

export async function controllUpdateResource(resource, id, body) {
  const api = new APIResource(resource);
  const model = new Model(api);
  const result = await model.updateResource(id, body);
}

export async function controllGetAccLogs(id) {
  const options = { query: `account_id==,${id}&sort=desc,date` };
  const api = new APIResource("logs");
  const model = new Model(api);
  const result = await model.getResources(options);
  AccountView.showAccLogTable(result.data);
}

// Showing the accounts schedules
export async function controllGetAccSchedule(id) {
  const options = { query: `account_id==,${id}&sort=asc,hour` };
  const api = new APIResource("schedules");
  const model = new Model(api);
  const result = await model.getResources(options);
  AccountView.showAccSchedule(result.data);
}

export async function controllDeleteSchedule(id) {
  const api = new APIResource("schedules");
  const model = new Model(api);
  const result = await model.deleteResource(id);
}

// Showing the menu for creating a new schedule
export async function controllShowCreateSchedule() {
  AccountView.showCreateSchedMenu();
}

// Creating the new schedule
export async function controllCreateSchedule(body) {
  const api = new APIResource("schedules");
  const model = new Model(api);
  const result = await model.createResource(body);
}
