import { General } from "./components/general.js";

//  Contains the View of items not related to tables and resource menus
export class GeneralView {
  static updateTodaySchedWindow(data) {
    const todaySched = document.querySelector(
      ".today--schedule__window"
    );
    todaySched.innerHTML = "";

    for (let sched of data) {
      todaySched.insertAdjacentHTML(
        "beforeend",
        General.generateTodaySchedRow(sched)
      );
    }
  }

  static updateScheduleQueueWindow(data) {
    const waitQueue = document.getElementById("waitSchedQ");
    const retryQueue = document.getElementById("retrySchedQ");
    const execQueue = document.getElementById("executeSchedQ");

    [waitQueue, retryQueue, execQueue].forEach((el) => {
      el.innerHTML = "";
    });

    for (let job of data["schedule_bot"]["waiting"]) {
      waitQueue.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
    for (let job of data["schedule_bot"]["retry"]) {
      retryQueue.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
    for (let job of data["schedule_bot"]["executing"]) {
      execQueue.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
  }

  static updatePersonalQueueWindow(data) {
    const waitQueue = document.getElementById("waitPersQ");
    const execQueue = document.getElementById("executePersQ");

    [waitQueue, execQueue].forEach((el) => {
      el.innerHTML = "";
    });

    for (let job of data["personal_bot"]["capture"]["waiting"]) {
      waitPersQ.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
    for (let job of data["personal_bot"]["email"]["waiting"]) {
      waitPersQ.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
    for (let job of data["personal_bot"]["capture"]["executing"]) {
      execQueue.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
    for (let job of data["personal_bot"]["email"]["executing"]) {
      execQueue.insertAdjacentHTML(
        "beforeend",
        General.generateNewQueueEntry(job)
      );
    }
  }

  static updateBots(data) {
    const personal_bot = data["personal_bot"];
    const schedule_bot = data["schedule_bot"];

    if (
      personal_bot["capture"]["executing"].length ||
      personal_bot["email"]["executing"].length
    ) {
      this._updateBotStatus("personal_bot", "working");
    } else {
      this._updateBotStatus("personal_bot", "sleeping");
    }

    if (schedule_bot["executing"].length) {
      this._updateBotStatus("schedule_bot", "working");
    } else {
      this._updateBotStatus("schedule_bot", "sleeping");
    }
  }

  static _updateBotStatus(botName, status) {
    const statusDiv = document.querySelector(
      `.${botName}--wrapper .bot-status`
    );
    status === "sleeping"
      ? (statusDiv.innerHTML = General.generateSleepingStat())
      : (statusDiv.innerHTML = General.generateWorkingStat());
  }
}
