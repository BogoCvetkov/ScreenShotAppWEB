export class EventHandlers {
  static searchBtn = document.querySelector(".btn--search");
  static filterMenuBtn = document.getElementById("filterBtn");
  static filterMenu = document.getElementById("filterMenu");
  static addFilterBtn = document.getElementById("add-filter");
  static clearFilterBtn = document.getElementById("clear-filters");
  static filterCounter = document.getElementById("filterCounter");

  static searchHandler(handler) {
    const searchField = document.getElementById("search");

    this.searchBtn.addEventListener("click", (e) => {
      let query = "";
      // Default search field in the input element is for /name/
      query = `name=${searchField.value}`;

      const filterRows = document.querySelectorAll(".filter__row");
      for (let row of filterRows) {
        const field = row.children[0].lastChild;
        const operator = row.children[1].lastChild;
        let value = row.children[2].lastChild;

        // Transform to timestamp
        if (value.type === "datetime-local") {
          value = new Date(value.value).getTime() / 1000;
        } else {
          value = value.value;
        }

        if (["includes", "is"].includes(operator.textContent)) {
          query = `${query}&${field.value}=${value}`;
        } else {
          query = `${query}&${field.value}=${operator.value},${value}`;
        }
      }
      console.log(query);

      handler(query);
    });
  }

  static filterMenuHandler() {
    this.filterMenuBtn.addEventListener("click", (e) => {
      this.filterMenu.parentElement.classList.toggle("hidden");
    });
  }

  static addFilterHandler(handler) {
    this.addFilterBtn.addEventListener("click", (e) => {
      handler();
      this.filterCounter.classList.remove("hidden");
      this.filterCounter.textContent =
        this.filterMenu.children.length;
    });
  }

  static filterOperatorHandler() {
    this.filterMenu.addEventListener("change", (e) => {
      if (e.target.className != "filter--field") return;

      const filterOperator =
        e.target.parentElement.nextSibling.lastChild;
      const filterInput =
        e.target.parentElement.nextSibling.nextSibling.lastChild;
      const selectedField = e.target.children[e.target.selectedIndex];
      filterOperator.innerHTML = "";

      filterInput.type = "text";
      filterInput.placeholder = "Filter value";

      if (selectedField.dataset.type === "int") {
        const operators = [">", "<", "="];

        for (let op of operators) {
          const option = document.createElement("option");
          [option.value, option.textContent] = [op, op];
          filterOperator.append(option);
        }
      } else if (selectedField.dataset.type === "str") {
        const option = document.createElement("option");
        [option.value, option.textContent] = ["=", "includes"];
        filterOperator.append(option);
      } else if (selectedField.dataset.type === "bool") {
        const option = document.createElement("option");
        [option.value, option.textContent] = ["=", "is"];
        filterOperator.append(option);
        filterInput.placeholder = "True / False";
      } else if (selectedField.dataset.type === "date") {
        filterInput.type = "datetime-local";
        filterInput.required = true;
        const operators = [">", "<"];

        for (let op of operators) {
          const option = document.createElement("option");
          [option.value, option.textContent] = [op, op];
          filterOperator.append(option);
        }
      }
    });
  }

  static clearFiltersHandler() {
    this.clearFilterBtn.addEventListener("click", (e) => {
      this.filterMenu.innerHTML = "";
      this.filterCounter.classList.add("hidden");
      this.filterCounter.textContent = "";
    });
  }
}
