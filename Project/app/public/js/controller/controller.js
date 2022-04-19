import {
  AccountsTableView,
  AssetsTableView,
} from "../view/tableView.js";
import { EventHandlers } from "../view/eventHandlers.js";
import { controllSearch, controllAddFilter } from "./callbacks.js";

async function test() {
  // const api = new APIResource("accounts");
  // const model = new Model(api);
  // const result = await model.getResources();
  // AssetsTableView.renderTable();
  // AccountsTableView.updateTable(result.data);
  // AssetsTableView.updateRow(67, result.data[0]);
  // AccountsTableView.addFilter();
}

// Register callbacks with the Eventhandlers
EventHandlers.searchHandler(controllSearch);
EventHandlers.filterMenuHandler();
EventHandlers.addFilterHandler(controllAddFilter);
EventHandlers.clearFiltersHandler();
EventHandlers.filterOperatorHandler();

test();
