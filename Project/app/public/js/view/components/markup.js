// Contains all HTML templates
export class HTMlMarkup {
  static createAccountMenu() {
    let markup = `
      <div class="create__wrapper top--layer">
            <div class="create--resource__window">
            <div class="close-X">X</div>
                <h3>Create Account</h3>
                <div class="create--form">
                    <div class="resource--field">
                        <p>Account Name</p>
                        <input type="text" name="name" data-input='true'>
                    </div>
                    <div class="resource--field">
                        <p>Account Email</p>
                        <input type="email" name="email" data-input='true'>
                    </div>
                    <btn id="create"> CREATE</btn> 
                </div>
            </div>
        </div>`;

    return markup;
  }

  static statusSlider(status) {
    let markup = `
      <label class="switch">
                      <input type="checkbox" ${
                        status === true ? "checked" : "unchecked"
                      } >
                      <span class="slider round"></span>
                  </label>
      `;

    return markup;
  }

  static statusDot(status) {
    let markup;
    if (status === true) {
      markup = `
      <div class="status--dot dot-red">
        <div class="status--dot dot-red ringring-red"></div>
      </div>
        `;
    } else {
      markup = `
      <div class="status--dot dot-green">
        <div class="status--dot dot-green ringring-green"></div>
      </div>
        `;
    }

    return markup;
  }

  static createLogRow(data) {
    let markup = `
    <tr class=${data.fail ? "tr-red" : "tr-green"}>
      <td>${data["started_by"]}</td>
      <td>${data["log_msg"]}</td>
      <td>${data["date"]}</td>
    </tr>
    `;
    return markup;
  }

  static checkScheduleMenu(data) {
    let markup = `
    <div class="schedule__wrapper top--layer  ">
      <div class="account-schedule-screen">
        <div class="close-wrapper">
          <h3>ACCOUNT SCHEDULE</h3>
          <div class="close-X">X</div>
        </div>
        <div class="schedule-grid">
          <div class="grid-section">
            <p>Monday</p>
          </div>
          <div class="grid-section">
            <p>Tuesday</p>
          </div>
          <div class="grid-section">
            <p>Wednesday</p>
          </div>
          <div class="grid-section">
            <p>Thursday</p>
          </div>
          <div class="grid-section">
            <p>Friday</p>
          </div>
          <div class="grid-section">
            <p>Saturday</p>
          </div>
          <div class="grid-section">
            <p>Sunday</p>
          </div>
        </div>
      </div>
    </div>
    `;
    return markup;
  }

  static createScheduleMenu() {
    let markup = `
    <div class="create__wrapper top--layer ">
    <div class="create--resource__window">
        <div class="close-X">X</div>
        <h3>Create Schedule</h3>
        <div class="create--form">
            <div class="resource--field">
                <p>Day</p>
                <select name="day" data-input='true' required>
                 <option value='0'>Monday</option>
                 <option value='1'>Tuesday</option>
                 <option value='2'>Wednesday</option>
                 <option value='3'>Thursday</option>
                 <option value='4'>Friday</option>
                 <option value='5'>Saturday</option>
                 <option value='6'>Sunday</option>
                </select>
            </div>
            <div class="resource--field" >
                <p>Hour</p>
                <input type="number" name="hour" data-input='true' required>
            </div>
            <btn id="create"> CREATE</btn> 
        </div>
    </div>
</div> 
  `;
    return markup;
  }

  static createPageMenu() {
    let markup = `
    <div class="create__wrapper top--layer ">
    <div class="create--resource__window">
        <div class="close-X">X</div>
        <h3>Add Page</h3>
        <div class="create--form">
            <div class="resource--field" >
                <p>Page Name</p>
                <input type="text" name="name" data-input='true' required>
            </div>
            <div class="resource--field" >
                <p>Page ID</p>
                <input type="text" name="page_id" data-input='true' required>
            </div>
            <btn id="create"> CREATE</btn> 
        </div>
    </div>
</div> 
  `;
    return markup;
  }

