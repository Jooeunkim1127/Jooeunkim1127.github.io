(function () {
  "use strict";

  function pickWork(works, id) {
    return works.find(function (work) {
      return work.id === id || work.id === id + ".html";
    });
  }

  function renderMissing(container) {
    container.innerHTML =
      "<p>Artwork not found. <a href='index.html'>Back to Works</a></p>";
  }

  function renderWork(container, work) {
    var wrapper = document.createElement("div");

    var img = document.createElement("img");
    img.className = "work-expanded";
    img.src = work.fullSrc || work.thumbSrc;
    img.alt = work.alt || work.title || "Artwork";
    if (work.width) {
      img.width = work.width;
    }
    if (work.height) {
      img.height = work.height;
    }

    var mediaInfo = document.createElement("div");
    mediaInfo.id = "media_info";

    var spacer = document.createTextNode("\u00A0");
    var p = document.createElement("p");
    p.innerHTML = window.WorksData.mediaLinesToHtml(work.mediaLines || [work.title]);

    mediaInfo.appendChild(spacer);
    mediaInfo.appendChild(p);

    wrapper.appendChild(img);
    wrapper.appendChild(mediaInfo);
    container.replaceChildren(wrapper);

    if (work.title) {
      document.title = "Jooeun Kim - " + work.title;
    }
  }

  async function init() {
    var container = document.getElementById("work-detail");
    if (!container || !window.WorksData) {
      return;
    }

    var params = new URLSearchParams(window.location.search);
    var id = params.get("id");
    if (!id) {
      renderMissing(container);
      return;
    }

    try {
      var works = await window.WorksData.fetchWorks();
      var work = pickWork(works, id);
      if (!work) {
        renderMissing(container);
        return;
      }
      renderWork(container, work);
    } catch (error) {
      container.innerHTML = "<p>Unable to load artwork right now.</p>";
      console.error(error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
