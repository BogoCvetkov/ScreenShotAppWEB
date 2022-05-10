import { LogsEventHandler } from "../view/eventhandlers/logsHandlers.js";
import * as cb from "./callbacks.js";

LogsEventHandler.getAllLogsHandler(cb.controllGetAllLogs);
