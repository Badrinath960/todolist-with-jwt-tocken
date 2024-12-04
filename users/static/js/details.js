// tasks.js

// Function to animate the counting of numbers
function animateNumber(id, endValue) {
    let startValue = 0;
    let duration = 1500; // Duration of animation in ms
    let increment = endValue / (duration / 20);  // Adjust the increment
    let currentValue = startValue;

    const element = document.getElementById(id);
    const interval = setInterval(() => {
        currentValue += increment;
        if (currentValue >= endValue) {
            currentValue = endValue; // Ensure final value matches exactly
            clearInterval(interval);
        }
        element.textContent = Math.floor(currentValue);  // Update the displayed value
    }, 20);
}

// Trigger the animation on page load
document.addEventListener('DOMContentLoaded', () => {
    animateNumber('total-tasks', totalTasks);
    animateNumber('completed-tasks', completedTasks);
    animateNumber('pending-tasks', pendingTasks);
});
