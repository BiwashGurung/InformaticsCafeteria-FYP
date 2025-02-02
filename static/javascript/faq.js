// Initiate the FAQ accordion
    document.addEventListener("DOMContentLoaded", function () {
        const questions = document.querySelectorAll(".faq-question");

        questions.forEach((question) => {
            question.addEventListener("click", function () {
                const faq = this.parentElement;
                const answer = faq.querySelector(".faq-answer");

                // Close other open FAQs
                document.querySelectorAll(".faq").forEach((item) => {
                    if (item !== faq) {
                        item.classList.remove("active");
                        item.querySelector(".faq-answer").style.display = "none";
                    }
                });

                // Toggle current FAQ
                faq.classList.toggle("active");
                answer.style.display = faq.classList.contains("active") ? "block" : "none";
            });
        });
    });
