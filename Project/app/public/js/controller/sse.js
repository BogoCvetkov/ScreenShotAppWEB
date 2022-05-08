import * as cb from "./callbacks.js";

export function addSSE() {
  const evtSource = new EventSource("/api/stream/");
  evtSource.addEventListener("workers", (e) => {
    const data = JSON.parse(e.data);
    for (let id of data.message.ids) {
      cb.controllUpdateAccRow(id);
    }
  });
}
