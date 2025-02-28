// For home.html
const bookButton = document.getElementById("bookButton");
if (bookButton) {
  bookButton.addEventListener("click", function () {
    alert("Choose a room that you like!");
    document.querySelector("#rooms").scrollIntoView({ behavior: "smooth" });
  });
}

// For the rooms lightbox
const galleryButton = document.getElementById("galleryButton");
const galleryContainer = document.getElementById("gallery-container");
const galleryItem = document.getElementsByClassName("gallery-item");
const lightBoxContainer = document.createElement("div");
const lightBoxContent = document.createElement("div");
const lightBoxImg = document.createElement("img");
const lightBoxPrev = document.createElement("div");
const lightBoxNext = document.createElement("div");
const lightBoxClose = document.createElement("div");

lightBoxContainer.classList.add("lightbox");
lightBoxContent.classList.add("lightbox-content");

lightBoxPrev.textContent = "🡸";
lightBoxNext.textContent = "🡺";
lightBoxClose.textContent = "𝙓";

lightBoxPrev.classList.add("lightbox-prev");
lightBoxNext.classList.add("lightbox-next");
lightBoxClose.classList.add("lightbox-close");

lightBoxContainer.appendChild(lightBoxContent);
lightBoxContent.appendChild(lightBoxImg);
lightBoxContent.appendChild(lightBoxPrev);
lightBoxContent.appendChild(lightBoxNext);
lightBoxContainer.appendChild(lightBoxClose);

document.body.appendChild(lightBoxContainer);

let index = 1;

function showLightBox(n) {
  if (n > galleryItem.length) {
    index = 1;
  } else if (n < 1) {
    index = galleryItem.length;
  }
  let imageLocation = galleryItem[index - 1].children[0].getAttribute("src");
  lightBoxImg.setAttribute("src", imageLocation);
  lightBoxContainer.style.display = "block";
}

document.addEventListener("DOMContentLoaded", function () {
  const galleryButton = document.getElementById("galleryButton");
  const galleryContainer = document.getElementById("gallery-container");

  if (galleryButton && galleryContainer) {
    galleryButton.addEventListener("click", function () {
      const currentDisplay = window.getComputedStyle(galleryContainer).display;

      if (currentDisplay === "block") {
        galleryContainer.style.display = "none";
      } else {
        galleryContainer.style.display = "block";
        showLightBox(index);
      }
    });
  }
});

function currentImage() {
  let imageIndex = parseInt(this.getAttribute("data-index"));
  showLightBox((index = imageIndex));
}

for (let i = 0; i < galleryItem.length; i++) {
  galleryItem[i].addEventListener("click", currentImage);
}

function sliderImage(n) {
  showLightBox((index += n));
}

function prevImage() {
  sliderImage(-1);
}

function nextImage() {
  sliderImage(1);
}

lightBoxPrev.addEventListener("click", prevImage);
lightBoxNext.addEventListener("click", nextImage);

lightBoxClose.addEventListener("click", function () {
  lightBoxContainer.style.display = "none";
  galleryContainer.style.display = "none";
});

function closeLightBox() {
  lightBoxContainer.style.display = "none";
  galleryContainer.style.display = "none";
}
lightBoxClose.addEventListener("click", closeLightBox);

lightBoxContent.addEventListener("click", function (event) {
  event.stopPropagation();
});

// For calendar
let today = new Date();
let day = String(today.getDate()).padStart(2, "0");
let month = String(today.getMonth() + 1).padStart(2, "0");
let year = String(today.getFullYear());
let formattedDate = `${day}-${month}-${year}`;

let minDate = `${year}-${month}-${day}`;
let checkIn = document.getElementById("checkIn");
let checkOut = document.getElementById("checkOut");

if (checkIn) checkIn.setAttribute("min", minDate);
if (checkOut) checkOut.setAttribute("min", minDate);
if (checkIn) checkIn.setAttribute("placeholder", "Check-in");
if (checkOut) checkOut.setAttribute("placeholder", "Check-out");

checkIn.addEventListener("change", function () {
  checkOut.setAttribute("min", this.value);
});

document.querySelectorAll("input[type='date']").forEach((input) => {
  input.addEventListener("focus", function () {
    this.removeAttribute("placeholder");
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const roomTitle = document.getElementById("room-title");
  const roomName = document.getElementById("room-name");
  const roomSize = document.getElementById("room-size");
  const roomDescription = document.getElementById("room-description");
  const roomPrice = document.getElementById("room-price");
  const roomBackground = document.getElementById("room-background");
  const galleryContainer = document.getElementById("gallery-container");

  // Extract room ID from the URL path (e.g., /room/101/)
  const pathSegments = window.location.pathname.split("/");
  const roomNumber = pathSegments[pathSegments.length - 2]; // Get the second-to-last segment (room ID)

  console.log("🔍 Selected Room Number:", roomNumber); // Debugging

  if (!roomNumber || !ROOMS[roomNumber]) {
    console.error(`🚫 Room not found or missing room number: ${roomNumber}`);
    roomTitle.innerText = "Room not found!";
    roomName.innerText = "Sorry, we couldn't find this room.";
    return; // Exit early if the room number is invalid or missing.
  }

  const room = ROOMS[roomNumber]; // Get the room object from the dictionary

  roomTitle.innerText = room.name;
  roomName.innerText = room.name;
  roomSize.innerHTML = room.size;
  roomDescription.innerText = room.description;
  roomPrice.innerText = room.price;
  roomBackground.style.backgroundImage = `url('${room.bckgImage}')`;

  if (room.gallery.length > 0) {
    galleryContainer.innerHTML = room.gallery
      .map(
        (img) =>
          `<div class='gallery-item'><img src='${img}' alt='Room' class='image'/></div>`
      )
      .join("");
  } else {
    galleryContainer.innerHTML = "<p>No images available</p>";
  }
});
