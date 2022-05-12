import { ResourceMenu } from "./components/menu.js";

// Contains the view for the Users Page
export class UsersView {
  static generateCreateUserForm() {
    const container = document.querySelector(".user_form--wrapper");
    container.innerHTML = "";
    container.insertAdjacentHTML(
      "beforeend",
      ResourceMenu.generateCreateUserForm()
    );
  }

  static generateUsersGrid(data) {
    const container = document.querySelector(
      ".user_grid--wrapper .user--grid"
    );
    container.innerHTML = "";
    for (let user of data) {
      container.insertAdjacentHTML(
        "beforeend",
        ResourceMenu.generateUsersGridElement(user)
      );
    }
  }

  static generateUpdateUserForm(data) {
    const container = document.querySelector(".user_form--wrapper");
    container.innerHTML = "";
    container.insertAdjacentHTML(
      "beforeend",
      ResourceMenu.generateUpdateUserForm(data)
    );
  }
}
