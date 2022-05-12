export class UsersEventHandler {
  static newUserBtn = document.getElementById("newUser");
  static updateUserBtn = document.getElementById("updateUser");
  static backBtn = document.getElementById("back");
  static usrMenuWrap = document.querySelector(".user_menu-wrapper");
  static usrFormWrap = document.querySelector(".user_form--wrapper");
  static usrGridWrap = document.querySelector(".user_grid--wrapper");

  static showCreateUserFormHandler(handler, innerHandlers) {
    this.newUserBtn.addEventListener("click", () => {
      this.usrMenuWrap.classList.add("hidden");
      handler();
      this._createUserHandler(innerHandlers.createUser);
      this.usrFormWrap.classList.remove("hidden");
    });
  }

  static _createUserHandler(handler) {
    const createBtn = document.getElementById("create");
    createBtn.addEventListener("click", () => {
      const form = this.usrFormWrap.children[0];
      const body = this._getFieldData(form);
      handler("users", body);
    });
  }

  static showUsersGrid(handler, innerHandlers) {
    this.updateUserBtn.addEventListener("click", () => {
      this.usrMenuWrap.classList.add("hidden");
      handler();
      this.usrGridWrap.classList.remove("hidden");
    });
    this._showUpdateUserFormHandler(
      innerHandlers.updateUserForm,
      innerHandlers
    );
  }

  static _showUpdateUserFormHandler(handler, innerHandlers) {
    this.usrGridWrap.addEventListener("click", (e) => {
      if (e.target.tagName === "DIV") return;
      const id = e.target.closest("div").dataset.id;
      this.usrGridWrap.classList.add("hidden");
      handler(id).then(() => {
        this.usrFormWrap.classList.remove("hidden");
        this._updateUserHandler(innerHandlers.updateUser);
      });
    });
  }

  static _updateUserHandler(handler) {
    const updateBtn = document.getElementById("update");
    updateBtn.addEventListener("click", () => {
      const form = this.usrFormWrap.children[0];
      const body = this._getFieldData(form);
      handler("users", form.dataset.id, body);
    });
  }

  static goBackhandler() {
    this.backBtn.addEventListener("click", (e) => {
      const wrappers = document.querySelectorAll(".user--component");
      wrappers.forEach((el) => {
        el.classList.contains("user_menu-wrapper")
          ? el.classList.remove("hidden")
          : el.classList.add("hidden");
      });
    });
  }

  static _getFieldData(form) {
    const fields = form.querySelectorAll("input");
    const body = {};
    for (let field of fields) {
      body[field.name] = field.value;
    }

    return body;
  }
}
