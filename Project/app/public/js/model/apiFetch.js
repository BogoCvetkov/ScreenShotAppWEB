import { apiEndpointMap } from "../config.js";

// Class for fetching the Api. It's not being used directly, but inside the model class.
// Every instance is a different resource./accounts,pages,users, etc./
export class APIResource {
  constructor(resource) {
    this.apiEndpoint = apiEndpointMap[resource];
  }

  // Options parameter contains the url params and query
  async get(options = undefined) {
    let url = this.apiEndpoint;
    if (options && options.url_param !== undefined)
      url = `${url}${options.url_param}`;
    if (options && options.query !== undefined)
      url = `${url}?${options.query}`;
    try {
      const response = await axios.get(url);
      return response;
    } catch (e) {
      throw e;
    }
  }

  // Creating resource
  async post(body = undefined, options = undefined) {
    let url = this.apiEndpoint;
    if (options && options.query !== undefined)
      url = `${url}?${options.query}`;
    try {
      const response = await axios.post(url, body);
      return response;
    } catch (e) {
      throw e;
    }
  }

  // Updating a resource
  async patch(id = undefined, body = undefined) {
    let url;
    id !== undefined
      ? (url = `${this.apiEndpoint}${id}`)
      : (url = `${this.apiEndpoint}`);
    try {
      const response = await axios.patch(url, body);
      return response;
    } catch (e) {
      throw e;
    }
  }

  // Deleting a resource
  async delete(id) {
    let url = `${this.apiEndpoint}${id}`;
    try {
      const response = await axios.delete(url);
      return response;
    } catch (e) {
      throw e;
    }
  }
}
