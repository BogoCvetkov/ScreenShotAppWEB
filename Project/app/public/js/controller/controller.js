import {
  AccountsTableView,
  AssetsTableView,
} from "../view/tableView.js";
import { EventHandlers } from "../view/eventHandlers.js";
import * as cb from "./callbacks.js";

async function test() {
  // const api = new APIResource("accounts");
  // const model = new Model(api);
  // const result = await model.getResources();
  AccountsTableView.renderTable();
  // AccountsTableView.updateTable(result.data);
  // AssetsTableView.updateRow(67, result.data[0]);
  // AccountsTableView.addFilter();
}

// Register callbacks with the Eventhandlers
async function addHandlers() {
  EventHandlers.searchHandler(cb.controllSearch);
  EventHandlers.filterMenuHandler();
  EventHandlers.addFilterHandler(cb.controllAddFilter);
  EventHandlers.clearFiltersHandler();
  EventHandlers.filterOperatorHandler();
  EventHandlers.createMenuHandler(cb.controllCreateResource);
  // Attaching the inner handlers inside the update menu
  EventHandlers.updateMenuHandler(cb.controllGetResource, {
    updateResource: cb.controllUpdateResource,
    getAccLogs: cb.controllGetAccLogs,
    getAccSched: cb.controllGetAccSchedule,
    deleteSched: cb.controllDeleteSchedule,
    showCreateSched: cb.controllShowCreateSchedule,
    createSched: cb.controllCreateSchedule,
  });
  EventHandlers.selectAllHandler();
  EventHandlers.selectedListenerHandler();
}

test()
  .then(() => {
    addHandlers();
  })
  .catch((e) => {
    console.log(e);
  });
