import { UsersEventHandler } from "../../view/eventhandlers/usersHandlers.js";
import * as cb from "../callbacks.js";

UsersEventHandler.showCreateUserFormHandler(
  cb.controllShowCreateUserForm,
  {
    createUser: cb.controllCreateResource,
  }
);

UsersEventHandler.showUsersGrid(cb.controllGetAllUsers, {
  updateUserForm: cb.controllShowUpdateUserForm,
  updateUser: cb.controllUpdateResource,
});

UsersEventHandler.goBackhandler();
