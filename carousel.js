// Powers the one-at-a-time photo/video viewer on each hobby page.
// gallery.py builds the markup (a .carousel div with one .carousel-slide per
// file, prev/next buttons, and a counter); this shows one slide at a time,
// wires up the buttons and arrow keys, and keeps the arrows flush against the
// actual visible photo (object-fit: contain can letterbox a portrait photo,
// leaving empty space the arrows would otherwise float over).

document.querySelectorAll(".carousel").forEach(function (carousel) {
  var slides = carousel.querySelectorAll(".carousel-slide");
  var counter = carousel.querySelector(".carousel-counter");
  var prev = carousel.querySelector(".carousel-prev");
  var next = carousel.querySelector(".carousel-next");
  var index = 0;

  function positionArrows() {
    var media = slides[index].querySelector("img, video");
    if (!media || !prev || !next) return;

    var boxW = media.offsetWidth;
    var boxH = media.offsetHeight;
    var natW = media.tagName === "VIDEO" ? media.videoWidth : media.naturalWidth;
    var natH = media.tagName === "VIDEO" ? media.videoHeight : media.naturalHeight;

    // Dimensions aren't known yet (image/video still loading): default to
    // the box edges, and this re-runs once they're available.
    var inset = 0;
    if (natW && natH && boxW && boxH) {
      var visibleWidth = natW / natH > boxW / boxH ? boxW : boxH * (natW / natH);
      inset = Math.max(0, (boxW - visibleWidth) / 2);
    }
    prev.style.left = inset + "px";
    next.style.right = inset + "px";
  }

  function show(i) {
    index = (i + slides.length) % slides.length;
    slides.forEach(function (slide, n) {
      slide.hidden = n !== index;
      if (n !== index) {
        var video = slide.querySelector("video");
        if (video) video.pause();
      }
    });
    if (counter) {
      counter.textContent = (index + 1) + " / " + slides.length;
    }
    positionArrows();
  }

  slides.forEach(function (slide) {
    var media = slide.querySelector("img, video");
    if (!media) return;
    var event = media.tagName === "VIDEO" ? "loadedmetadata" : "load";
    media.addEventListener(event, positionArrows);
  });
  window.addEventListener("resize", positionArrows);

  if (prev) prev.addEventListener("click", function () { show(index - 1); });
  if (next) next.addEventListener("click", function () { show(index + 1); });

  carousel.tabIndex = 0;
  carousel.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });

  positionArrows();
});
