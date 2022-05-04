import {
  AccountsTableView,
  PagesTableView,
} from "../view/tableView.js";
import { EventHandlers } from "../view/eventHandlers.js";
import * as cb from "./callbacks.js";

async function test() {
  // const api = new APIResource("accounts");
  // const model = new Model(api);
  // const result = await model.getResources();
  // AccountsTableView.renderTable();
  // AssetsTableView.renderTable();
  // AccountsTableView.updateTable(result.data);
  // AssetsTableView.updateRow(67, result.data[0]);
  // AccountsTableView.addFilter();
}

// Register callbacks with the Eventhandlers
async function addHandlers() {
  EventHandlers.switchTabHandler({
    getBulk: cb.controllGetResourceInBulk,
    getAll: cb.controllGetAllResources,
  });
  EventHandlers.searchHandler(cb.controllSearch);
  EventHandlers.filterMenuHandler();
  EventHandlers.addFilterHandler(cb.controllAddFilter);
  EventHandlers.clearFiltersHandler();
  EventHandlers.filterOperatorHandler();
  EventHandlers.createMenuHandler(cb.controllShowCreateMenu, {
    createResource: cb.controllCreateResource,
  });
  // Attaching the inner handlers inside the update menu
  EventHandlers.updateMenuHandler(
    // Main handlers
    {
      getAccount: cb.controllGetResource,
      getAsset: cb.controllGetAssetWithAccountData,
    },
    // Handlers of nested menus
    {
      updateResource: cb.controllUpdateResource,
      getAccLogs: cb.controllGetAccLogs,
      getAccSched: cb.controllGetAccSchedule,
      deleteResource: cb.controllDeleteResource,
      showCreateSched: cb.controllShowCreateSchedule,
      createResource: cb.controllCreateResource,
    }
  );
  EventHandlers.selectAllHandler();
  EventHandlers.selectedListenerHandler();
  EventHandlers.showBulkActionsHandler(cb.controllUpdateResource);
}

test()
  .then(() => {
    addHandlers();
  })
  .catch((e) => {
    console.log(e);
  });
