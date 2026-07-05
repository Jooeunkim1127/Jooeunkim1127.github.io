(function () {
  "use strict";

  function createCard(work, index) {
    var item = document.createElement("div");
    item.className = "work-item";

    var placeholder = document.createElement("div");
    placeholder.className = "image-placeholder";

    var link = document.createElement("a");
    link.className = "link";
    link.href = "html/" + work.id;

    var img = document.createElement("img");
    img.src = work.thumbSrc;
    img.alt = work.alt || work.title || "Artwork";
    img.decoding = "async";
    if (work.width) {
      img.width = work.width;
    }
    if (work.height) {
      img.height = work.height;
    }
    if (index < 2) {
      img.loading = "eager";
      img.setAttribute("fetchpriority", "high");
    } else {
      img.loading = "lazy";
    }

    link.appendChild(img);
    placeholder.appendChild(link);
    item.appendChild(placeholder);
    return item;
  }

  async function renderIndex() {
    var grid = document.getElementById("works-grid");
    if (!grid || !window.WorksData) {
      return;
    }

    try {
      var works = await window.WorksData.fetchWorks();
      var fragment = document.createDocumentFragment();
      works.forEach(function (work, index) {
        fragment.appendChild(createCard(work, index));
      });
      grid.appendChild(fragment);
    } catch (error) {
      grid.innerHTML = "<p>Unable to load artworks right now.</p>";
      console.error(error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderIndex);
  } else {
    renderIndex();
  }
})();
