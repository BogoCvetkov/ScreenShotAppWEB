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
                        <input type="text">
                    </div>
                    <div class="resource--field">
                        <p>Account Email</p>
                        <input type="email">
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
      <div class="status--dot dot-green">
        <div class="status--dot dot-green ringring-green"></div>
      </div>
        `;
    } else {
      markup = `
      <div class="status--dot dot-red">
        <div class="status--dot dot-red ringring-red"></div>
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
    <div class="schedule__wrapper top--layer ">
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
}
