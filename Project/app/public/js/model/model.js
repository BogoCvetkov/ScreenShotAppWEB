import { APIResource } from "./apiFetch.js";

// Data class used for transforming the api json response
class Data {
  constructor(data) {
    this.data = data;
  }

  // Transform the date fields to Date objects
  get transformedData() {
    for (let el of this.data.data) {
      if (el["last_scraped"])
        el["last_scraped"] = new Date(
          el["last_scraped"]
        ).toLocaleString();

      if (el["last_emailed"])
        el["last_emailed"] = new Date(
          el["last_emailed"]
        ).toLocaleString();
    }
    return this.data;
  }
}

// Uses and instance of APIResource to fetch data
export class Model {
  constructor(apiResource) {
    this.api = apiResource;
  }

  async getResources(options = undefined) {
    const response = await this.api.get(options);
    let data = new Data(response.data);
    return data.transformedData;
  }

  async createResource(body = undefined) {
    const response = await this.api.post(body);
    let data = new Data(response.data);
    return data.transformedData;
  }

  async updateResource(id, body = undefined) {
    const response = await this.api.patch(id, body);
    let data = new Data(response.data);
    return data.transformedData;
  }

  async deleteResource(id) {
    const response = await this.api.delete(id);
    let data = new Data(response.data);
    return data.transformedData;
  }
}
