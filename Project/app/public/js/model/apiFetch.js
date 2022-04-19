import { apiEndpointMap } from "../config.js";

export class APIResource {
  constructor(resource) {
    this.apiEndpoint = apiEndpointMap[resource];
  }

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

  async patch(id, body = undefined) {
    let url = `${this.apiEndpoint}${id}`;
    try {
      const response = await axios.patch(url, body);
      return response;
    } catch (e) {
      throw e;
    }
  }

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
