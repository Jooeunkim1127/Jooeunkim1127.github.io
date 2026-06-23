(function () {
  "use strict";
  var worksPromise = null;

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function mediaLinesToHtml(lines) {
    if (!Array.isArray(lines) || lines.length === 0) {
      return "";
    }
    return lines.map(escapeHtml).join("<br>");
  }

  function startWorksFetch() {
    if (!worksPromise) {
      worksPromise = fetch("data/works.json")
        .then(function (response) {
          if (!response.ok) {
            throw new Error("Failed to load works.json");
          }
          return response.json();
        })
        .catch(function (error) {
          worksPromise = null;
          throw error;
        });
    }
    return worksPromise;
  }

  function fetchWorks() {
    return startWorksFetch();
  }

  // Start loading data as soon as this script is parsed.
  startWorksFetch();

  window.WorksData = {
    fetchWorks: fetchWorks,
    mediaLinesToHtml: mediaLinesToHtml,
  };
})();
