function createAPIDict(prefix) {
  const apiEndpointsDict = {
    accounts: `${prefix}/accounts/`,
    login: `${prefix}/login/`,
    forgetPass: `${prefix}/forget-pass/`,
    resetPass: `${prefix}/reset-pass/`,
    logOut: `${prefix}/logout`,
    me: `${prefix}/me/`,
    pages: `${prefix}/pages/`,
    keywords: `${prefix}/keywords/`,
    schedules: `${prefix}/schedules/`,
    services: `${prefix}/service/`,
    users: `${prefix}/users/`,
    logs: `${prefix}/logs/`,
  };

  return apiEndpointsDict;
}

//// Local Host Config
// export const apiEndpointMap = createAPIDict(
//   "http://localhost:5000/api"
// );

// Production Config
export const apiEndpointMap = createAPIDict(
  "http://46.41.136.0:5000/api"
);
