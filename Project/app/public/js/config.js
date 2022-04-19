function createAPIDict(prefix) {
  const apiEndpointsDict = {
    accounts: `${prefix}/accounts/`,
    login: `${prefix}/login/`,
    forgetPass: `${prefix}/forget-pass/`,
    resetPass: `${prefix}/reset-pass/`,
    logOut: `${prefix}/logout`,
    me: `${prefix}/me/`,
    pages: `${prefix}/pages/`,
    schedules: `${prefix}/schedules/`,
    services: `${prefix}/service/`,
    users: `${prefix}/users/`,
  };

  return apiEndpointsDict;
}

export const apiEndpointMap = createAPIDict(
  "http://localhost:5000/api"
);
