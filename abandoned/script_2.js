document.getElementById("predictButton").addEventListener("click", function () {
  var formData = {
    Age: document.getElementById("age").value,
    Gender: document.getElementById("gender").value,
    "Job Title": document.getElementById("jobTitle").value,
    "Years of Experience": document.getElementById("yearsExperience").value,
    Country: document.getElementById("companyNation").value,
    "Education Level": document.getElementById("educationLevel").value,
  };

  document.getElementById("predictionForm").style.display = "none";
  document.getElementById("loading").style.display = "block";

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("loading").style.display = "none";
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerHTML =
        "Predicted Salary: $" + data.predicted_salary.toFixed(2);
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("loading").style.display = "none";
      document.getElementById("result").style.display = "block";
      document.getElementById("result").innerHTML =
        "An error occurred: " + error.message;
    });
});
