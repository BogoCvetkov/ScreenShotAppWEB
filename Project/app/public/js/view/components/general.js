import { HTMlMarkup } from "./markup.js";

// This module contains the components outside of the table and resource menus

export class General {
  static generateTodaySchedRow(data) {
    return HTMlMarkup.createTodayScheduleRow(data);
  }

  static generateNewQueueEntry(id) {
    return HTMlMarkup.createQueueEntry(id);
  }

  static generateSleepingStat() {
    return HTMlMarkup.createSleepingStat();
  }

  static generateWorkingStat() {
    return HTMlMarkup.createWorkingStat();
  }
}
