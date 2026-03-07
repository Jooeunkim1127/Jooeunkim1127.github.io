(function () {
  "use strict";

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

  async function fetchWorks() {
    var response = await fetch("data/works.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error("Failed to load works.json");
    }
    return response.json();
  }

  window.WorksData = {
    fetchWorks: fetchWorks,
    mediaLinesToHtml: mediaLinesToHtml,
  };
})();
