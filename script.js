function formatSalary(salary) {
  return parseInt(salary).toLocaleString();
}

function calculatePppSalary(
  originalSalary,
  countryBigMacPrice,
  koreaBigMacPrice
) {
  var bigMacIndex = countryBigMacPrice / koreaBigMacPrice;
  var pppSalary = originalSalary / bigMacIndex;
  return pppSalary;
}

function showLoader() {
  var loader = document.getElementById("loader");
  loader.style.display = "block";
  setTimeout(function () {
    loader.classList.add("loader-visible");
  }, 100);
}

function hideLoader() {
  var loader = document.getElementById("loader");
  loader.classList.remove("loader-visible");
  setTimeout(function () {
    loader.style.display = "none";
  }, 500);
}

function fadeIn(element, duration) {
  element.style.opacity = 0;
  element.style.display = "block";

  var last = +new Date();
  var tick = function () {
    element.style.opacity =
      +element.style.opacity + (new Date() - last) / duration;
    last = +new Date();

    if (+element.style.opacity < 1) {
      (window.requestAnimationFrame && requestAnimationFrame(tick)) ||
        setTimeout(tick, 16);
    }
  };

  tick();
}

function getCountryBigMacPriceInKRW(companyNation) {
  switch (companyNation) {
    case "0": // Australia
      return 4.97 * 1317;
    case "1": // China
      return 3.5 * 1317;
    case "2": // Canada
      return 4.57 * 1317;
    case "3": // UK
      return 6.67 * 1317;
    case "4": // USA
      return 5.58 * 1317;
    default:
      return 5500; // 기본값으로 한국 가격 설정
  }
}

function predictSalary() {
  function getSelectedOptionText(selectElementId) {
    var selectElement = document.getElementById(selectElementId);
    return selectElement.options[selectElement.selectedIndex].text;
  }
  var userData = {
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    companyNation: document.getElementById("companyNation").value,
    educationLevel: document.getElementById("educationLevel").value,
    jobTitle: document.getElementById("jobTitle").value,
    yearsExperience: document.getElementById("yearsExperience").value,
  };

  var userCondition = {
    age: document.getElementById("age").value,
    gender: getSelectedOptionText("gender"), // 성별 텍스트
    companyNation: getSelectedOptionText("companyNation"), // 회사 국적 텍스트
    educationLevel: getSelectedOptionText("educationLevel"), // 최종 학력 텍스트
    jobTitle: getSelectedOptionText("jobTitle"), // 직업 명 텍스트
    yearsExperience: document.getElementById("yearsExperience").value,
  };

  document.getElementById("title2").style.display = "none";
  document.getElementById("bigMacIndexExplanation").style.display = "none";
  document.getElementById("predictionForm").style.display = "none";
  showLoader();

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  })
    .then((response) => response.json())
    .then((data) => {
      setTimeout(function () {
        hideLoader();
        var originalSalary = parseFloat(data.predictedSalary);
        var formattedSalary = formatSalary(originalSalary);

        var koreaBigMacPrice = 5500; // 한국 빅맥 가격 (원)
        var countryBigMacPriceInKRW; // 해당 국가 빅맥 가격 (원으로 환산)
        // 국가별 빅맥 가격 설정
        switch (userData.companyNation) {
          case "0":
            countryBigMacPriceInKRW = 4.97 * 1317;
            break;
          case "1":
            countryBigMacPriceInKRW = 3.5 * 1317;
            break;
          case "2":
            countryBigMacPriceInKRW = 4.57 * 1317;
            break;
          case "3":
            countryBigMacPriceInKRW = 6.67 * 1317;
            break;
          case "4":
            countryBigMacPriceInKRW = 5.58 * 1317;
            break;
          default:
            countryBigMacPriceInKRW = koreaBigMacPrice;
        }

        var pppSalary = calculatePppSalary(
          originalSalary * 1317,
          countryBigMacPriceInKRW,
          koreaBigMacPrice
        );
        var formattedPppSalary = formatSalary(pppSalary);

        setTimeout(() => {
          document.getElementById("userInput").innerHTML = `
        <p>나이: ${userCondition.age}</p>
        <p>성별: ${userCondition.gender}</p> 
        <p>회사 국적: ${userCondition.companyNation}</p>
        <p>최종 학력: ${userCondition.educationLevel}</p>
        <p>직업 명: ${userCondition.jobTitle}</p>
        <p>경력: ${userCondition.yearsExperience}년</p>
      `;
          var salaryContainer = document.getElementById(
            "predictedSalaryContainer"
          );
          document.getElementById("bicmacDescription").innerText = parseFloat(
            countryBigMacPriceInKRW / koreaBigMacPrice
          ).toFixed(2);
          document.getElementById("predictedSalary").innerText =
            formattedSalary;
          document.getElementById("pppSalary").innerText = formattedPppSalary;
          fadeIn(salaryContainer, 500);
          var container = document.getElementById("container");
          document.getElementById("container").style.background = "#fff";
          document.getElementById("container").style.borderRadius = "8px";
          document.getElementById("container").style.border = "3px dashed #000";
          document.getElementById("container").style.width = "80%";
          document.getElementById("container").style.marginLeft = "auto";
          document.getElementById("container").style.marginRight = "auto";
          fadeIn(container, 500);
          document.getElementById("container").style.display = "flex";
          document.getElementById("container").style.marginTop = "3.5%";
          fetch("http://127.0.0.1:5000/predictSalaryByExperience", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
          })
            .then((response) => response.json())
            .then((salaryDataByExperience) => {
              // 경력 연수별 연봉 데이터를 처리하는 로직
              drawSalaryChart(
                salaryDataByExperience,
                countryBigMacPriceInKRW,
                koreaBigMacPrice
              );
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        }, 500);
      }, 2000);
      // document.getElementById("leftColumn").style.padding = "5%";
      document.getElementById("rightColumn").style.margin = "auto";
      // document.getElementById("rightColumn").style.padding = "10%";
    })
    .catch((error) => {
      console.error("Error:", error);
      hideLoader();
    });
}

function drawSalaryChart(
  experienceData,
  countryBigMacPriceInKRW,
  koreaBigMacPrice
) {
  const labels = Object.keys(experienceData).map((year) => `${year}년 경력`);
  const predictedSalaryData = Object.values(experienceData).map((salary) =>
    parseInt(salary * 1317)
  );
  const pppSalaryData = predictedSalaryData.map((salary) =>
    parseInt(salary / (countryBigMacPriceInKRW / koreaBigMacPrice))
  );

  var ctx = document.getElementById("experienceSalaryChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "예상 연봉",
          data: predictedSalaryData,
          backgroundColor: "rgba(126,220,230,255)", // 바 차트 색상 설정
          borderColor: "rgb(75, 192, 192)",
          borderWidth: 1,
        },
        {
          label: "체감 연봉",
          data: pppSalaryData,
          backgroundColor: "rgba(255, 99, 132, 0.5)", // 바 차트 색상 설정
          borderColor: "rgb(255, 99, 132)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
