"use strict";
document.addEventListener("DOMContentLoaded", function () {
  Chart.defaults.global.defaultFontColor = "#75787c";
  var r = !0;
  window.outerWidth < 576 && (r = !1);
  const a = document.getElementById("lineChart");
  new Chart(a, {
    type: "line",
    options: {
      scales: {
        xAxes: [{ display: !0, gridLines: { display: !1 } }],
        yAxes: [
          {
            ticks: { max: 60, min: 10 },
            display: !0,
            gridLines: { display: !1 },
          },
        ],
      },
      legend: { display: r },
    },
    data: {
      labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
      datasets: [
        {
          label: "Page Visitors",
          fill: !0,
          lineTension: 0.2,
          backgroundColor: "transparent",
          borderColor: "#864DD9",
          pointBorderColor: "#864DD9",
          pointHoverBackgroundColor: "#864DD9",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0,
          borderJoinStyle: "miter",
          borderWidth: 2,
          pointBackgroundColor: "#fff",
          pointBorderWidth: 5,
          pointHoverRadius: 5,
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 0,
          data: [20, 27, 20, 35, 30, 40, 33, 25, 39],
          spanGaps: !1,
        },
        {
          label: "Page Views",
          fill: !0,
          lineTension: 0.2,
          backgroundColor: "transparent",
          borderColor: "#EF8C99",
          pointBorderColor: "#EF8C99",
          pointHoverBackgroundColor: "#EF8C99",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0,
          borderJoinStyle: "miter",
          borderWidth: 2,
          pointBackgroundColor: "#fff",
          pointBorderWidth: 5,
          pointHoverRadius: 5,
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: [25, 17, 28, 25, 33, 27, 30, 33, 27],
          spanGaps: !1,
        },
      ],
    },
  });
  const e = document.getElementById("barChartExample1");
  new Chart(e, {
    type: "bar",
    options: {
      scales: {
        xAxes: [{ display: !1, gridLines: { color: "#eee" } }],
        yAxes: [{ display: !1, gridLines: { color: "#eee" } }],
      },
    },
    data: {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "Data Set 1",
          backgroundColor: [
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
          ],
          hoverBackgroundColor: [
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
            "rgba(134, 77, 217, 0.57)",
          ],
          borderColor: [
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
            "rgba(134, 77, 217, 1)",
          ],
          borderWidth: 1,
          data: [65, 59, 80, 81, 56, 55, 40],
        },
        {
          label: "Data Set 2",
          backgroundColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          hoverBackgroundColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          borderColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          borderWidth: 1,
          data: [35, 40, 60, 47, 88, 27, 30],
        },
      ],
    },
  });
  const o = document.getElementById("lineChart1");
  new Chart(o, {
    type: "line",
    options: {
      scales: {
        xAxes: [{ display: !0, gridLines: { display: !1 } }],
        yAxes: [
          {
            ticks: { max: 40, min: 10, stepSize: 0.1 },
            display: !1,
            gridLines: { display: !1 },
          },
        ],
      },
      legend: { display: !0 },
    },
    data: {
      labels: [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
      ],
      datasets: [
        {
          label: "Team Drills",
          fill: !0,
          lineTension: 0.3,
          backgroundColor: "transparent",
          borderColor: "#EF8C99",
          pointBorderColor: "#EF8C99",
          pointHoverBackgroundColor: "#EF8C99",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0,
          borderJoinStyle: "miter",
          borderWidth: 2,
          pointBackgroundColor: "#EF8C99",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 0,
          pointRadius: 1,
          pointHitRadius: 0,
          data: [
            20, 21, 25, 22, 24, 18, 20, 23, 19, 22, 25, 19, 24, 27, 22, 17, 20,
            17, 20, 26, 22,
          ],
          spanGaps: !1,
        },
        {
          label: "Team Drills",
          fill: !0,
          lineTension: 0.3,
          backgroundColor: "transparent",
          borderColor: "rgba(238, 139, 152, 0.24)",
          pointBorderColor: "rgba(238, 139, 152, 0.24)",
          pointHoverBackgroundColor: "rgba(238, 139, 152, 0.24)",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0,
          borderJoinStyle: "miter",
          borderWidth: 2,
          pointBackgroundColor: "rgba(238, 139, 152, 0.24)",
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderColor: "#fff",
          pointHoverBorderWidth: 0,
          pointRadius: 1,
          pointHitRadius: 0,
          data: [
            24, 20, 23, 19, 22, 20, 25, 21, 23, 19, 21, 23, 19, 24, 19, 22, 21,
            24, 19, 21, 20,
          ],
          spanGaps: !1,
        },
      ],
    },
  });
  const t = document.getElementById("barChartExample2");
  new Chart(t, {
    type: "bar",
    options: {
      scales: {
        xAxes: [{ display: !1, gridLines: { color: "#eee" } }],
        yAxes: [{ display: !1, gridLines: { color: "#eee" } }],
      },
    },
    data: {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "Data Set 1",
          backgroundColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          hoverBackgroundColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          borderColor: [
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
            "rgba(75, 75, 75, 0.7)",
          ],
          borderWidth: 1,
          data: [65, 59, 80, 81, 56, 55, 40],
        },
        {
          label: "Data Set 2",
          backgroundColor: [
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
          ],
          hoverBackgroundColor: [
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
            "rgba(238, 139, 152, 0.7)",
          ],
          borderColor: [
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
            "rgba(238, 139, 152, 1)",
          ],
          borderWidth: 1,
          data: [35, 40, 60, 47, 88, 27, 30],
        },
      ],
    },
  });
  const d = document.getElementById("pieChartHome1");
  new Chart(d, {
    type: "doughnut",
    options: { cutoutPercentage: 90, legend: { display: !1 } },
    data: {
      labels: ["First", "Second", "Third", "Fourth"],
      datasets: [
        {
          data: [300, 50, 100, 60],
          borderWidth: [0, 0, 0, 0],
          backgroundColor: ["#6933b9", "#8553d1", "#a372ec", "#be9df1"],
          hoverBackgroundColor: ["#6933b9", "#8553d1", "#a372ec", "#be9df1"],
        },
      ],
    },
  });
  const n = document.getElementById("pieChartHome2");
  new Chart(n, {
    type: "doughnut",
    options: { cutoutPercentage: 90, legend: { display: !1 } },
    data: {
      labels: ["First", "Second", "Third", "Fourth"],
      datasets: [
        {
          data: [80, 70, 100, 60],
          borderWidth: [0, 0, 0, 0],
          backgroundColor: ["#9528b9", "#b046d4", "#c767e7", "#e394fe"],
          hoverBackgroundColor: ["#9528b9", "#b046d4", "#c767e7", "#e394fe"],
        },
      ],
    },
  });
  const b = document.getElementById("pieChartHome3");
  new Chart(b, {
    type: "doughnut",
    options: { cutoutPercentage: 90, legend: { display: !1 } },
    data: {
      labels: ["First", "Second", "Third", "Fourth"],
      datasets: [
        {
          data: [120, 90, 77, 95],
          borderWidth: [0, 0, 0, 0],
          backgroundColor: ["#da4d60", "#e96577", "#f28695", "#ffb6c1"],
          hoverBackgroundColor: ["#da4d60", "#e96577", "#f28695", "#ffb6c1"],
        },
      ],
    },
  });
  const l = document.getElementById("salesBarChart1");
  new Chart(l, {
    type: "bar",
    options: {
      scales: {
        xAxes: [{ display: !1, barPercentage: 0.2 }],
        yAxes: [{ display: !1 }],
      },
      legend: { display: !1 },
    },
    data: {
      labels: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
      datasets: [
        {
          label: "Data Set 1",
          backgroundColor: [
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
          ],
          borderColor: [
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
            "#EF8C99",
          ],
          borderWidth: 0.2,
          data: [35, 55, 65, 85, 40, 30, 18, 35, 20, 70],
        },
      ],
    },
  });
  const i = document.getElementById("salesBarChart2");
  new Chart(i, {
    type: "bar",
    options: {
      scales: {
        xAxes: [{ display: !1, barPercentage: 0.2 }],
        yAxes: [{ display: !1 }],
      },
      legend: { display: !1 },
    },
    data: {
      labels: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
      datasets: [
        {
          label: "Data Set 1",
          backgroundColor: [
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
          ],
          borderColor: [
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
            "#CF53F9",
          ],
          borderWidth: 0.2,
          data: [44, 75, 65, 34, 60, 45, 22, 35, 30, 63],
        },
      ],
    },
  });
  const s = document.getElementById("visitPieChart");
  new Chart(s, {
    type: "pie",
    options: { legend: { display: !1 } },
    data: {
      labels: ["A", "B", "C", "D"],
      datasets: [
        {
          data: [300, 50, 100, 80],
          borderWidth: 0,
          backgroundColor: ["#723ac3", "#864DD9", "#9762e6", "#a678eb"],
          hoverBackgroundColor: ["#723ac3", "#864DD9", "#9762e6", "#a678eb"],
        },
      ],
    },
  });
});