  static createKeywordMenu() {
    let markup = `
    <div class="create__wrapper top--layer ">
    <div class="create--resource__window">
        <div class="close-X">X</div>
        <h3>Add Keyword</h3>
        <div class="create--form">
            <div class="resource--field" >
                <p>Keyword</p>
                <input type="text" name="keyword" data-input='true' required>
            </div>
            <btn id="create"> CREATE</btn> 
        </div>
    </div>
</div> 
  `;
    return markup;
  }

  static createTodayScheduleRow(data) {
    let markup = `
           <div class="scheduled--account">
               <p class="scheduled--account_email">${data.email}</p>
               <p class="scheduled--account_hour">${data.hour}</p>
           </div>
    `;
    return markup;
  }

  static createQueueEntry(id) {
    let markup = `
    <div class="queued--job">${id}</div>
    `;
    return markup;
  }

  static createWorkingStat() {
    let markup = `
    <div class="spinner--gear_wrapper">
      <div class="spinner--gear_container">
          <svg class="machine" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
              viewBox="0 0 645 526">
              <linearGradient id="header-shape-gradient" x2="0.35" y2="1">
                  <stop offset="0%" stop-color="var(--color-stop)" />
                  <stop offset="30%" stop-color="var(--color-stop)" />
                  <stop offset="100%" stop-color="var(--color-bot)" />
              </linearGradient>
              <defs />
              <g>
                  <path x="-173,694" y="-173,694" class="large-shadow"
                      d="M645 194v-21l-29-4c-1-10-3-19-6-28l25-14 -8-19 -28 7c-5-8-10-16-16-24L602 68l-15-15 -23 17c-7-6-15-11-24-16l7-28 -19-8 -14 25c-9-3-18-5-28-6L482 10h-21l-4 29c-10 1-19 3-28 6l-14-25 -19 8 7 28c-8 5-16 10-24 16l-23-17L341 68l17 23c-6 7-11 15-16 24l-28-7 -8 19 25 14c-3 9-5 18-6 28l-29 4v21l29 4c1 10 3 19 6 28l-25 14 8 19 28-7c5 8 10 16 16 24l-17 23 15 15 23-17c7 6 15 11 24 16l-7 28 19 8 14-25c9 3 18 5 28 6l4 29h21l4-29c10-1 19-3 28-6l14 25 19-8 -7-28c8-5 16-10 24-16l23 17 15-15 -17-23c6-7 11-15 16-24l28 7 8-19 -25-14c3-9 5-18 6-28L645 194zM471 294c-61 0-110-49-110-110S411 74 471 74s110 49 110 110S532 294 471 294z" />
              </g>
              <g>
                  <path x="-136,996" y="-136,996" class="medium-shadow"
                      d="M402 400v-21l-28-4c-1-10-4-19-7-28l23-17 -11-18L352 323c-6-8-13-14-20-20l11-26 -18-11 -17 23c-9-4-18-6-28-7l-4-28h-21l-4 28c-10 1-19 4-28 7l-17-23 -18 11 11 26c-8 6-14 13-20 20l-26-11 -11 18 23 17c-4 9-6 18-7 28l-28 4v21l28 4c1 10 4 19 7 28l-23 17 11 18 26-11c6 8 13 14 20 20l-11 26 18 11 17-23c9 4 18 6 28 7l4 28h21l4-28c10-1 19-4 28-7l17 23 18-11 -11-26c8-6 14-13 20-20l26 11 11-18 -23-17c4-9 6-18 7-28L402 400zM265 463c-41 0-74-33-74-74 0-41 33-74 74-74 41 0 74 33 74 74C338 430 305 463 265 463z" />
              </g>
              <g>
                  <path x="-100,136" y="-100,136" class="small-shadow"
                      d="M210 246v-21l-29-4c-2-10-6-18-11-26l18-23 -15-15 -23 18c-8-5-17-9-26-11l-4-29H100l-4 29c-10 2-18 6-26 11l-23-18 -15 15 18 23c-5 8-9 17-11 26L10 225v21l29 4c2 10 6 18 11 26l-18 23 15 15 23-18c8 5 17 9 26 11l4 29h21l4-29c10-2 18-6 26-11l23 18 15-15 -18-23c5-8 9-17 11-26L210 246zM110 272c-20 0-37-17-37-37s17-37 37-37c20 0 37 17 37 37S131 272 110 272z" />
              </g>
              <g>
                  <path x="-100,136" y="-100,136" class="small"
                      d="M200 236v-21l-29-4c-2-10-6-18-11-26l18-23 -15-15 -23 18c-8-5-17-9-26-11l-4-29H90l-4 29c-10 2-18 6-26 11l-23-18 -15 15 18 23c-5 8-9 17-11 26L0 215v21l29 4c2 10 6 18 11 26l-18 23 15 15 23-18c8 5 17 9 26 11l4 29h21l4-29c10-2 18-6 26-11l23 18 15-15 -18-23c5-8 9-17 11-26L200 236zM100 262c-20 0-37-17-37-37s17-37 37-37c20 0 37 17 37 37S121 262 100 262z" />
              </g>
              <g>
                  <path x="-173,694" y="-173,694" class="large"
                      d="M635 184v-21l-29-4c-1-10-3-19-6-28l25-14 -8-19 -28 7c-5-8-10-16-16-24L592 58l-15-15 -23 17c-7-6-15-11-24-16l7-28 -19-8 -14 25c-9-3-18-5-28-6L472 0h-21l-4 29c-10 1-19 3-28 6L405 9l-19 8 7 28c-8 5-16 10-24 16l-23-17L331 58l17 23c-6 7-11 15-16 24l-28-7 -8 19 25 14c-3 9-5 18-6 28l-29 4v21l29 4c1 10 3 19 6 28l-25 14 8 19 28-7c5 8 10 16 16 24l-17 23 15 15 23-17c7 6 15 11 24 16l-7 28 19 8 14-25c9 3 18 5 28 6l4 29h21l4-29c10-1 19-3 28-6l14 25 19-8 -7-28c8-5 16-10 24-16l23 17 15-15 -17-23c6-7 11-15 16-24l28 7 8-19 -25-14c3-9 5-18 6-28L635 184zM461 284c-61 0-110-49-110-110S401 64 461 64s110 49 110 110S522 284 461 284z" />
              </g>
              <g>
                  <path x="-136,996" y="-136,996" class="medium"
                      d="M392 390v-21l-28-4c-1-10-4-19-7-28l23-17 -11-18L342 313c-6-8-13-14-20-20l11-26 -18-11 -17 23c-9-4-18-6-28-7l-4-28h-21l-4 28c-10 1-19 4-28 7l-17-23 -18 11 11 26c-8 6-14 13-20 20l-26-11 -11 18 23 17c-4 9-6 18-7 28l-28 4v21l28 4c1 10 4 19 7 28l-23 17 11 18 26-11c6 8 13 14 20 20l-11 26 18 11 17-23c9 4 18 6 28 7l4 28h21l4-28c10-1 19-4 28-7l17 23 18-11 -11-26c8-6 14-13 20-20l26 11 11-18 -23-17c4-9 6-18 7-28L392 390zM255 453c-41 0-74-33-74-74 0-41 33-74 74-74 41 0 74 33 74 74C328 420 295 453 255 453z" />
              </g>
          </svg>
      </div>
  </div>
                                
    `;
    return markup;
  }

  static createSleepingStat() {
    let markup = `
      <img src="/public/img/sleep.png">
    `;
    return markup;
  }

  static createConfirmWindow(msg) {
    let markup = `
    <div class="confirm--screen">
        <h4>${msg}</h4>
        <btn id="YES">YES</btn>
        <btn id="NO">NO</btn>
    </div>
  `;
    return markup;
  }

  static createProcessWindow() {
    let markup = `
    <div class="loading--screen">
        <h2> Processing</h2>
        <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
    </div>
  `;
    return markup;
  }
}
