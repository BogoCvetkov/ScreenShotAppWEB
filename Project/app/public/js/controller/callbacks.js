import { APIResource } from "../model/apiFetch.js";
import { Model } from "../model/model.js";
import {
  AccountsTableView,
  AssetsTableView,
} from "../view/tableView.js";

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
