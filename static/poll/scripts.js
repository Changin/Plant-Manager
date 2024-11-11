document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const categories = document.querySelectorAll('.category');
    const nextButton = document.getElementById('nextButton');
    const prevButton = document.getElementById('prevButton');
    const submitButton = document.getElementById('submitButton');
    let currentCategory = 0;

    categories[currentCategory].classList.add('active');
    nextButton.classList.add('first-page');

    nextButton.addEventListener('click', () => {
        if (currentCategory < categories.length - 1) {
            categories[currentCategory].classList.remove('active');
            currentCategory++;
            categories[currentCategory].classList.add('active');
        }
        updateButtons();
    });

    prevButton.addEventListener('click', () => {
        if (currentCategory > 0) {
            categories[currentCategory].classList.remove('active');
            currentCategory--;
            categories[currentCategory].classList.add('active');
        }
        updateButtons();
    });

    function updateButtons() {
        if (currentCategory === 0) {
            prevButton.style.display = 'none';
            nextButton.classList.add('first-page');
        } else {
            prevButton.style.display = 'inline-block';
            nextButton.classList.remove('first-page');
        }

        if (currentCategory === categories.length - 1) {
            nextButton.style.display = 'none';
            submitButton.style.display = 'inline-block';
        } else {
            nextButton.style.display = 'inline-block';
            submitButton.style.display = 'none';
        }
    }

    form.addEventListener('submit', (e) => {
        const questions = form.querySelectorAll('.question');
        let allAnswered = true;

        questions.forEach((question) => {
            const radios = question.querySelectorAll('input[type="radio"]');
            let answered = false;
            radios.forEach((radio) => {
                if (radio.checked) {
                    answered = true;
                }
            });
            if (!answered) {
                allAnswered = false;
                question.classList.add('unanswered');
            } else {
                question.classList.remove('unanswered');
            }
        });

        if (!allAnswered) {
            e.preventDefault();
            alert('아직 모든 설문에 답하지 않았습니다.');
        }
    });

    updateButtons();
});
