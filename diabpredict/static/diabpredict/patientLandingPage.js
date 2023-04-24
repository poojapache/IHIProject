// document.querySelector('link[rel="icon"]').addEventListener('click', function() {
//     window.location.href = "/";
// });
var patientClick = false;
var doctorClick = false;
$('input#genhealthSlider').after('<output for="foo1" onforminput="value = foo1.valueAsNumber;"></output>');
$('input#educationSlider').after('<output for="foo2" onforminput="value = foo2.valueAsNumber;"></output>');
$('input#incomeSlider').after('<output for="foo3" onforminput="value = foo3.valueAsNumber;"></output>');

function viewQuestions()
{
    if(!patientClick)
    {
        document.getElementById('questionnaire').style.display = "none";
        document.getElementById('predictBtn').style.backgroundColor = "#9FA3F2";
        document.getElementById('predictBtn').style.color = "#000";
        patientClick = true;
    }
    else
    {
        document.getElementById('questionnaire').style.display = "block";
        document.getElementById('predictBtn').style.backgroundColor = "#4a50d2";
        document.getElementById('predictBtn').style.color = "#FFF";
        patientClick = false;
    }
}

function viewPatients()
{
  if(!doctorClick)
  {
      document.getElementById('patientsList').style.display = "none";
      document.getElementById('viewPatientBtn').style.backgroundColor = "#9FA3F2";
      document.getElementById('viewPatientBtn').style.color = "#000";
      doctorClick = true;
  }
  else
  {
      document.getElementById('patientsList').style.display = "block";
      document.getElementById('viewPatientBtn').style.backgroundColor = "#4a50d2";
      document.getElementById('viewPatientBtn').style.color = "#FFF";
      doctorClick = false;
  }
}

function accordion()
{
  var acc = document.getElementsByClassName("accordion");
  var i;

  for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
      /* Toggle between adding and removing the "active" class,
      to highlight the button that controls the panel */
      this.classList.toggle("active");
      /* Toggle between hiding and showing the active panel */
      var panel = this.nextElementSibling;
      if (panel.style.display == "block") {
        panel.style.display = "none";
      } else {
        panel.style.display = "block";
      }
    });
  }
}
// var slider = document.getElementById("myRange");
// var output = document.getElementById("space");
// output.innerHTML = slider.value;

// slider.oninput = function() {
//   output.innerHTML = this.value;
// }


function modifyOffset() {
    var el, newPoint, newPlace, offset, siblings, k;
    width    = this.offsetWidth;
    newPoint = (this.value - this.getAttribute("min")) / (this.getAttribute("max") - this.getAttribute("min"));
    offset   = -1;
    if (newPoint < 0) { newPlace = 0;  }
    else if (newPoint > 1) { newPlace = width; }
    else { newPlace = width * newPoint + offset; offset -= newPoint;}
    siblings = this.parentNode.childNodes;
    for (var i = 0; i < siblings.length; i++) {
      sibling = siblings[i];
      if (sibling.id == this.id) { k = true; }
      if ((k == true) && (sibling.nodeName == "OUTPUT")) {
        outputTag = sibling;
      }
    }
    outputTag.style.left       = newPlace + "px";
    outputTag.style.marginLeft = offset + "%";
    outputTag.innerHTML        = this.value;
  }
  
  function modifyInputs() {
      
    var inputs = document.getElementsByTagName("input");
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].getAttribute("type") == "range") {
        inputs[i].onchange = modifyOffset;
  
        if ("fireEvent" in inputs[i]) {
            inputs[i].fireEvent("onchange");
        } else {
            var evt = document.createEvent("HTMLEvents");
            evt.initEvent("change", false, true);
            inputs[i].dispatchEvent(evt);
        }
      }
    }
  }
  
  modifyInputs();