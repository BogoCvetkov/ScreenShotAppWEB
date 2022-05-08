import {
  AccountsTableView,
  PagesTableView,
} from "../view/tableView.js";
import { EventHandlers } from "../view/eventHandlers.js";
import * as cb from "./callbacks.js";
import { addSSE } from "./sse.js";

async function test() {
  // const api = new APIResource("accounts");
  // const model = new Model(api);
  // const result = await model.getResources();
  // AccountsTableView.renderTable();
  // AssetsTableView.renderTable();
  // AccountsTableView.updateTable(result.data);
  // AssetsTableView.updateRow(67, result.data[0]);
  // AccountsTableView.addFilter();
  cb.controllUpdateBotData();
  cb.controllUpdateAccRow(55);
  // addSSE();
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
      deleteResource: cb.controllDeleteResource,
      accServices: cb.controllService,
      getAccLogs: cb.controllGetAccLogs,
      getAccSched: cb.controllGetAccSchedule,
      deleteResource: cb.controllDeleteResource,
      showCreateSched: cb.controllShowCreateSchedule,
      showCreatePage: cb.controllShowCreatePage,
      showCreateKeyword: cb.controllShowCreateKeyword,
      showConfirm: cb.controllShowConfirmWindow,
      createResource: cb.controllCreateResource,
    }
  );
  EventHandlers.selectAllHandler();
  EventHandlers.selectedListenerHandler();
  EventHandlers.showBulkActionsHandler({
    updateResource: cb.controllUpdateResource,
    accServices: cb.controllService,
  });
  EventHandlers.showTodaySchedule(cb.controllGetTodaySchedule);
  EventHandlers.showQueueWindows();
  EventHandlers.tableSliderHandler(cb.controllUpdateResource);
}

test()
  .then(() => {
    addHandlers();
  })
  .catch((e) => {
    console.log(e);
  });
