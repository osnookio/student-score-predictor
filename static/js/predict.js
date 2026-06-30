/* predict.js */

const hoursInput  = document.getElementById("hours");
const attInput    = document.getElementById("attendance");
const hoursVal    = document.getElementById("hours-val");
const attVal      = document.getElementById("att-val");
const predictBtn  = document.getElementById("predict-btn");
const errMsg      = document.getElementById("err-msg");
const resultIdle  = document.getElementById("result-idle");
const resultData  = document.getElementById("result-data");
const scoreNum    = document.getElementById("score-num");
const gradeBadge  = document.getElementById("grade-badge");
const resultMsg   = document.getElementById("result-msg");
const resultInputs= document.getElementById("result-inputs");
const ringFill    = document.getElementById("ring-fill");

const CIRCUMFERENCE = 2 * Math.PI * 50;

// ── Sliders ────────────────────────────────────────────────────────
hoursInput.addEventListener("input", () => {
  hoursVal.textContent = `${hoursInput.value} hrs`;
});
attInput.addEventListener("input", () => {
  attVal.textContent = `${attInput.value}%`;
});

// ── Grade colour map ───────────────────────────────────────────────
const gradeColour = {
  "A+": "#22c55e",
  "A":  "#4ade80",
  "B":  "#60a5fa",
  "C":  "#f59e0b",
  "D":  "#fb923c",
  "F":  "#ef4444",
};

// ── Predict ────────────────────────────────────────────────────────
predictBtn.addEventListener("click", async () => {
  errMsg.textContent = "";
  predictBtn.textContent = "Predicting…";
  predictBtn.disabled = true;

  const hours      = parseFloat(hoursInput.value);
  const attendance = parseFloat(attInput.value);

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hours, attendance }),
    });

    const data = await res.json();

    if (!res.ok) {
      errMsg.textContent = data.error || "Something went wrong.";
      return;
    }

    showResult(data, hours, attendance);

  } catch (e) {
    errMsg.textContent = "Network error – please try again.";
  } finally {
    predictBtn.textContent = "Predict my score ✦";
    predictBtn.disabled = false;
  }
});

function showResult(data, hours, attendance) {
  const { score, grade, message } = data;
  const colour = gradeColour[grade] || "#4f8ef7";

  resultIdle.classList.add("hidden");
  resultData.classList.remove("hidden");

  // Animate number count-up
  let current = 0;
  const target = score;
  const step   = target / 40;
  const timer  = setInterval(() => {
    current = Math.min(current + step, target);
    scoreNum.textContent = current.toFixed(1);
    if (current >= target) {
      scoreNum.textContent = target;
      clearInterval(timer);
    }
  }, 25);

  // Animate ring
  const offset = CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE;
  ringFill.style.strokeDashoffset = offset;
  ringFill.style.stroke = colour;

  // Grade badge
  gradeBadge.textContent = `Grade: ${grade}`;
  gradeBadge.style.background = colour + "22";
  gradeBadge.style.borderColor = colour + "66";
  gradeBadge.style.color = colour;

  resultMsg.textContent = message;

  resultInputs.innerHTML = `
    <span>📖 ${hours} hrs / day</span>
    <span>📅 ${attendance}% attendance</span>
  `;
}