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

export const apiEndpointMap = createAPIDict(`${location.origin}/api`);
