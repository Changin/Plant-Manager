document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startButton');
    startButton.addEventListener('click', () => {
        window.location.href = '/poll/survey'; // 설문조사 페이지 URL로 변경
    });
});
