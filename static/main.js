// HTML elements


const imageDisplay = document.getElementById("showImage");
const prevImg = document.getElementById("prevImage");
const uploadCaption = document.getElementById("upload-caption");
const predResult = document.getElementById("classResult");
const predDescr = document.getElementById("descriptionResult");
const upload = document.getElementById("upload");

upload.addEventListener("change", fileSelectPreviewFile, false);


function fileSelectPreviewFile(d) {
  
  var files = d.target.files || d.dataTransfer.files;
 
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);

  }
}


//events functions
function classifyImage() {

  if (!imageDisplay.src) {
    window.alert("Upload an image.");
    return;
  }

  // call the predict function of the backend
  predictImage(imageDisplay.src);
}

function clearField() {
  
  upload.value = "";
  prevImg.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";
  predDescr.innerHTML = "";

  hide(prevImg);
  hide(imageDisplay);
  hide(predResult);
  hide(predDescr);
  show(uploadCaption);

}

function previewFile(file) {
   
  var filereaderinstance = new FileReader();
  filereaderinstance.readAsDataURL(file);
  filereaderinstance.onloadend = () => {
    prevImg.src = URL.createObjectURL(file);

    // reset
    predResult.innerHTML = "";

    displayImage(filereaderinstance.result, "showImage");
  };
}

// FETCH
function predictImage(image) {

    fetch("/classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(image)
    })
      .then(resp => {
        if (resp.ok)
          resp.json().then(data => {
            displayResult(data);
          });
      })
      .catch(err => {
        console.log("Error", err.message);
      });
  }

function displayImage(image, id) {

  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
 
  predResult.innerHTML = data.result;
  predDescr.innerHTML = data.description;
  show(predResult);
  show(predDescr);
}

function hide(d) {
 d.classList.add("hidden");
}

function show(d) {
  d.classList.remove("hidden");
}